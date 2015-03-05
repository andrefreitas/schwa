from parsing.abstract_parser import AbstractParser

import difflib
from repository import *
import re


#TODO: Detect functions overloading
class JavaParser(AbstractParser):
    @staticmethod
    def parse(code):
        components = []

        """ Regular Expressions to evaluate if a line is a class, function, etc """
        class_re = re.compile("(class)\s+([a-zA-Z0-1]+)")
        comment_re = re.compile("^\*((\/\/)|(\/\*\*)|(\*\/)|(\*))")
        function_re = re.compile("(public|private|protected)\s+([^(){}]*\s+)?([a-zA-Z0-1\s]+)\s*\([^(){}]*\)\s*{?\s*$")
        closing_bracket_re = re.compile("}\s*$")

        """ Helpers for line scanning """
        current_class = None
        current_method = None
        last_closing_bracket_number = None
        penultimate_closing_bracket_number = None
        lines = code.split("\n")
        line_count = len(lines)
        line_counter = 0

        for line in lines:
            line_counter += 1

            # Is a comment
            if comment_re.search(line):
                continue

            # Is a class
            search = class_re.search(line)
            if search:
                if current_class:
                    current_class[0][1] = last_closing_bracket_number
                if current_method:
                    current_method[0][1] = last_closing_bracket_number
                    components.append(current_method)
                current_class = [[line_counter, 0], search.group(2)]
                continue

            # Is a function
            search = function_re.search(line)
            if search:
                if current_method:
                    current_method[0][1] = last_closing_bracket_number
                    components.append(current_method)
                current_method = [[line_counter, 0], [current_class[1], search.group(3)]]
                continue

            # Is a closing bracket
            search = closing_bracket_re.search(line)
            if search:
                penultimate_closing_bracket_number = last_closing_bracket_number
                last_closing_bracket_number = line_counter

            # Is last line
            if line_count == line_counter:
                if current_class:
                    current_class[0][1] = last_closing_bracket_number
                if current_method:
                    components.append(current_method)
                    current_method[0][1] = penultimate_closing_bracket_number

        return components



    @staticmethod
    def diff(file_a, file_b):
        path_a, source_a = file_a
        path_b, source_b = file_b
        changed_lines = difflib.ndiff(source_a.split("\n"), source_b.split("\n"))

        line_number_a = 0
        line_number_b = 0
        added_re = re.compile("^\+")
        removed_re = re.compile("^-")
        incremental_re = re.compile("^\?")
        changed_sequence = None
        changed_sequences = []

        for line in changed_lines:
            print(line)
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







