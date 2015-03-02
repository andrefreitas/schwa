class File:
    def __init__(self, path, classes):
        self.path = path
        self.classes = classes


class Class:
    def __init__(self, name, functions):
        self.name = name
        self.functions = functions


class Function:
    def __init__(self, name):
        self.name = name