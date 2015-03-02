class Repository:
    def __init__(self, commits, timestamp):
        self.commits = commits
        self.timestamp = timestamp


class Commit:
    def __init__(self, _id, message, author, timestamp, diffs):
        self._id = _id
        self.message = message
        self.author = author
        self.timestamp = timestamp
        self.diff = diffs


class Diff:
    def __init__(self, renamed=False, modified=False, added=False, removed=False):
        self.renamed = renamed
        self.modified = modified
        self.added = added
        self.removed = removed


class DiffFile(Diff):
    def __init__(self, file_a=None, file_b=None, renamed=False, modified=False, added=False, removed=False):
        self.file_a = file_a
        self.file_b = file_b
        super().__init__(renamed, modified, added, removed)


class DiffClass(Diff):
    def __init__(self, file_name, class_a=None, class_b=None, renamed=False, modified=False, added=False, removed=False):
        self.file_name = file_name
        self.class_a = class_a
        self.class_b = class_b
        super().__init__(renamed, modified, added, removed)


class DiffMethod(Diff):
    def __init__(self, file_name, class_name, method_a=None, method_b=None, renamed=False, modified=False, added=False, removed=False):
        self.file_name = file_name
        self.class_name = class_name
        self.method_a = method_a
        self.method_b = method_b
        super().__init__(renamed, modified, added, removed)