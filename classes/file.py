from classes.schema import Schema


class File(Schema):

    def __init__(self, name) -> None:
        super().__init__(name)
        self.type = ""
        self.content = ""

    def print_structure(self, level=0):
        print(" " * level, self.name, f"({self.type})" if self.type else "")

    def print_content(self):
        print(self.content)

    def set_content(self, content: str):
        self.content = content
