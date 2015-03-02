from parsing.abstract_parser import AbstractParser
import plyj.parser as plyj
from plyj.model import MethodDeclaration, ConstructorDeclaration
import difflib
from pyparsing import *
from repository import *

plyj_parser = plyj.Parser()

#TODO: Detect functions overloading
class JavaParser(AbstractParser):
    @staticmethod
    def parse(code):
        global plyj_parser
        tree = plyj_parser.parse_string(code)
        classes = {}
        for class_declaration in tree.type_declarations:
            functions = {}
            for function_declaration in class_declaration.body:
                if isinstance(function_declaration, MethodDeclaration) or isinstance(function_declaration, ConstructorDeclaration):
                    functions[function_declaration.name] = Function(function_declaration.name)
            classes[class_declaration.name] = Class(class_declaration.name, functions)
        return classes

    #TODO: Parse complete method
    @staticmethod
    def extract_method(class_name, method_name, code):
        class_syntax = originalTextFor(Literal("class " + class_name) + Regex("[^{}]*") + nestedExpr('{', '}'))
        extracted_code = class_syntax.searchString(code)[0][0]
        method_syntax = originalTextFor(Literal(method_name) + Regex("[^{}]*") + nestedExpr('{', '}'))
        extracted_code = method_syntax.searchString(extracted_code)[0][0]
        return extracted_code

    #TODO: Detect renamings
    @staticmethod
    def diff(file_name, source_a, source_b):
        components_a = JavaParser.parse(source_a)
        components_b = JavaParser.parse(source_b)
        diffs = []

        classes_a = set(components_a.keys())
        classes_b = set(components_b.keys())
        classes_added = classes_b - classes_a
        classes_removed = classes_a - classes_b
        classes_same = classes_a & classes_b

        for _class in classes_added:
            diffs.append(DiffClass(file_name=file_name, class_b=_class, added=True))

        for _class in classes_removed:
            diffs.append(DiffClass(file_name=file_name, class_a=_class, removed=True))

        for _class in classes_same:
            class_is_modified = False
            class_a = components_a[_class]
            class_b = components_b[_class]
            functions_a = set(class_a.functions.keys())
            functions_b = set(class_b.functions.keys())
            functions_added = functions_b - functions_a
            functions_removed = functions_a - functions_b
            functions_same = functions_a & functions_b

            for function in functions_added:
                diffs.append(DiffMethod(file_name=file_name, class_name=_class, added=True, method_b=function))

            for function in functions_removed:
                diffs.append(DiffMethod(file_name=file_name, class_name=_class, removed=True, method_a=function))

            class_is_modified = len(functions_added | functions_removed) > 0

            for function in functions_same:
                code_a = JavaParser.extract_method(_class, function, source_a)
                code_b = JavaParser.extract_method(_class, function, source_b)
                functions_is_modified = difflib.SequenceMatcher(None, code_a, code_b).ratio() != 1.0
                if functions_is_modified:
                    class_is_modified = True
                    diffs.append(DiffMethod(file_name=file_name, class_name=_class, modified=True, method_a=function, method_b=function))
            if class_is_modified:
                diffs.append(DiffClass(file_name=file_name, class_a=_class, class_b=_class, modified=True))
        return diffs