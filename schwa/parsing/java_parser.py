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

""" Module for the Java Parser """

import difflib
import re
import javalang as jl
from javalang.parser import JavaSyntaxError
from .abstract_parser import AbstractParser
from schwa.repository import *

parser = None


class JavaParser(AbstractParser):
    """ A Java Parser.

    It parses Java Code using [javalang](https://github.com/c2nes/javalang).
    """

    @staticmethod
    def parse(granularity, path, code):
        """ Parses Java code.

        Args:
            path: Path to the Java code.
            code: A string of Java code.

        Returns:
            A File instance.

        Raises:
            JavaSyntaxError: When the source code is not valid Java.
        """
        tree = jl.parse.parse(code)
        file = File(path)
        JavaParser.parse_tree(granularity, file, tree)
        return file

    @staticmethod
    def parse_tree(granularity, parent, tree):
        """ Finds end line of code of a node (e.g., a class, or method)

        Args:
            A node from javalang.

        Returns:
            End line number of a node.
        """
        def end_line(node):
            max_line = node.position.line

            def find_end_line(node):
                for child in node.children:
                    if isinstance(child, list) and (len(child) > 0):
                        for item in child:
                            find_end_line(item)
                    else:
                        if hasattr(child, '_position'):
                            nonlocal max_line
                            if child._position.line > max_line:
                                max_line = child._position.line
                                return

            find_end_line(node)
            return max_line

        def get_composed_arg_str(type):
            if type.sub_type == None:
                return type.name
            return type.name + "." + get_composed_arg_str(type.sub_type)

        def parse_arguments(args):
            str_args = []
            for arg in args:
                if isinstance(arg.type, jl.tree.BasicType):
                    str_args.append(arg.type.name)
                elif isinstance(arg.type, jl.tree.ReferenceType):
                    str_args.append(get_composed_arg_str(arg.type))
            return "(" + ','.join(str_args) + ")"

        """ Parses a tree recursively.

        It iterates trough classes and parses nested classes, methods, and lines.

        Args:
            parent: An object representing a Component (i.e., File, Class, or Method)
            tree: A tree parsed from javalang.
        """
        def traverse(parent, tree):
            p_component = None
            if isinstance(tree, (jl.tree.InterfaceDeclaration, jl.tree.ClassDeclaration)):
                if granularity == Granularity.CLASS or granularity == Granularity.METHOD or granularity == Granularity.LINE:
                    p_component = Class(name=tree.name, start_line=tree.position.line, end_line=end_line(tree), parent=parent)
            elif isinstance(tree, (jl.tree.ConstructorDeclaration, jl.tree.MethodDeclaration)):
                if granularity == Granularity.METHOD or granularity == Granularity.LINE:
                    p_component = Method(name=tree.name + parse_arguments(tree.parameters), start_line=tree.position.line, end_line=end_line(tree), parent=parent)

            # Line where Class or Method is defined
            if isinstance(tree, (jl.tree.ClassDeclaration, jl.tree.ConstructorDeclaration, jl.tree.MethodDeclaration)):
                if granularity == Granularity.LINE:
                    line_component = Line(name=tree.position.line, start_line=tree.position.line, end_line=tree.position.line, parent=p_component)

            for child in tree.children:
                if isinstance(child, list) and (len(child) > 0):
                    for item in child:
                        traverse(p_component if p_component != None else parent, item)
                else:
                    if hasattr(child, '_position'):
                        if granularity == Granularity.LINE:
                            line_component = Line(name=child._position.line, start_line=child._position.line, end_line=child._position.line, parent=parent)
                        return

        traverse(parent, tree)


    @staticmethod
    def extract_changed_sequences(source_a, source_b):
        """ Extracts sequences of changes.

        It returns a list of sequences changed between source A and source B.
        For example: [["-", 1, 10], ["+", 15, 35], ["-", 100, 110]]

        Args:
            source_a: A string representing Java source of version A.
            source_b: A string representing Java source of version B.

        Returns:
            A list of lists with changed sequences.
        """

        changed_lines = difflib.ndiff(source_a.split("\n"), source_b.split("\n"))
        line_number_a = 0
        line_number_b = 0
        added_re = re.compile("^\+")
        removed_re = re.compile("^-")
        incremental_re = re.compile("^\?")
        changed_sequence = None
        changed_sequences = []

        for line in changed_lines:
            # Added line
            if added_re.search(line):
                if changed_sequence and changed_sequence[0] == "-":
                    changed_sequence[2] = line_number_a
                    changed_sequences.append(changed_sequence)
                    changed_sequence = None

                line_number_b += 1
                if not changed_sequence:
                    changed_sequence = ["+", line_number_b, 0]

            # Removed line
            elif removed_re.search(line):
                if changed_sequence and changed_sequence[0] == "+":
                    changed_sequence[2] = line_number_b
                    changed_sequences.append(changed_sequence)
                    changed_sequence = None

                line_number_a += 1
                if not changed_sequence:
                    changed_sequence = ["-", line_number_a, 0]

            # Incremental or same
            else:
                if changed_sequence and changed_sequence[0] == "+":
                    changed_sequence[2] = line_number_b
                    changed_sequences.append(changed_sequence)
                    changed_sequence = None
                elif changed_sequence and changed_sequence[0] == "-":
                    changed_sequence[2] = line_number_a
                    changed_sequences.append(changed_sequence)
                    changed_sequence = None
                # Same
                if not incremental_re.search(line):
                    line_number_a += 1
                    line_number_b += 1

        return changed_sequences

    @staticmethod
    def diff(granularity, file_a, file_b):
        """ Computes diffs between 2 version of a file.

        By giving files paths and source code, outputs Diffs instances.

        Args:
            file_a: A tuple with (File Path, Source Code) of version A.
            file_b: A tuple with (File Path, Source Code) of version B.

        Returns:
            A list of Diff instances.
        """
        diffs = []
        path_a, source_a = file_a
        path_b, source_b = file_b
        try:
            parsed_file_a = JavaParser.parse(granularity, path_a, source_a)
            parsed_file_b = JavaParser.parse(granularity, path_b, source_b)
        except JavaSyntaxError:
            return diffs
        changed_a = set()
        changed_b = set()
        changed_sequences = JavaParser.extract_changed_sequences(source_a, source_b)

        # Obtain changed components of each version
        for operation, start_line, end_line in changed_sequences:
            if operation == "-":
                changed_a = changed_a | parsed_file_a.get_components_hit(start_line, end_line)
            if operation == "+":
                changed_b = changed_b | parsed_file_b.get_components_hit(start_line, end_line)

        # Method granularity differences
        methods_changed_a = set(c for c in changed_a if isinstance(c, Method))
        methods_changed_b = set(c for c in changed_b if isinstance(c, Method))
        methods_a = parsed_file_a.get_functions()
        methods_b = parsed_file_b.get_functions()
        methods_added = methods_b - methods_a
        methods_removed = methods_a - methods_b
        methods_modified = (methods_changed_a | methods_changed_b) - (methods_added | methods_removed)
        for m in methods_added:
            diffs.append(DiffMethod(parent=m.parent, method_b=m, added=True))
        for m in methods_removed:
            diffs.append(DiffMethod(parent=m.parent, method_a=m, removed=True))
        for m in methods_modified:
            diffs.append(DiffMethod(parent=m.parent, method_a=m, method_b=m, modified=True))

        # Class granularity differences
        classes_changed_a = set(c for c in changed_a if isinstance(c, Class))
        classes_changed_b = set(c for c in changed_b if isinstance(c, Class))
        classes_a = parsed_file_a.get_classes()
        classes_b = parsed_file_b.get_classes()
        classes_added = classes_b - classes_a
        classes_removed = classes_a - classes_b
        classes_modified = (classes_changed_a | classes_changed_b) - (classes_added | classes_removed)
        for c in classes_added:
            diffs.append(DiffClass(parent=c.parent, class_b=c, added=True))
        for c in classes_removed:
            diffs.append(DiffClass(parent=c.parent, class_a=c, removed=True))
        for c in classes_modified:
            diffs.append(DiffClass(parent=c.parent, class_a=c, class_b=c, modified=True))

        lines_changed_a = set(c for c in changed_a if isinstance(c, Line))
        lines_changed_b = set(c for c in changed_b if isinstance(c, Line))
        lines_a = parsed_file_a.get_lines()
        lines_b = parsed_file_b.get_lines()
        lines_added = lines_b - lines_a
        lines_removed = lines_a - lines_b
        lines_modified = (lines_changed_a | lines_changed_b) - (lines_added | lines_removed)
        for l in lines_added:
            diffs.append(DiffLine(parent=l.parent, line_b=l, added=True))
        for l in lines_removed:
            diffs.append(DiffLine(parent=l.parent, line_a=l, removed=True))
        for l in lines_modified:
            diffs.append(DiffLine(parent=l.parent, line_a=l, line_b=l, modified=True))

        return diffs