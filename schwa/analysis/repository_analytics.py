import math

FIXES_WEIGHT = 0.5
AUTHORS_WEIGHT = 0.2
REVISIONS_WEIGHT = 0.3
BETA = 1
ALPHA = 1


class Metrics:
    def __init__(self):
        self.revisions_twr = 0
        self.fixes_twr = 0
        self.authors_twr = 0
        self.authors = set()
        self.fixes = 0
        self.revisions = 0

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
    def convert_to_probability(twr):
        return 1 - BETA * math.e ** (- ALPHA * twr)

    def update_revisions(self, begin_ts, ts, current_ts):
        self.revisions += 1
        self.revisions_twr = Metrics.twr(begin_ts, ts, current_ts)

    def update_fixes(self, begin_ts, ts, current_ts):
        self.fixes += 1
        self.fixes_twr = Metrics.twr(begin_ts, ts, current_ts)

    def update_authors(self, begin_ts, ts, current_ts, author):
        if author not in self.authors:
            self.authors.add(author)
            self.authors_twr = Metrics.twr(begin_ts, ts, current_ts)

    def defect_probability(self):
        revisions_probability = Metrics.convert_to_probability(self.revisions_twr)
        fixes_probability = Metrics.convert_to_probability(self.fixes_twr)
        authors_probability = Metrics.convert_to_probability(self.authors_twr)
        probability = REVISIONS_WEIGHT * revisions_probability + FIXES_WEIGHT * fixes_probability \
            + AUTHORS_WEIGHT * authors_probability
        return probability


class RepositoryAnalytics(Metrics):
    def __init__(self):
        super().__init__()
        self.files_analytics = {}


class FileAnalytics(Metrics):
    def __init__(self):
        super().__init__()
        self.classes_analytics = {}


class ClassAnalytics(Metrics):
    def __init__(self):
        super().__init__()
        self.methods_analytics = {}


class MethodAnalytics(Metrics):
    def __init__(self):
        super().__init__()