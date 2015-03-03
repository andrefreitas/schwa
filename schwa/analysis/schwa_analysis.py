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

    def analyze(self):
        current_timestamp = time.time()
        analytics = RepositoryAnalytics()

        for commit in self.repository.commits:
            diff_timestamp = current_timestamp - commit.timestamp
            twr = None
            if SchwaAnalysis.is_bug_fixing(commit):
                ts = SchwaAnalysis.normalise_timestamp(self.repository.timestamp, commit.timestamp, current_timestamp)
                twr = 1 / (1 + math.e ** (-12 * ts + 12))

            """Repository Granularity"""
            analytics.revisions += 1
            analytics.authors.add(commit.author)
            if twr:
                analytics.fixes += 1
                analytics.twr += twr
            if diff_timestamp > analytics.age:
                analytics.age = diff_timestamp

            for diff in commit.diffs:

                """ File Granularity"""
                if isinstance(diff, DiffFile):
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

                    file_analytics.revisions += 1
                    file_analytics.authors.add(commit.author)
                    if twr:
                        file_analytics.fixes += 1
                        file_analytics.twr += twr
                    if diff_timestamp > file_analytics.age:
                        file_analytics.age = diff_timestamp

        return analytics