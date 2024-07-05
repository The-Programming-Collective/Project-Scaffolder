import os
import shutil

from controllers.engine.template_engine import Template_Engine
from controllers.file_system import File_System
from controllers.github import Github


class Project_Manager:
    def __init__(self) -> None:
        self.file_system = File_System()
        self.template_engine = Template_Engine()

    def generate_project(self, project_template):
        try:
            directory_name, directory_path = self.file_system.generate_files(project_template)
            target_path = os.path.join(self.file_system.tempPath, directory_name)
            file_path = shutil.make_archive(target_path, "zip", directory_path)
            file_handle = open(target_path + ".zip", "rb")
            return file_handle, file_path, directory_path
        except Exception as e:
            return False, e.args[0]

    def download_project(self, request, github_info=None):
        try:
            project_template = self.template_engine.render_template(request)
            file_handle, file_path, directory_path = self.generate_project(project_template)
            if github_info:
                github_info["files_path"] = directory_path
                Github(github_info).upload_project()
        except Exception as e:
            if directory_path and os.path.exists(directory_path):
                shutil.rmtree(directory_path)
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            return False, e.args[0]
        
        result = {"file_handle" : file_handle, "file_path": file_path, "directory_path": directory_path}
        return True, result

    def clean_up(self, generator: dict):
        yield from generator["file_handle"]
        generator["file_handle"].close()
        shutil.rmtree(generator["directory_path"])
        os.remove(generator["file_path"])
        
    def get_project_structure(self, zip_file):
        try:
            rand_dir, dir_path = self.file_system.extract_zip_file(zip_file)
            project_structure = self.template_engine.generate_template(dir_path)
            shutil.rmtree(rand_dir)
            return project_structure
        except:
            if os.path.exists(rand_dir):
                shutil.rmtree(rand_dir)
    
    def get_supported_frameworks(self):
        try:
            return self.file_system.traverse_directory(
                root=os.path.join(self.file_system.rootPath,"controllers/engine/templates"), levels=2
            )
        except Exception as e:
            return e.args[0]
        
    def get_supported_stuff(self,desired_keys):
        try:
            dependencies = {}
            all_frameworks = self.get_supported_frameworks()
            for framework_type in all_frameworks:
                dependencies[framework_type] = {}
                for framework_name in all_frameworks[framework_type]:
                    curr_dependencies = self.template_engine.read_jinja_files([],framework_type, framework_name, 'dependencies')
                    dependencies[framework_type][framework_name] = {}
                    for key,value in curr_dependencies.items():
                        temp = {wanted_key: value.get(wanted_key) for wanted_key in desired_keys if wanted_key in value}
                        dependencies[framework_type][framework_name][key] = temp
            return dependencies
        except Exception as e:
            return e.args[0]
