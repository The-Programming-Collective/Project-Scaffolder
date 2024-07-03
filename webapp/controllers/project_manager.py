import os
import shutil

from controllers.engine.template_engine import TemplateEngine
from controllers.file_system import FileSystem


class ProjectManager:
    def __init__(self) -> None:
        self.file_system = FileSystem()
        self.template_engine = TemplateEngine()

    def generate_project(self, project):
        directory_name, directory_path = self.file_system.generate_files(project)
        target_path = os.path.join(self.file_system.tempPath, directory_name)
        file_path = shutil.make_archive(target_path, "zip", directory_path)
        file_handle = open(target_path + ".zip", "rb")
        return file_handle, file_path, directory_path

    def download_project(self, request):
        project = self.template_engine.render_template(request)
        file_handle, file_path, directory_path = self.generate_project(project)
        yield from file_handle
        file_handle.close()
        shutil.rmtree(directory_path)
        os.remove(file_path)

    def get_project_structure(self, zip_file):
        randDir = self.file_system.generate_random_directory()[1]
        file_path = os.path.join(randDir, zip_file.filename)
        dir_path = os.path.join(randDir, zip_file.filename.split(".")[0])
        zip_file.save(file_path)
        self.file_system.extract_zip_file(file_path, dir_path)
        project_structure = self.template_engine.generate_template(dir_path)
        shutil.rmtree(randDir)
        return project_structure
    
    def get_supported_frameworks(self):
        return self.file_system.traverse_directory(
            root="controllers/engine/templates", levels=3
        )
