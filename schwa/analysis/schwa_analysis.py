import re
import time
import math
from analysis.abstract_analysis import AbstractAnalysis
from .repository_analytics import *
from repository import *


class SchwaAnalysis(AbstractAnalysis):

    def __init__(self, repository):
        super().__init__(repository)

    @staticmethod
    def is_bug_fixing(commit):
        return re.search("bug|fix", commit.message, re.I)

    @staticmethod
    def normalise_timestamp(begin_ts, ts, current_ts):
        begin_diff = ts - begin_ts
        diff = current_ts - begin_ts
        normalized = begin_diff / diff
        return normalized

    @staticmethod
    def update_analytics(analytics, is_bug_fixing, author, repo_ts, commit_ts, current_ts):
        analytics.update_revisions(repo_ts, commit_ts, current_ts)
        if is_bug_fixing:
            analytics.update_fixes(repo_ts, commit_ts, current_ts)
        analytics.update_authors(repo_ts, commit_ts, current_ts, author)

    def analyze(self):
        current_timestamp = time.time()
        analytics = RepositoryAnalytics()

        for commit in self.repository.commits:
            is_bug_fixing = SchwaAnalysis.is_bug_fixing(commit)

            """ Repository Granularity """
            SchwaAnalysis.update_analytics(analytics, is_bug_fixing, commit.author, self.repository.timestamp,
                                           commit.timestamp, current_timestamp)

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
                    continue

                SchwaAnalysis.update_analytics(file_analytics, is_bug_fixing, commit.author, self.repository.timestamp,
                                               commit.timestamp, current_timestamp)

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
                    continue

                SchwaAnalysis.update_analytics(class_analytics, is_bug_fixing, commit.author, self.repository.timestamp,
                                               commit.timestamp, current_timestamp)

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
                    continue

                SchwaAnalysis.update_analytics(method_analytics, is_bug_fixing, commit.author,
                                               self.repository.timestamp, commit.timestamp, current_timestamp)

        return analytics