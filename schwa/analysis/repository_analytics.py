REVISIONS_WEIGHT = 0.1
AUTHORS_WEIGHT = 0.3
AGE_WEIGHT = 0.1
FIXES_WEIGHT = 0.5


class Metrics:
    def __init__(self, revisions=0, fixes=0, authors=set(), twr=0, age=0):
        self.revisions = revisions
        self.fixes = fixes
        self.authors = authors
        self.twr = twr
        self.age = age
        self.defect = 0

    def compute_defect(self, total_revisions, total_authors, total_twr, total_age):
        prob = (self.revisions / total_revisions) * REVISIONS_WEIGHT \
            + (len(self.authors) / total_authors) * AUTHORS_WEIGHT \
            + (self.twr / total_twr) * FIXES_WEIGHT \
            + ((total_age - self.age) / total_age) * AGE_WEIGHT
        self.defect = prob


class RepositoryAnalytics(Metrics):
    def __init__(self, files_analytics={}, revisions=0, fixes=0, authors=set(), twr=0, age=0):
        super().__init__(revisions, fixes, authors, twr, age)
        self.files_analytics = files_analytics
        self.defect = 1.0

    def compute_defect(self):
        for f in self.files_analytics.values():
            f.compute_defect(self.revisions, len(self.authors), self.twr, self.age)


class FileAnalytics(Metrics):
    def __init__(self, classes_analytics={}, revisions=0, fixes=0, authors=set(), twr=0, age=0):
        super().__init__(revisions, fixes, authors, twr, age)
        self.classes_analytics = classes_analytics

    def compute_defect(self, total_revisions, total_authors, total_twr, total_age):
        super().compute_defect(total_revisions, total_authors, total_twr, total_age)
        for c in self.classes_analytics.values():
            c.compute_defect(total_revisions, total_authors, total_twr, total_age)


class ClassAnalytics(Metrics):
    def __init__(self, methods_analytics={}, revisions=0, fixes=0, authors=set(), twr=0, age=0):
        super().__init__(revisions, fixes, authors, twr, age)
        self.methods_analytics = methods_analytics

    def compute_defect(self, total_revisions, total_authors, total_twr, total_age):
        super().compute_defect(total_revisions, total_authors, total_twr, total_age)
        for m in self.methods_analytics.values():
            m.compute_defect(total_revisions, total_authors, total_twr, total_age)


class MethodAnalytics(Metrics):
    def __init__(self,  revisions=0, fixes=0, authors=set(), twr=0, age=0):
        super().__init__(revisions, fixes, authors, twr, age)