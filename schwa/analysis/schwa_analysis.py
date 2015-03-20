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

    @staticmethod
    def is_bug_fixing(commit):
        return re.search("bug|fix|corrigido", commit.message, re.I)

    def update_analytics(self, analytics, is_bug_fixing, author, commit_timestamp):
        analytics.update(ts=commit_timestamp, begin_ts=self.repository.begin_ts, current_ts=self.repository.last_ts,
                         is_bug_fixing=is_bug_fixing, author=author)

    def analyze(self):
        """ Analyzes a repository and creates analytics.

        It iterates over commits to analyze all the information.

        Returns:
            A RepositoryAnalytics instance.
        """
        analytics = RepositoryAnalytics()

        for commit in self.repository.commits:
            is_bug_fixing = SchwaAnalysis.is_bug_fixing(commit)

            """ Repository Granularity """
            self.update_analytics(analytics, is_bug_fixing, commit.author, commit.timestamp)

            """ File Granularity"""
            for diff in [diff for diff in commit.diffs if isinstance(diff, DiffFile)]:
                file_analytics = None
                if diff.added:
                    file_analytics = FileAnalytics()
                    analytics.files_analytics[diff.file_b] = file_analytics
                elif diff.modified:
                    if diff.file_b not in analytics.files_analytics:
                        file_analytics = FileAnalytics()
                        analytics.files_analytics[diff.file_b] = file_analytics
                    else:
                        file_analytics = analytics.files_analytics[diff.file_b]
                elif diff.renamed:
                    if diff.file_a not in analytics.files_analytics:
                        file_analytics = FileAnalytics()
                        analytics.files_analytics[diff.file_b] = file_analytics
                    else:
                        analytics.files_analytics[diff.file_b] = analytics.files_analytics.pop(diff.file_a)
                        file_analytics = analytics.files_analytics[diff.file_b]
                elif diff.removed:
                    if diff.file_a in analytics.files_analytics:
                        del analytics.files_analytics[diff.file_a]
                    continue  # To avoid update of removed components pragma: no cover
                self.update_analytics(file_analytics, is_bug_fixing, commit.author, commit.timestamp)

            """ Class Granularity """
            for diff in [diff for diff in commit.diffs if isinstance(diff, DiffClass)]:
                class_analytics = None

                try:
                    global_class_analytics = analytics.files_analytics[diff.file_name].classes_analytics
                # File could be already removed
                except KeyError:
                    continue

                if diff.added:
                    class_analytics = ClassAnalytics()
                    global_class_analytics[diff.class_b] = class_analytics
                elif diff.modified:
                    if diff.class_b not in global_class_analytics:
                        class_analytics = ClassAnalytics()
                        global_class_analytics[diff.class_b] = class_analytics
                    else:
                        class_analytics = global_class_analytics[diff.class_b]
                elif diff.renamed:
                    if diff.class_a not in global_class_analytics:
                        class_analytics = ClassAnalytics()
                        global_class_analytics[diff.class_b] = class_analytics
                    else:
                        global_class_analytics[diff.class_b] = global_class_analytics.pop(diff.class_a)
                        class_analytics = global_class_analytics[diff.class_b]
                elif diff.removed:
                    if diff.class_a in global_class_analytics:
                        del global_class_analytics[diff.class_a]
                    continue  # To avoid update of removed components pragma: no cover

                self.update_analytics(class_analytics, is_bug_fixing, commit.author, commit.timestamp)

            """ Method Granularity """
            for diff in [diff for diff in commit.diffs if isinstance(diff, DiffMethod)]:
                method_analytics = None

                try:
                    global_method_analytics = analytics.files_analytics[diff.file_name].classes_analytics[diff.class_name].methods_analytics
                # Class could be already removed and will raise a KeyError
                except KeyError:
                    continue

                if diff.added:
                    method_analytics = MethodAnalytics()
                    global_method_analytics[diff.method_b] = method_analytics
                elif diff.modified:
                    if diff.method_b not in global_method_analytics:
                        method_analytics = MethodAnalytics()
                        global_method_analytics[diff.method_b] = method_analytics
                    else:
                        method_analytics = global_method_analytics[diff.method_b]
                elif diff.renamed:
                    if diff.method_a not in global_method_analytics:
                        method_analytics = MethodAnalytics()
                        global_method_analytics[diff.method_b] = method_analytics
                    else:
                        global_method_analytics[diff.method_b] = global_method_analytics.pop(diff.method_a)
                        method_analytics = global_method_analytics[diff.method_b]
                elif diff.removed:
                    if diff.method_a in global_method_analytics:
                        del global_method_analytics[diff.method_a]
                    continue  # To avoid update of removed components pragma: no cover

                self.update_analytics(method_analytics, is_bug_fixing, commit.author, commit.timestamp)
        analytics.compute_defect_probability()
        return analytics