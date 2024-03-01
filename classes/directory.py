from classes.schema import Schema


class Directory(Schema):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.childern = []

    def add(self, child) -> None:
        self.childern.append(child)

    def remove(self, child: Schema) -> None:
        self.childern.remove(child)

    def print_structure(self, level=0):
        
        print(" " * level, self.name, "->")
        for child in self.childern:
            child.print_structure(level + 1)
