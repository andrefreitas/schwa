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
        file = File(path=path, start_line=tree.start_position.line, end_line=tree.end_position.line)
        JavaParser.traverse_for_classes(granularity, file, tree)
        return file

    @staticmethod
    def traverse_for_lines(granularity, parent, node):

        if hasattr(node, 'children'):
            for child in node.children:
                if isinstance(child, list) and (len(child) > 0):
                    for item in child:
                        JavaParser.traverse_for_lines(granularity, parent, item)
                else:
                    if hasattr(child, 'start_position') and hasattr(child, 'end_position') and \
                        child.start_position != None and child.end_position != None:
                        Line(name=child.start_position.line, start_line=child.start_position.line, end_line=child.end_position.line, parent=parent)

    @staticmethod
    def get_composed_arg_str(type):
        if type.sub_type == None:
            return type.name
        return type.name + "." + JavaParser.get_composed_arg_str(type.sub_type)

    @staticmethod
    def parse_arguments(args):
        str_args = []
        for arg in args:
            if isinstance(arg.type, jl.tree.BasicType):
                str_args.append(arg.type.name)
            elif isinstance(arg.type, jl.tree.ReferenceType):
                str_args.append(JavaParser.get_composed_arg_str(arg.type))
        return "(" + ','.join(str_args) + ")"

    @staticmethod
    def traverse_for_methods(granularity, parent, node):

        p_component = parent

        if isinstance(node, jl.tree.ConstructorDeclaration) or isinstance(node, jl.tree.MethodDeclaration):
            p_component = Method(name=node.name + str(JavaParser.parse_arguments(node.parameters)),
                start_line=node.start_position.line, end_line=node.end_position.line, parent=parent)

            if granularity == Granularity.LINE:
                # Method's declaration line
                Line(name=p_component.start_line, start_line=p_component.start_line, end_line=p_component.end_line, parent=p_component)
                # Traverse lines of this method
                JavaParser.traverse_for_lines(granularity, p_component, node)

        elif isinstance(node, jl.tree.ClassDeclaration):
            if parent.name != node.name:
                # Do not go any futher as any further method is a method of an
                # inner/anonymous class
                return

        elif isinstance(node, jl.tree.ClassCreator): # Anonymous classes
            JavaParser.traverse_for_classes(granularity, p_component, node)

        if hasattr(node, 'children'):
            for child in node.children:
                if isinstance(child, list) and (len(child) > 0):
                    for item in child:
                        JavaParser.traverse_for_methods(granularity, p_component, item)
                else:
                    JavaParser.traverse_for_methods(granularity, p_component, child)

    @staticmethod
    def traverse_for_classes(granularity, parent, node):

        if granularity == Granularity.FILE:
            return

        p_component = parent

        if isinstance(node, (jl.tree.InterfaceDeclaration, jl.tree.ClassDeclaration)):
            p_component = Class(name=node.name, start_line=node.start_position.line, end_line=node.end_position.line, parent=parent)

            if granularity == Granularity.LINE:
                # Class's declaration line
                Line(name=p_component.start_line, start_line=p_component.start_line, end_line=p_component.end_line, parent=p_component)

            if granularity == Granularity.METHOD or granularity == Granularity.LINE:
                # Traverse methods of this class
                JavaParser.traverse_for_methods(granularity, p_component, node)

        if hasattr(node, 'children'):
            for child in node.children:
                if isinstance(child, list) and (len(child) > 0):
                    for item in child:
                        JavaParser.traverse_for_classes(granularity, p_component, item)
                else:
                    JavaParser.traverse_for_classes(granularity, p_component, child)


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
        for method_b in methods_added:
            diffs.append(DiffMethod(parent=method_b.parent, method_b=method_b, added=True))
        for method_a in methods_removed:
            diffs.append(DiffMethod(parent=method_a.parent, method_a=method_a, removed=True))
        for method_a in methods_modified:
            # find version_b
            method_b = None
            for m_b in methods_b:
                if m_b.name == method_a.name:
                    method_b = m_b
                    break
            assert method_b != None
            diffs.append(DiffMethod(parent=method_b.parent, method_a=method_a, method_b=method_b, modified=True))

        # Class granularity differences
        classes_changed_a = set(c for c in changed_a if isinstance(c, Class))
        classes_changed_b = set(c for c in changed_b if isinstance(c, Class))
        classes_a = parsed_file_a.get_classes()
        classes_b = parsed_file_b.get_classes()
        classes_added = classes_b - classes_a
        classes_removed = classes_a - classes_b
        classes_modified = (classes_changed_a | classes_changed_b) - (classes_added | classes_removed)
        for class_b in classes_added:
            diffs.append(DiffClass(parent=class_b.parent, class_b=class_b, added=True))
        for class_a in classes_removed:
            diffs.append(DiffClass(parent=class_a.parent, class_a=class_a, removed=True))
        for class_a in classes_modified:
            # find version_b
            class_b = None
            for c_b in classes_b:
                if c_b.name == class_a.name:
                    class_b = c_b
                    break
            assert class_b != None
            diffs.append(DiffClass(parent=class_b.parent, class_a=class_a, class_b=class_b, modified=True))

        lines_changed_a = set(c for c in changed_a if isinstance(c, Line))
        lines_changed_b = set(c for c in changed_b if isinstance(c, Line))
        lines_a = parsed_file_a.get_lines()
        lines_b = parsed_file_b.get_lines()
        lines_added = lines_b - lines_a
        lines_removed = lines_a - lines_b
        lines_modified = (lines_changed_a | lines_changed_b) - (lines_added | lines_removed)
        for line_b in lines_added:
            diffs.append(DiffLine(parent=line_b.parent, line_b=line_b, added=True))
        for line_a in lines_removed:
            diffs.append(DiffLine(parent=line_a.parent, line_a=line_a, removed=True))
        for line_a in lines_modified:
            # find version_b
            line_b = None
            for l_b in lines_b:
                if l_b.name == line_a.name:
                    line_b = l_b
                    break
            assert line_b != None
            diffs.append(DiffLine(parent=line_b.parent, line_a=line_a, line_b=line_b, modified=True))

        return diffs