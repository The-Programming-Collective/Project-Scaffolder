from classes.schema import Schema

class Directory(Schema):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def remove(self, child: Schema) -> None:
        self.children.remove(child)

    def print_structure(self, level=0):
        print(" " * level, self.name, "->")
        for child in self.children:
            child.print_structure(level + 1)
    
    def __iter__(self):
        return iter(self.children)
