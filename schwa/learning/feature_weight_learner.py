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
import itertools

# TODO: Write module documentation


class FeatureWeightLearner:

    BITS_PRECISION = 2
    POPULATION = 100
    GENERATIONS = 100
    FEATURES = 3

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
        self.toolbox.register("attr_bool", random.randint, 0, 1)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool,
                              n=FeatureWeightLearner.FEATURES * FeatureWeightLearner.BITS_PRECISION)
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

        all_components = set()
        distance = 0
        distances = []
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
            if commit.is_bug_fixing():
                not_involved_components = all_components - involved_components
                distance_commit = FeatureWeightLearner.distance(analytics, involved_components, not_involved_components, revisions_weight, fixes_weight, authors_weight)
                distance += distance_commit
                distances.append(distance_commit)

        return distance

    @staticmethod
    def distance(analytics, involved_components, not_involved_components, revisions_weight, fixes_weight, authors_weight):
        schwa_avg_involved = FeatureWeightLearner.average_schwa(involved_components, analytics,
                                                                revisions_weight, fixes_weight, authors_weight)
        schwa_avg_not_involved = FeatureWeightLearner.average_schwa(not_involved_components, analytics,
                                                                    revisions_weight, fixes_weight, authors_weight)
        return schwa_avg_involved - schwa_avg_not_involved


    @staticmethod
    def average_schwa(components, analytics, revisions_weight, fixes_weight, authors_weight):
        schwa_sum = 0
        n = 0
        for component in components:
            a = analytics.files_analytics[component]
            if a.last_twr:
                revisions, fixes, authors = a.last_twr
                schwa_prob = Metrics.compute_defect_probability(revisions, fixes, authors,
                                                                revisions_weight, fixes_weight, authors_weight)
                n += 1
                schwa_sum += schwa_prob
        if n > 0:
            return schwa_sum / n
        else:
            return 0

    @staticmethod
    def decode_individual(individual):
        ind = list(zip(*(iter(map(str, individual)),) * FeatureWeightLearner.BITS_PRECISION))
        ind = list(map(lambda t: int("".join(t), 2), ind))
        max_encoded = int("1" * FeatureWeightLearner.BITS_PRECISION, 2)
        weights = list(map(lambda w: w / max_encoded, ind))
        return weights

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


        best = tools.selBest(population, k=1)[0]
        revisions_weight, fixes_weight, authors_weight = FeatureWeightLearner.decode_individual(best)
        weights["revisions"] = revisions_weight
        weights["fixes"] = fixes_weight
        weights["authors"] = authors_weight
        return weights

    def learn_sort(self):
        weights = {}

        population = list(itertools.product([0, 1], repeat=3 * FeatureWeightLearner.BITS_PRECISION))
        sorted_population = sorted(population, key=self.fitness_wrapper, reverse=True)
        sorted_population_fitness = list(map(self.fitness_wrapper, sorted_population))
        best = sorted_population[0]
        revisions_weight, fixes_weight, authors_weight = FeatureWeightLearner.decode_individual(best)
        weights["revisions"] = revisions_weight
        weights["fixes"] = fixes_weight
        weights["authors"] = authors_weight
        print(sorted_population)
        print(sorted_population_fitness)
        return weights




