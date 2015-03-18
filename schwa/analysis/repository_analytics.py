import math


class Metrics:
    fixes_dataset = []
    fixes_weight = 0.5
    authors_weight = 0.25
    revisions_weight = 0.25

    def __init__(self):
        self.revisions_timestamps = []
        self.fixes_timestamps = []
        self.authors_timestamps = []
        self.revisions_twr = 0
        self.fixes_twr = 0
        self.authors_twr = 0
        self.authors = set()
        self.fixes = 0
        self.revisions = 0
        self.defect_prob = 0

    @staticmethod
    def normalise_timestamp(begin_ts, ts, current_ts):
        begin_diff = ts - begin_ts
        diff = current_ts - begin_ts
        normalized = begin_diff / diff
        return normalized

    @staticmethod
    def twr(begin_ts, ts, current_ts):
        ts = Metrics.normalise_timestamp(begin_ts, ts, current_ts)
        twr = 1 / (1 + math.e ** (-12 * ts + 12))
        return twr

    @staticmethod
    def list_twr(seq, begin_ts, current_ts):
        twr_sum = 0
        for ts in seq:
            twr_sum += Metrics.twr(begin_ts, ts, current_ts)
        return twr_sum

    def update(self, begin_ts, ts, current_ts, author, is_bug_fixing):
        # Fixes
        if is_bug_fixing:
            self.add_to_dataset(begin_ts)
            self.fixes += 1
            self.fixes_timestamps.append(ts)
            self.fixes_twr += Metrics.twr(begin_ts, ts, current_ts)
        # Revisions
        self.revisions += 1
        self.revisions_timestamps.append(ts)
        self.revisions_twr += Metrics.twr(begin_ts, ts, current_ts)
        # Authors
        if author not in self.authors:
            self.authors.add(author)
            self.authors_timestamps.append(ts)
            self.authors_twr += Metrics.twr(begin_ts, ts, current_ts)

    def add_to_dataset(self, begin_ts):
        # Reasoning: In the last revision, this component had a bug
        if self.revisions_timestamps:
            last_revision_timestamp = self.revisions_timestamps[-1]
            revisions_twr = Metrics.list_twr(self.revisions_timestamps, begin_ts, last_revision_timestamp)
            fixes_twr = Metrics.list_twr(self.fixes_timestamps, begin_ts, last_revision_timestamp)
            authors_twr = Metrics.list_twr(self.authors_timestamps, begin_ts, last_revision_timestamp)
            Metrics.fixes_dataset.append((revisions_twr, fixes_twr, authors_twr))

    def defect_probability(self):
        twr = Metrics.fixes_weight * self.fixes_twr + Metrics.revisions_weight * self.revisions_twr \
            + Metrics.authors_weight * self.authors_twr
        probability = 1 - math.e ** (- twr)
        return probability


class RepositoryAnalytics(Metrics):
    def __init__(self):
        super().__init__()
        self.files_analytics = {}

    def compute_defect_probability(self):
        self.defect_prob = self.defect_probability()
        for file_analytics in self.files_analytics.values():
            file_analytics.compute_defect_probability()


class FileAnalytics(Metrics):
    def __init__(self):
        super().__init__()
        self.classes_analytics = {}

    def compute_defect_probability(self):
        self.defect_prob = self.defect_probability()
        for class_analytics in self.classes_analytics.values():
            class_analytics.compute_defect_probability()


class ClassAnalytics(Metrics):
    def __init__(self):
        super().__init__()
        self.methods_analytics = {}

    def compute_defect_probability(self):
        self.defect_prob = self.defect_probability()
        for method_analytics in self.methods_analytics.values():
            method_analytics.compute_defect_probability()


class MethodAnalytics(Metrics):
    def __init__(self):
        super().__init__()

    def compute_defect_probability(self):
        self.defect_prob = self.defect_probability()
