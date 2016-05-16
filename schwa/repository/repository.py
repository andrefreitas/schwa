import re

class Commit:
    def __init__(self, identifier, message, author, timestamp, diffs):
        self.identifier = identifier
        self.message = message
        self.author = author
        self.timestamp = timestamp
        self.diffs = diffs

    def is_bug_fix(self):
        return re.search("fix(e[ds])?|bugs?|defects?|patch|corrigidos?|close([sd])?|resolve([sd])?", self.message, re.I)


class Diff:
    def __init__(self, component_a=None, component_b=None, modified=False, added=False, removed=False, renamed=False, parent=None):
        self.component_a = component_a
        self.component_b = component_b
        self.modified = modified
        self.added = added
        self.removed = removed
        self.renamed = renamed
