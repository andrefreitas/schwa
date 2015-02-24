import re
import time
import math
from analysis.abstract_analysis import AbstractAnalysis


class TimeWeightedRiskAnalysis(AbstractAnalysis):

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
        metrics = {}
        creation_timestamp = self.repository.timestamp

        for commit in self.repository.commits.values():
            if not TimeWeightedRiskAnalysis.is_bug_fixing(commit):
                continue
            files = commit.files_ids
            ts = TimeWeightedRiskAnalysis.normalise_timestamp(creation_timestamp, commit.timestamp, current_timestamp)
            calc = 1 / (1 + math.e ** (-12 * ts + 12))
            for f in files:
                if f not in metrics:
                    metrics[f] = 0
                metrics[f] += calc
        return metrics