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


class Diff:
    """ Diff class.

    Represents a change in a certain component.

    Attributes:
        renamed: Optional boolean that indicates that the changes was a renaming.
        modified: Optional boolean that indicates that the change was a modification.
        added: Optional boolean that indicates that the change was an addition.
        removed: Optional boolean that indicates that the change was a removal.
    """

    def __init__(self, renamed=False, modified=False, added=False, removed=False):
        self.renamed = renamed
        self.modified = modified
        self.added = added
        self.removed = removed

    def __eq__(self, other):
        return self.renamed == other.renamed and self.modified == other.modified and self.added == other.added \
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


class DiffFile(Diff):
    """ Diff of a File component.

    Represents a changed made to a File and it is a subclass of Diff.

    Attributes:
        file_a: String representing the path of version A of the file.
        file_b: String representing the path of version B of the file.
    """

    def __init__(self, file_a=None, file_b=None, renamed=False, modified=False, added=False, removed=False):
        self.file_a = file_a
        self.file_b = file_b
        super().__init__(renamed, modified, added, removed)

    def __eq__(self, other):
        if isinstance(other, DiffFile):
            return self.file_a == other.file_a and self.file_b == other.file_b and super().__eq__(other)
        else:
            return False

    def __repr__(self):
        return "%s file %s,%s" % (super().__repr__(), self.file_a, self.file_b)

    def component_a(self):
        return self.file_a

    def component_b(self):
        return self.file_b


class DiffClass(Diff):
    """ Diff of a Class component.

    Represents a changed made to a Class and it is a subclass of Diff.

    Attributes:
        file_name: String representing the path of the file that the class belongs.
        class_a: String with the name of version A of the Class.
        class_b: String with the name of version B of the Class.
    """

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

    def __repr__(self):
        return "%s class %s,%s in file %s" % (super().__repr__(), self.class_a, self.class_b, self.file_name)

    def component_a(self):
        return self.class_a

    def component_b(self):
        return self.class_b


class DiffMethod(Diff):
    """ Diff of a Method component.

    Represents a change made to a Method and it is a subclass of Diff.

    Attributes:
        file_name: String representing the path of the file that the method belongs.
        class_name: String representing the name of the class that the method belongs.
        method_a: String with the name of version A of the Method.
        method_b: String with the name of version B of the Method.
    """
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

    def __repr__(self):
        return "%s method %s,%s in class %s and file %s" % (super().__repr__(), self.method_a, self.method_b,
                                                            self.class_name, self.file_name)

    def component_a(self):
        return self.method_a

    def component_b(self):
        return self.method_b