class Metrics:
    def __init__(self, revisions=0, fixes=0, authors=set(), twr=0, age=0):
        self.revisions = revisions
        self.fixes = fixes
        self.authors = authors
        self.twr = twr
        self.age = age


class RepositoryAnalytics(Metrics):
    def __init__(self, files_analytics={}, revisions=0, fixes=0, authors=set(), twr=0, age=0):
        super().__init__(revisions, fixes, authors, twr, age)
        self.files_analytics = files_analytics


class FileAnalytics(Metrics):
    def __init__(self, classes_analytics={}, revisions=0, fixes=0, authors=set(), twr=0, age=0):
        super().__init__(revisions, fixes, authors, twr, age)
        self.classes_analytics = classes_analytics


class ClassAnalytics(Metrics):
    def __init__(self, methods_analytics={}, revisions=0, fixes=0, authors=set(), twr=0, age=0):
        super().__init__(revisions, fixes, authors, twr, age)
        self.methods_analytics = methods_analytics


class MethodAnalytics(Metrics):
    def __init__(self,  revisions=0, fixes=0, authors=set(), twr=0, age=0):
        super().__init__(revisions, fixes, authors, twr, age)


