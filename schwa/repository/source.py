class Component:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

class File(Component):
    pass

class Class(Component):
    pass

class Function(Component):
    pass
