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
import plyj.parser as plyj
from plyj.model import *
from plyj.parser import *
from .abstract_parser import AbstractParser
from schwa.repository import *

parser = None


class JavaParser(AbstractParser):
    """ A Java Parser.

    It parses Java Code using Plyj.
    """

    @staticmethod
    def parse(code):
        """ Parses Java code.

        Uses a modified version of Plyj (line annotations) to parse Java.

        Args:
            code: A string of Java code.

        Returns:
            A File instance.

        Raises:
            ParsingError: When the source code is not valid Java.
        """
        global parser
        if not parser:
            parser = plyj.Parser()
        tree = parser.parse_string(code)
        tree.body = tree.type_declarations
        classes = JavaParser.parse_tree(tree)
        _file = File()
        _file.classes = classes
        return _file

    @staticmethod
    def parse_tree(tree):
        """ Parses a tree recursively.

        It iterates trough methods and parses nested classes and methods.

        Args:
            tree: A tree parsed from plyj.

        Returns:
            A list of Components, that can be nested Classes and Methods.
        """

        # Child classes
        child_classes = []
        for declaration in tree.body:
            if isinstance(declaration, ClassDeclaration):
                components = JavaParser.parse_tree(declaration)
                child_classes.append(components)

        # Is a class
        if isinstance(tree, ClassDeclaration):
            class_component = Class(name=tree.name, start_line=tree.start_line, end_line=tree.end_line)
            for declaration in tree.body:
                if isinstance(declaration, (MethodDeclaration, ConstructorDeclaration)):
                    method = declaration
                    method_component = Method(name=method.name, start_line=method.start_line, end_line=method.end_line)
                    class_component.methods.append(method_component)
            class_component.classes.extend(child_classes)
            return class_component
        else:
            return child_classes


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
    def diff(file_a, file_b):
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
            parsed_file_a = JavaParser.parse(source_a)
            parsed_file_b = JavaParser.parse(source_b)
        except ParsingError:
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
        methods_changed_a = set(c for c in changed_a if isinstance(c, tuple))
        methods_changed_b = set(c for c in changed_b if isinstance(c, tuple))
        methods_a = parsed_file_a.get_functions_set()
        methods_b = parsed_file_b.get_functions_set()
        methods_added = methods_b - methods_a
        methods_removed = methods_a - methods_b
        methods_modified = (methods_changed_a | methods_changed_b) - (methods_added | methods_removed)
        for c, m in methods_added:
            diffs.append(DiffMethod(file_name=path_b, class_name=c, method_b=m, added=True))
        for c, m in methods_removed:
            diffs.append(DiffMethod(file_name=path_b, class_name=c, method_a=m, removed=True))
        for c, m in methods_modified:
            diffs.append(DiffMethod(file_name=path_b, class_name=c, method_a=m, method_b=m, modified=True))

        # Class granularity differences
        classes_changed_a = set(c for c in changed_a if isinstance(c, str))
        classes_changed_b = set(c for c in changed_b if isinstance(c, str))
        classes_a = parsed_file_a.get_classes_set()
        classes_b = parsed_file_b.get_classes_set()
        classes_added = classes_b - classes_a
        classes_removed = classes_a - classes_b
        classes_modified = (classes_changed_a | classes_changed_b) - (classes_added | classes_removed)
        for c in classes_added:
            diffs.append(DiffClass(file_name=path_b, class_b=c, added=True))
        for c in classes_removed:
            diffs.append(DiffClass(file_name=path_b, class_a=c, removed=True))
        for c in classes_modified:
            diffs.append(DiffClass(file_name=path_b, class_a=c, class_b=c, modified=True))

        return diffs