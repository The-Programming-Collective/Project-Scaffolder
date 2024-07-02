import json
import os
import random
import shutil
import string
from decorators.singleton import singleton


@singleton
class FileSystem:

    def __init__(self) -> None:
        self.rootPath = os.path.join(os.path.dirname(__file__))
        while "app.py" not in os.listdir(self.rootPath):
            self.rootPath = os.path.dirname(self.rootPath)
        os.makedirs(os.path.join(self.rootPath, "temp"), exist_ok=True)

    def get_os_path(self, path):
        split = path.split("/")
        return os.path.join(self.rootPath, *split)

    def allowed_file(self, filename, allowedExtensions):
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in allowedExtensions
        )

    def random_file_name(self, length):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(length))

    def generate_random_directory(self):
        randName = self.random_file_name(10)
        randFilePath = os.path.join(self.rootPath, "temp", randName)
        os.mkdir(randFilePath)
        return randName, randFilePath

    def traverse_directory(self, root, levels=1):
        root = self.get_os_path(root)
        if levels == 0:
            return None

        tree = {}

        try:
            for entry in os.scandir(root):
                if entry.is_dir(follow_symlinks=False):
                    tree[entry.name] = self.traverse_directory(entry.path, levels - 1)
                else:
                    tree[entry.name] = None
        except:
            return {"error": "Permission denied"}

        print(tree)
        return tree

    def generate_files(self, project):
        randName, directory_path = self.generate_random_directory()
        print(type(project))

        def generate_files_recursive(path, project):
            for name, content in project.items():
                if isinstance(content, dict):
                    os.makedirs(os.path.join(path, name), exist_ok=True)
                    generate_files_recursive(os.path.join(path, name), content)
                else:
                    with open(os.path.join(path, name), "w") as file:
                        file.write(content)

        generate_files_recursive(directory_path, project)

        return randName, directory_path

    def generate_project(self, project):
        directory_name, directory_path = self.generate_files(project)

        # project_name = ""
        # for key in project.keys():
        #     project_name = key
        #     break
        target_path = os.path.join(self.rootPath, "temp", directory_name)
        file_path = shutil.make_archive(
            target_path, "zip", directory_path
        )
        file_handle = open(target_path + ".zip", "rb")
        return file_handle, file_path, directory_path

    def download_project(self, project):
        file_handle, file_path, directory_path = self.generate_project(project)
        yield from file_handle
        file_handle.close()
        shutil.rmtree(directory_path)
        os.remove(file_path)
