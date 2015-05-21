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



from schwa.extraction import GitExtractor
from schwa.analysis import SchwaAnalysis
from schwa.learning import FeatureWeightLearner



class Schwa:
    """ GIT repositories analyzer.

    Schwa is a tool that analyzes GIT repositories of Java projects and
    predicts component's reliability from a variety of metrics.

    Attributes:
        repo_path: A string that contains the repository local path.
    """

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
        extractor = GitExtractor(self.repo_path)
        repo = extractor.extract(ignore_regex, max_commits, method_granularity, parallel)
        analysis = SchwaAnalysis(repo)
        analytics = analysis.analyze()
        return analytics

    def learn(self,  ignore_regex="^$", max_commits=None, method_granularity=False, parallel=True,
              bits=None, generations=None):
        extractor = GitExtractor(self.repo_path)
        repo = extractor.extract(ignore_regex, max_commits, method_granularity, parallel)
        solution = FeatureWeightLearner(repo, bits, generations).learn()
        return solution







