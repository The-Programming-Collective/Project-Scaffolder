from classes.schema import Schema


class File(Schema):

    def __init__(self, name) -> None:
        super().__init__(name)
        self.content = ""

    def print_structure(self, level=0):
        print(" " * level, self.name)

    def print_content(self):
        print(self.content)

    def set_content(self, content: str):
        self.content = content
        
    def create(self,path):
        file_writer = open(path, "w")
        file_writer.write(self.content)
        file_writer.close()
