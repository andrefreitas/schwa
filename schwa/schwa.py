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

""" Main entry point to start using Schwa. """

import os
import yaml
from decimal import Decimal

from schwa.extraction import GitExtractor
from schwa.analysis import SchwaAnalysis, Metrics
from schwa.learning import FeatureWeightLearner


class Schwa:
    """ GIT repositories analyzer.

    Schwa is a tool that analyzes GIT repositories of Java projects and
    predicts component's reliability from a variety of metrics.

    Attributes:
        repo_path: A string that contains the repository local path.
        YAML_FILE: A string with the name of the Yaml file
    """

    YAML_FILE = ".schwa.yml"

    def __init__(self, repo_path):
        """ Inits Schwa with the repository local path. """
        self.repo_path = repo_path

    def analyze(self,  ignore_regex="^$", max_commits=None, method_granularity=True, parallel=True):
        """ Analyze commits.

        Extracts commits and call an analyzer to output analytics.

        Args:
            ignore_regex: An optional string that is a regex pattern to ignore unnecessary files.
            max_commits: An optional int that is the maximum number of commits to extract since the last one.
            method_granularity: An optional boolean that enables extraction until the method granularity.

        Returns:
            A RepositoryAnalytics instance.
        """
        configs = self.get_yaml_configs()
        max_commits = self.configure_yaml(configs, max_commits)
        extractor = GitExtractor(self.repo_path)
        repo = extractor.extract(ignore_regex, max_commits, method_granularity, parallel)
        analysis = SchwaAnalysis(repo)
        analytics = analysis.analyze()
        return analytics

    def configure_yaml(self, configs, max_commits):
        if not max_commits:
            max_commits = configs.get("commits", max_commits)

        time_range = configs.get("time_range")
        if time_range:
            Metrics.TIME_RANGE = Decimal(time_range)

        revisions_config = configs.get("features_weights", {}).get("revisions", False)
        fixes_config = configs.get("features_weights", {}).get("fixes", False)
        authors_config = configs.get("features_weights", {}).get("authors", False)

        if revisions_config and fixes_config and authors_config:
            if round((revisions_config + fixes_config + authors_config), 5) == 1:
                Metrics.REVISIONS_WEIGHT = Decimal(revisions_config)
                Metrics.FIXES_WEIGHT = Decimal(fixes_config)
                Metrics.AUTHORS_WEIGHT = Decimal(authors_config)
            else:
                raise SchwaConfigurationException("Errors in .schwa.yml: features weights sum must be 1!")
        return max_commits

    def get_yaml_configs(self):
        yaml_path = os.path.join(self.repo_path, Schwa.YAML_FILE)
        configs = {}
        if os.path.exists(yaml_path):
            stream = open(yaml_path, "r")
            configs = yaml.load(stream)

        return configs

    def learn(self,  ignore_regex="^$", max_commits=None, method_granularity=False, parallel=True,
              bits=None, generations=None):
        configs = self.get_yaml_configs()
        max_commits = self.configure_yaml(configs, max_commits)
        extractor = GitExtractor(self.repo_path)
        repo = extractor.extract(ignore_regex, max_commits, method_granularity, parallel)
        solution = FeatureWeightLearner(repo, bits, generations).learn()
        return solution

class SchwaConfigurationException(Exception):
    pass
