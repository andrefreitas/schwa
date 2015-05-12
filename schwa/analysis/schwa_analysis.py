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

""" Module for the analysis algorithm. """

import re
from schwa.analysis import *
from schwa.repository import *


class SchwaAnalysis(AbstractAnalysis):
    """ Class representing the Schwa Analysis. """
    def __init__(self, repository):
        super().__init__(repository)

    def update_analytics(self, analytics, commit):
        """ Updates analytics.

        By giving commit data, updates the component analytics.

        Args:
            analytics: An instance of analytics.
            commit: A commit instance.
        """

        analytics.update(ts=commit.timestamp, begin_ts=self.repository.begin_ts, current_ts=self.repository.last_ts,
                         is_bug_fixing=commit.is_bug_fixing(), author=commit.author)
    @staticmethod
    def get_analytics_from_tree(parent_analytics_dict, diff, instance):
        analytics = None

        if diff.added:
            analytics = instance
            parent_analytics_dict[diff.component_b()] = analytics

        elif diff.modified:
            if diff.component_b() not in parent_analytics_dict:
                analytics = instance
                parent_analytics_dict[diff.component_b()] = analytics
            else:
                analytics = parent_analytics_dict[diff.component_b()]

        elif diff.renamed:
            if diff.component_a() not in parent_analytics_dict:
                analytics = instance
                parent_analytics_dict[diff.component_b()] = analytics
            else:
                analytics = parent_analytics_dict.pop(diff.component_a())
                parent_analytics_dict[diff.component_b()] = analytics

        elif diff.removed:
            if diff.component_a() in parent_analytics_dict:
                del parent_analytics_dict[diff.component_a()]
            return False

        return analytics

    def analyze(self):
        """ Analyzes a repository and creates analytics.

        It iterates over commits to analyze all the information. The granularity order must be
        preserved because child components depend of the parents.

        Returns:
            A RepositoryAnalytics instance.
        """
        analytics = RepositoryAnalytics()

        for commit in self.repository.commits:

            # Repository Granularity
            self.update_analytics(analytics, commit)

            # File Granularity
            parent_analytics_dict = analytics.files_analytics
            for diff in [diff for diff in commit.diffs if isinstance(diff, DiffFile)]:
                file_analytics = SchwaAnalysis.get_analytics_from_tree(parent_analytics_dict, diff, FileAnalytics())
                if file_analytics:
                    self.update_analytics(file_analytics, commit)

            # Class Granularity
            for diff in [diff for diff in commit.diffs if isinstance(diff, DiffClass)]:
                try:  # Parent component can be already removed
                    parent_analytics_dict = analytics.files_analytics[diff.file_name].classes_analytics
                    class_analytics = SchwaAnalysis.get_analytics_from_tree(parent_analytics_dict, diff, ClassAnalytics())
                    if class_analytics:
                        self.update_analytics(class_analytics, commit)
                except KeyError:
                    continue

            # Method Granularity
            for diff in [diff for diff in commit.diffs if isinstance(diff, DiffMethod)]:
                try:  # Parent component can be already removed
                    parent_analytics_dict = analytics.files_analytics[diff.file_name].classes_analytics[diff.class_name].methods_analytics
                    method_analytics = SchwaAnalysis.get_analytics_from_tree(parent_analytics_dict, diff, MethodAnalytics())
                    if method_analytics:
                        self.update_analytics(method_analytics, commit)
                except KeyError:
                    continue

        analytics.compute_defect_probability()

        return analytics