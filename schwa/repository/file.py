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

import sys


class Component:
    """A class for representing a generic Software component. A component can be
    a Class, Method, Function, or a Line.

    Attributes:
        name: A string with the name of the component.
        start_line: A number with the line number of the beginning of the component.
        end_line: A number with the line number of the end of the component.
        parent: An optional parent Component instance.
    """

    def __init__(self, name, start_line, end_line, parent=None):
        self.name = name
        self.start_line = start_line
        self.end_line = end_line
        self.parent = parent
        self.components = set()
        if self.parent != None:
            parent.components.add(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__repr__() == other.__repr__()

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        # A class or method/function in different versions but with the same
        # 'fullname', may represent the same class or method/function
        if self.parent == None or isinstance(self.parent, File):
            return str(self.name)
        return str(self.parent.__repr__()) + "." + str(self.name)

    def __str__(self):
        if self.start_line != None and self.end_line != None:
            return "%s<%i,%i>" % (self.name, self.start_line, self.end_line)
        return "%s" % (self.name)

    def range_hit(self, start_line, end_line):
        return self.start_line <= start_line <= self.end_line or self.start_line <= end_line <= self.end_line

    def get_components_hit(self, start_line, end_line):
        """Returns a set of components that got hit by the range.

        By comparing the line numbers, obtains the affected components of start and end line.

        Args:
            start_line: A number with the start line.
            end_line: A number with the end line.

        Returns:
            A set of classes, methods, functions, and/or lines in the given range.
        """
        components_hit = set()
        for component in self.components:
            if component.range_hit(start_line, end_line):
                components_hit.add(component)
                # and all components within start_line and end_line
                components_hit.update(component.get_components_hit(start_line, end_line))
        return components_hit

    def __get_components_of_type(self, type):
        comps = set()
        for component in self.components:
            if isinstance(component, type):
                comps.add(component)
        return comps

    def get_classes(self):
        return self.__get_components_of_type(Class)

    def get_functions(self):
        return self.__get_components_of_type(Function)

    def get_methods(self):
        return self.__get_components_of_type(Method)

    def get_lines(self):
        return self.__get_components_of_type(Line)

    def __get_all_components_of_type(self, type):
        comps = set()
        for component in self.components:
            if isinstance(component, type):
                comps.add(component)
            comps.update(component.__get_all_components_of_type(type))
        return comps

    def get_all_classes(self):
        return self.__get_all_components_of_type(Class)

    def get_all_functions(self):
        return self.__get_all_components_of_type(Function)

    def get_all_methods(self):
        return self.__get_all_components_of_type(Method)

    def get_all_lines(self):
        return self.__get_all_components_of_type(Line)


class File(Component):
    """A class for representing a file structure.

    A file can contain different components, i.e., classes, functions, and lines.
    It is a subclass of Component.

    Attributes:
        path: An optional string that is the file path.
    """

    def __init__(self, path=None, start_line=None, end_line=None):
        super().__init__(path, start_line, end_line)
        self.path = path

    def get_classes(self):
        """ Get the set of classes.

        Returns:
            A set of classes.
        """
        classes = set()
        for component in self.components:
            if isinstance(component, Class):
                classes.add(component)
            classes.update(component.get_all_classes())
        return classes

    def get_functions(self):
        """ Get the set of functions.

        Returns:
            A set of functions.
        """
        functions = set()
        for component in self.components:
            if isinstance(component, Function):
                functions.add(component)
            functions.update(component.get_all_functions())
            functions.update(component.get_all_methods())
        return functions

    def get_lines(self):
        """ Get the set of lines of code.

        Returns:
            A set of lines of code.
        """
        lines = set()
        for component in self.components:
            if isinstance(component, Line):
                # lines in a file but not in a function, class, or class' method
                lines.add(line)
            else:
                # lines in a function, class, or class' method
                lines.update(component.get_all_lines())
        return lines


class Class(Component):
    """A class for representing a Class structure.

    It can have nested classes and methods.
    It is a subclass of Component.
    """

    def __init__(self, name, start_line, end_line, parent):
        super().__init__(name, start_line, end_line, parent)

class Function(Component):
    """A Function component representation.

    It is not a member of a class but a top level function of a file.
    It is a subclass of Component.
    """

    def __init__(self, name, start_line, end_line, parent):
        super().__init__(name, start_line, end_line, parent)


class Method(Function):
    """A Method is a member of a class.

    It is, basically, the same thing as a Function but with another meaning.
    It is a subclass of Function.
    """

    def __init__(self, name, start_line, end_line, parent):
        super().__init__(name, start_line, end_line, parent)

class Line(Component):
    """A Line component representation.

    It is a subclass of Component and represents a line of code.
    """

    def __init__(self, name, start_line, end_line, parent):
        super().__init__(name, start_line, end_line, parent)