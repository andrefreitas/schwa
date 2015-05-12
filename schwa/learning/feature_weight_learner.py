# Copyright (c) 2015 Faculty of Engineering of the University of Porto
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" Module for the Feature Weight Learner """

import random
from deap import base, creator, tools, algorithms
from schwa.analysis import *
from schwa.repository import *

# TODO: Write module documentation


class FeatureWeightLearner:

    BITS_PRECISION = 3
    POPULATION = 1000
    GENERATIONS = 100

    def __init__(self, repository):
        self.repository = repository
        self.toolbox = base.Toolbox()
        self.setup()

    def setup(self):
        # Single-objective maximization (1.0)
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))

        # Individual
        creator.create("Individual", list, fitness=creator.FitnessMax)

        # Types
        max_int = int("1" * FeatureWeightLearner.BITS_PRECISION, 2)
        self.toolbox.register("attr_bool", random.randint, 0, max_int)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool, n=3)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        # Operators
        self.toolbox.register("evaluate", self.fitness_wrapper)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def update_analytics(self, analytics, commit):
        """ Updates analytics.

        By giving commit data, updates the component analytics.

        Args:
            analytics: An instance of analytics.
            commit: A commit instance.
        """

        analytics.update(ts=commit.timestamp, begin_ts=self.repository.begin_ts, current_ts=self.repository.last_ts,
                         is_bug_fixing=commit.is_bug_fixing(), author=commit.author)

    def fitness_wrapper(self, individual):
        revisions_weight, fixes_weight, authors_weight = FeatureWeightLearner.decode_individual(individual)
        return self.fitness(revisions_weight, fixes_weight, authors_weight),

    def fitness(self, revisions_weight, fixes_weight, authors_weight):

        Metrics.REVISIONS_WEIGHT = revisions_weight
        Metrics.FIXES_WEIGHT = fixes_weight
        Metrics.AUTHORS_WEIGHT = authors_weight

        all_components = set()
        distance = 0
        analytics = RepositoryAnalytics()

        for commit in self.repository.commits:

            involved_components = set()

            # Repository Granularity
            self.update_analytics(analytics, commit)

            # File Granularity
            parent_analytics_dict = analytics.files_analytics
            for diff in [diff for diff in commit.diffs if isinstance(diff, DiffFile)]:
                file_analytics = SchwaAnalysis.get_analytics_from_tree(parent_analytics_dict, diff, FileAnalytics())
                if diff.renamed or diff.removed:
                    all_components.discard(diff.file_a)
                if file_analytics:
                    involved_components.add(diff.file_b)
                    all_components.add(diff.file_b)
                    self.update_analytics(file_analytics, commit)

            # Distance
            not_involved_components = all_components - involved_components
            distance += FeatureWeightLearner.distance(analytics, involved_components, not_involved_components)

        return distance

    @staticmethod
    def distance(analytics, involved_components, not_involved_components):
        schwa_avg_involved = FeatureWeightLearner.average_schwa(involved_components, analytics)
        schwa_avg_not_involved = FeatureWeightLearner.average_schwa(not_involved_components, analytics)
        return schwa_avg_involved - schwa_avg_not_involved


    @staticmethod
    def average_schwa(components, analytics):
        schwa_sum = 0
        n = 0
        for component in components:
            schwa_prob = analytics.files_analytics[component].last_defect_prob
            if schwa_prob:
                n += 1
                schwa_sum += schwa_prob
        if n > 0:
            return schwa_sum / n
        else:
            return 0

    @staticmethod
    def decode_individual(individual):
        max_encoded = int("1" * FeatureWeightLearner.BITS_PRECISION, 2)
        return individual[0] / max_encoded, individual[1] / max_encoded, individual[2] / max_encoded

    def learn(self):
        weights = {}
        population = self.toolbox.population(n=FeatureWeightLearner.POPULATION)
        NGEN = FeatureWeightLearner.GENERATIONS
        for gen in range(NGEN):
            offspring = algorithms.varAnd(population, self.toolbox, cxpb=0.5, mutpb=0.1)
            fits = self.toolbox.map(self.toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            population = self.toolbox.select(offspring, k=len(population))
        top10 = tools.selBest(population, k=10)
        best = tools.selBest(population, k=1)[0]
        #print(top10)
        revisions_weight, fixes_weight, authors_weight = FeatureWeightLearner.decode_individual(best)
        weights["revisions"] = revisions_weight
        weights["fixes"] = fixes_weight
        weights["authors"] = authors_weight
        return weights



