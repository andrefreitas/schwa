# Copyright (c) 2015 Faculty of Engineering of the University of Porto
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" Module for representing a repository.

Software evolution can be described as a set of commits that have a set off diffs.
This differences (diffs) can be at File, Class or Method granularity.
"""

import re


class Repository:
    """ Repository class.

    A repository have commits, and information of first and last commit timestamps.

    Attributes:
        commits: List of commits
        begin_ts: An int representing the first commit timestamp
        last_ts: An int representing the last commit timestamp
    """

    def __init__(self, commits, begin_ts, last_ts):
        self.commits = commits
        self.begin_ts = begin_ts
        self.last_ts = last_ts


class Commit:
    """ Commit class.

    A class to represent a Commit with its most important information.

    Attributes:
        _id: A string that is the unique identifier of that commit.
        message: A string with the commit message.
        author: A string with the email of the author.
        timestamp: An int with the timestamp of the commit
        diffs: A list of Diff instances.
    """

    def __init__(self, _id, message, author, timestamp, diffs):
        self._id = _id
        self.message = message
        self.author = author
        self.timestamp = timestamp
        self.diffs = diffs

    def is_bug_fixing(self):
        return re.search("fix(e[ds])?|bugs?|defects?|patch|corrigidos?|close([sd])?|resolve([sd])?", self.message, re.I)


class Diff:
    """ Diff class.

    Represents a change in a certain component.

    Attributes:
        version_a: Object representing the version A of the change.
        version_b: Object representing the version B of the change.
        renamed: Optional boolean that indicates that the changes was a renaming.
        modified: Optional boolean that indicates that the change was a modification.
        added: Optional boolean that indicates that the change was an addition.
        removed: Optional boolean that indicates that the change was a removal.
    """

    def __init__(self, version_a, version_b, renamed=False, modified=False, added=False, removed=False):
        self.version_a = version_a
        self.version_b = version_b
        self.renamed = renamed
        self.modified = modified
        self.added = added
        self.removed = removed

    def __eq__(self, other):
        return self.version_a == other.version_a and self.version_b == other.version_b and \
            self.renamed == other.renamed and self.modified == other.modified and self.added == other.added \
            and self.removed == other.removed

    def __repr__(self):
        if self.renamed:
            return "renamed"
        elif self.modified:
            return "modified"
        elif self.added:
            return "added"
        elif self.removed:
            return "removed"

    def component_a(self):
        return self.version_a

    def component_b(self):
        return self.version_b


class DiffFile(Diff):
    """ Diff of a File component.

    Represents a changed made to a File and it is a subclass of Diff.

    Attributes:
        file_a: A File object representing the version A of the file.
        file_b: A File object representing the version B of the file.
    """

    def __init__(self, file_a=None, file_b=None, renamed=False, modified=False, added=False, removed=False):
        super().__init__(file_a, file_b, renamed, modified, added, removed)
        self.parent = None

    def __eq__(self, other):
        if isinstance(other, DiffFile):
            return super().__eq__(other)
        else:
            return False

    def __repr__(self):
        return "%s file %s,%s" % (super().__repr__(), self.version_a, self.version_b)


class DiffClass(Diff):
    """ Diff of a Class component.

    Represents a changed made to a Class and it is a subclass of Diff.

    Attributes:
        parent: An object representing the parent that the class belongs, e.g., Class or File.
        class_a: A Class object with version A of the class.
        class_b: A Class object with version B of the class.
    """

    def __init__(self, parent, class_a=None, class_b=None, renamed=False, modified=False, added=False,
                 removed=False):
        super().__init__(class_a, class_b, renamed, modified, added, removed)
        self.parent = parent

    def __eq__(self, other):
        if isinstance(other, DiffClass):
            return self.parent == other.parent and super().__eq__(other)
        else:
            return False

    def __repr__(self):
        return "%s class %s,%s in %s" % (super().__repr__(), self.version_a, self.version_b, self.parent)


class DiffMethod(Diff):
    """ Diff of a Method component.

    Represents a change made to a Method and it is a subclass of Diff.

    Attributes:
        parent: An object representing the parent that the method belongs, e.g., Class or File.
        method_a: A Method object with version A of the method.
        methods_b: A Method object with version B of the method.
    """
    def __init__(self, parent, method_a=None, method_b=None, renamed=False, modified=False, added=False, removed=False):
        super().__init__(method_a, method_b, renamed, modified, added, removed)
        self.parent = parent

    def __eq__(self, other):
        if isinstance(other, DiffMethod):
            return self.parent == other.parent and super().__eq__(other)
        else:
            return False

    def __repr__(self):
        return "%s method %s,%s in %s" % (super().__repr__(), self.version_a, self.version_b, self.parent)


class DiffLine(Diff):
    """ Diff of a Line component.

    Represents a change made to a Line and it is a subclass of Diff.

    Attributes:
        parent: An object representing the parent that the line belongs, e.g., Method, Class, or File.
        line_a: A Line object with version A of the line.
        line_a: A Line object with version B of the line.
    """
    def __init__(self, parent, line_a=None, line_b=None, renamed=False, modified=False, added=False, removed=False):
        super().__init__(line_a, line_b, renamed, modified, added, removed)
        self.parent = parent

    def __eq__(self, other):
        if isinstance(other, DiffLine):
            return self.parent == other.parent and super().__eq__(other)
        else:
            return False

    def __repr__(self):
        return "%s line %s,%s in %s" % (super().__repr__(), self.version_a, self.version_b, self.parent)
