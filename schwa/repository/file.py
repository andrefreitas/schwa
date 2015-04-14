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

""" A module for representing software components. """


class File:
    """A class for representing a file structure.

    A file can contain classes or functions.

    Attributes:
        path: An optional string that is the file path.
        classes: An optional list of Class instances.
        functions: An optional list of Function instances.
    """
    def __init__(self, path=None):
        self.path = path
        self.classes = []
        self.functions = []

    def get_components_hit(self, start_line, end_line):
        """Returns a set of components that got hit by the range.

        By comparing the line numbers, obtains the affected components of start and end line.

        Args:
            start_line: A number with the start line.
            end_line: A number with the end line.

        Returns:
            A set of tuples that are classes, methods or functions. E.g. {(API), (API, main), (API.Core), (,login)}.
        """

        components = set()
        for _class in self.classes:
            components = components | _class.get_components_hit(start_line, end_line)
        for function in self.functions:
            if function.range_hit(start_line, end_line):
                components.add(("", function.name))
        return components

    def get_classes_set(self):
        """ Get the set of classes names.

        It uses dot notation for nested classes.

        Returns:
            A set of classes names. E.g. {(API), (API.Core)}
        """
        classes = set()
        for _class in self.classes:
            classes = classes | _class.get_classes_set()
        return classes

    def get_functions_set(self):
        """ Get the set of functions names.

        Remember that a class function is called method. Functions have an empty string
        for the parent class.

        Returns:
            A set of functions names. E.g. {(, main), (API, login)}
        """
        functions = set()
        for function in self.functions:
            functions.add(('', function.name))
        for _class in self.classes:
            functions = functions | _class.get_methods_set()
        return functions


class Component:
    """A class for representing a generic Software component.

    A component can be a Class, Method or Function.

    Attributes:
        name: A string with the name of the component.
        start_line: A number with the line number of the beginning of the component.
        end_line: A number with the line number of the end of the component.
    """
    def __init__(self, name, start_line, end_line):
        self.name = name
        self.start_line = start_line
        self.end_line = end_line

    def __repr__(self):
        return "%s<%i,%i>" % (self.name, self.start_line, self.end_line)

    def range_hit(self, start_line, end_line):
        return self.start_line <= start_line <= self.end_line or self.start_line <= end_line <= self.end_line


class Class(Component):
    """A class for representing a Class structure.

    It can have nested classes and methods and it is a subclass of Component.

    Attributes:
        methods: A list of Methods instances.
        classes: A list of Classes instances.
    """
    def __init__(self, name, start_line, end_line):
        super().__init__(name, start_line, end_line)
        self.methods = []
        self.classes = []

    def get_components_hit(self, start_line, end_line, parent_classes=None):
        """Returns a set of components that got hit by the range.

        By comparing the line numbers, obtains the affected components of start and end line.

        Args:
            start_line: A number with the start line.
            end_line: A number with the end line.
            parent_classes: A list of parent classes to use dot notation for nested classes.

        Returns:
            A set of tuples that are classes or methods. E.g. {(API), (API, main), (API.Core), (API.Core,login)}
        """
        if parent_classes is None:
            parent_classes = []
        components = set()
        class_id = ".".join(parent_classes + [self.name])
        if self.range_hit(start_line, end_line):
            components.add(class_id)
        components = components.union([(class_id, m.name) for m in self.methods if m.range_hit(start_line, end_line)])
        for _class in self.classes:
            components = components.union(_class.get_components_hit(start_line, end_line, parent_classes + [self.name]))
        return components

    def get_classes_set(self, parent_classes=None):
        """ Get the set of classes names.

        It uses dot notation for nested classes.

        Args:
            parent_classes: An optional list of parent classes names for dot notation.

        Returns:
            A set of classes names. E.g. {(API), (API.Core)}
        """
        if parent_classes is None:
            parent_classes = []
        classes = set()
        class_id = ".".join(parent_classes + [self.name])
        classes.add(class_id)
        for _class in self.classes:
            classes = classes | _class.get_classes_set(parent_classes + [self.name])
        return classes

    def get_methods_set(self, parent_classes=None):
        """ Get the set of methods names.

        It uses dot notation for nested classes.

        Args:
            parent_classes: An optional list of parent classes names for dot notation.

        Returns:
            A set of methods and parent classes names. E.g. {(API, main), (API.Core,login)}
        """
        if parent_classes is None:
            parent_classes = []
        methods = set()
        class_id = ".".join(parent_classes + [self.name])
        for method in self.methods:
            methods.add((class_id, method.name))
        for _class in self.classes:
            methods = methods | _class.get_methods_set(parent_classes + [self.name])
        return methods


class Method(Component):
    """A Method is a member of a class.

    Is basically the same thing as a function but with another meaning. It is
    a subclass of Component.
    """


class Function(Component):
    """A Function component representation.

    It isn't a member of a class but a top level function of a file.
    It is a subclass of Component.

    """