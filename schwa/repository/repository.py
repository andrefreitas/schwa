class Repository:
    def __init__(self, commits, begin_ts, last_ts):
        self.commits = commits
        self.begin_ts = begin_ts
        self.last_ts = last_ts


class Commit:
    def __init__(self, _id, message, author, timestamp, diffs):
        self._id = _id
        self.message = message
        self.author = author
        self.timestamp = timestamp
        self.diffs = diffs


class Diff:
    def __init__(self, renamed=False, modified=False, added=False, removed=False):
        self.renamed = renamed
        self.modified = modified
        self.added = added
        self.removed = removed

    def __eq__(self, other):
        return self.renamed == other.renamed and self.modified == other.modified and self.added == other.added \
            and self.removed == other.removed


class DiffFile(Diff):
    def __init__(self, file_a=None, file_b=None, renamed=False, modified=False, added=False, removed=False):
        self.file_a = file_a
        self.file_b = file_b
        super().__init__(renamed, modified, added, removed)

    def __eq__(self, other):
        if isinstance(other, DiffFile):
            return self.file_a == other.file_a and self.file_b == other.file_b and super().__eq__(other)
        else:
            return False


class DiffClass(Diff):
    def __init__(self, file_name, class_a=None, class_b=None, renamed=False, modified=False, added=False,
                 removed=False):
        self.file_name = file_name
        self.class_a = class_a
        self.class_b = class_b
        super().__init__(renamed, modified, added, removed)

    def __eq__(self, other):
        if isinstance(other, DiffClass):
            return self.file_name == other.file_name and self.class_a == other.class_a and self.class_b == other.class_b \
                and super().__eq__(other)
        else:
            return False


class DiffMethod(Diff):
    def __init__(self, file_name, class_name, method_a=None, method_b=None, renamed=False, modified=False, added=False,
                 removed=False):
        self.file_name = file_name
        self.class_name = class_name
        self.method_a = method_a
        self.method_b = method_b
        super().__init__(renamed, modified, added, removed)

    def __eq__(self, other):
        if isinstance(other, DiffMethod):
            return self.file_name == other.file_name and self.class_name == other.class_name and \
                self.method_a == other.method_a and self.method_b == other.method_b and super().__eq__(other)
        else:
            return False