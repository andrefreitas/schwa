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

import copy
import re
from schwa.analysis import *
from schwa.repository import *


class SchwaAnalysis(AbstractAnalysis):
    """ Class representing the Schwa Analysis. """
    def __init__(self, repository):
        super().__init__(repository)

    @staticmethod
    def update_analytics(repository, analytics, commit):
        """ Updates analytics.

        By giving commit data, updates the component analytics.

        Args:
            analytics: An instance of analytics.
            commit: A commit instance.
        """

        analytics.update(ts=commit.timestamp, begin_ts=repository.begin_ts, current_ts=repository.last_ts,
                         is_bug_fixing=commit.is_bug_fixing(), author=commit.author)

    @staticmethod
    def create_analytics_from_diff(repository, parent_analytics, diff, commit, instance):
        analytics = None

        if diff.added:
            # Create analytics
            analytics = instance(repr(diff.version_b), repr(diff.version_b.name), parent_analytics)

        elif diff.modified:
            analytics = parent_analytics.get_analytics(repr(diff.version_b))
            if analytics == None:
                # Create new analytics
                analytics = instance(repr(diff.version_b), repr(diff.version_b.name), parent_analytics)

        elif diff.renamed:
            analytics_renamed = parent_analytics.get_analytics(repr(diff.version_a))
            if analytics_renamed != None:
                # Remove version_a
                parent_analytics.del_analytics(repr(diff.version_a))
                # Create new analytics
                analytics = instance(repr(diff.version_b), repr(diff.version_b.name), parent_analytics)
                # Update its metrics
                analytics.copy_metrics_from(analytics_renamed)

        elif diff.removed:
            # Remove version_a
            parent_analytics.del_analytics(repr(diff.version_a))

        if not diff.removed and analytics != None:
            # Update analytics
            SchwaAnalysis.update_analytics(repository, analytics, commit)

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
            self.update_analytics(self.repository, analytics, commit)

            # File Granularity
            for diff in [diff for diff in commit.diffs if isinstance(diff, DiffFile)]:
                SchwaAnalysis.create_analytics_from_diff(self.repository, analytics, diff, commit, FileAnalytics)

            # Class Granularity
            for diff in [diff for diff in commit.diffs if isinstance(diff, DiffClass)]:
                parent_analytics = analytics.get_analytics(repr(diff.parent))
                if parent_analytics == None:
                    # Parent component (i.e., file or class) no longer exist,
                    # thus no analytics is required
                    continue
                SchwaAnalysis.create_analytics_from_diff(self.repository, parent_analytics, diff, commit, ClassAnalytics)

            # Method Granularity
            for diff in [diff for diff in commit.diffs if isinstance(diff, DiffMethod)]:
                parent_analytics = analytics.get_analytics(repr(diff.parent))
                if parent_analytics == None:
                    # Parent component (i.e., file, class, or method) no longer
                    # exist, thus no analytics is required
                    continue
                SchwaAnalysis.create_analytics_from_diff(self.repository, parent_analytics, diff, commit, MethodAnalytics)

            # Line Granularity
            for diff in [diff for diff in commit.diffs if isinstance(diff, DiffLine)]:
                parent_analytics = analytics.get_analytics(repr(diff.parent))
                if parent_analytics == None:
                    # Parent component (i.e., file, class, or method) no longer
                    # exist, thus no analytics is required
                    continue
                SchwaAnalysis.create_analytics_from_diff(self.repository, parent_analytics, diff, commit, LineAnalytics)

        analytics.compute_defect_probability()

        return analytics