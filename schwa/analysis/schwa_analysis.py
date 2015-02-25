import re
import time
import math
from analysis.abstract_analysis import AbstractAnalysis


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
        metrics = {}
        creation_timestamp = self.repository.timestamp

        for commit in self.repository.commits.values():
            files = commit.files_ids

            twr = None
            if SchwaAnalysis.is_bug_fixing(commit):
                ts = SchwaAnalysis.normalise_timestamp(creation_timestamp, commit.timestamp, current_timestamp)
                twr = 1 / (1 + math.e ** (-12 * ts + 12))

            for f in files:
                if f in self.repository.files:
                    pass
                if f not in metrics:
                    metrics[f] = {
                        "revisions": 0,
                        "fixes": 0,
                        "authors": set(),
                        "twr": 0,
                        "age": 0,
                    }

                # TWR and Fixes
                if twr:
                    metrics[f]["twr"] += twr
                    metrics[f]["fixes"] += 1
                metrics[f]["revisions"] += 1
                metrics[f]["authors"].add(commit.author)
                diff_timestamp = current_timestamp - commit.timestamp
                if diff_timestamp > metrics[f]["age"]:
                    metrics[f]["age"] = diff_timestamp
        return metrics