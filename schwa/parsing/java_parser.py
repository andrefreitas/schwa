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
from .abstract_parser import AbstractParser
from schwa.repository import *


class JavaParser(AbstractParser):
    """ A Java Parser.

    It parses Java Code using regexs since it's faster.
    """

    @staticmethod
    def parse(code):
        """ Parses Java code.

        Iterates over the lines to parse components a return a list of components with their start and end line.
        For example: [[9, 11, 'API', 'getUrl'], [13, 15, 'API', 'setUrl']].

        Args:
            code: A string representing Java source code.

        Returns:
            A list of lists that have the start and end line for each component.
        """

        components = []

        """ Regular Expressions to evaluate if a line is a class, function, etc """
        class_re = re.compile("(class)\s+([a-zA-Z0-1]+)")
        comment_re = re.compile("^\s*((\/\/)|(\/\*\*)|(\*\/)|(\*))")
        function_re = re.compile("(static|private|protected|public)\s+([^(){}]*\s+)?([a-zA-Z0-1\s]+)\s*\([^(){}]*\)\s*{?\s*$")
        closing_bracket_re = re.compile("}\s*$")
        open_bracket_re = re.compile("{")
        close_bracket_re = re.compile("}")

        """ Helpers for line scanning """
        current_class = None
        current_method = None
        last_closing_bracket_number = None
        penultimate_closing_bracket_number = None
        lines = code.split("\n")
        line_count = len(lines)
        line_counter = 0
        open_brackets_counter = 0
        close_brackets_counter = 0

        for line in lines:
            line_counter += 1

            # Is a comment
            if comment_re.search(line):
                continue

            # Is a class
            search = class_re.search(line)
            if search:
                if current_class:
                    current_class[1] = last_closing_bracket_number
                if current_method:
                    current_method[1] = penultimate_closing_bracket_number
                    components.append(current_method)
                    current_method = None
                current_class = [line_counter, 0, search.group(2)]
                open_brackets_counter = 0 if open_bracket_re.search(line) else -1
                close_brackets_counter = 0
                continue

            # Is a function
            search = function_re.search(line)
            if search:
                # Evaluate if is pending closing a function declaration
                if open_brackets_counter == close_brackets_counter:
                    if current_method:
                        current_method[1] = last_closing_bracket_number
                        components.append(current_method)
                    current_method = [line_counter, 0, current_class[2], search.group(3)]
                    open_brackets_counter = 0
                    close_brackets_counter = 0

            # Is a closing bracket
            search = closing_bracket_re.search(line)
            if search:
                penultimate_closing_bracket_number = last_closing_bracket_number
                last_closing_bracket_number = line_counter

            # Is last line
            if line_count == line_counter:
                if current_class:
                    current_class[1] = last_closing_bracket_number
                if current_method:
                    components.append(current_method)
                    current_method[1] = penultimate_closing_bracket_number

            # Brackets
            if open_bracket_re.search(line):
                open_brackets_counter += 1
            if close_bracket_re.search(line):
                close_brackets_counter += 1

        return components

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

        By giving files paths and source code, outputs Diffs instances at the Class and Method granularity.

        Args:
            file_a: A tuple with (File Path, Source Code) of version A.
            file_b: A tuple with (File Path, Source Code) of version B.

        Returns:
            A list of Diff instances.
        """

        path_a, source_a = file_a
        path_b, source_b = file_b
        diffs = []
        components_a = JavaParser.parse(source_a)
        components_b = JavaParser.parse(source_b)
        changed_a = set()
        changed_b = set()
        changed_sequences = JavaParser.extract_changed_sequences(source_a, source_b)

        for operation, start_line, end_line in changed_sequences:
            if operation == "-":
                for start1, end1, class_name, function_name in components_a:
                    if (start_line >= start1 and start_line <= end1) or (end_line >= start1 and end_line <= end1):
                        changed_a.add((class_name, function_name))
            if operation == "+":
                for start1, end1, class_name, function_name in components_b:
                    if (start_line >= start1 and start_line <= end1) or (end_line >= start1 and end_line <= end1):
                        changed_b.add((class_name, function_name))

        # Method granularity
        methods_a = set((c, f) for _, _, c, f in components_a)
        methods_b = set((c, f) for _, _, c, f in components_b)
        methods_added = methods_b - methods_a
        methods_removed = methods_a - methods_b
        methods_modified = (changed_a | changed_b) - (methods_added | methods_removed)


        for c, m in methods_added:
            diffs.append(DiffMethod(file_name=path_b, class_name=c, method_b=m, added=True))
        for c, m in methods_removed:
            diffs.append(DiffMethod(file_name=path_b, class_name=c, method_a=m, removed=True))
        for c, m in methods_modified:
            diffs.append(DiffMethod(file_name=path_b, class_name=c, method_a=m, method_b=m, modified=True))

        # Class granularity
        classes_a = set(c for _, _, c, _ in components_a)
        classes_b = set(c for _, _, c, _ in components_b)
        classes_added = classes_b - classes_a
        classes_removed = classes_a - classes_b
        classes_modified = (classes_a & classes_b) & (set(c for c, f in methods_added) | set(c for c, f in methods_removed) | set(c for c, f in methods_modified))

        for c in classes_added:
            diffs.append(DiffClass(file_name=path_b, class_b=c, added=True))
        for c in classes_removed:
            diffs.append(DiffClass(file_name=path_b, class_a=c, removed=True))
        for c in classes_modified:
            diffs.append(DiffClass(file_name=path_b, class_a=c, class_b=c, modified=True))

        return diffs