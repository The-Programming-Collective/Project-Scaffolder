# Generates JSON template from existing project and renders jinja if any jinja code exists

from jinja2 import Template
import json, os, ast

class TemplateEngine:
    def __init__(self) -> None:
        self.templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        
    def traverse_directory(self, directory_path):
        project_structure = {}

        for root, dirs, files in os.walk(directory_path):
            relative_path = os.path.relpath(root, directory_path)
            if relative_path == ".":
                relative_path = ""

            current_level = project_structure
            if relative_path:
                for part in relative_path.split(os.sep):
                    current_level = current_level.setdefault(part, {})

            for d in dirs:
                current_level[d] = {}

            for f in files:
                with open(os.path.join(root, f), "r") as file:
                    file_content = file.read()
                    current_level[f] = file_content

        return project_structure
    
    def generate_template(self, directory_path : str):
        project_structure = self.traverse_directory(directory_path)
        project_structure_json = json.dumps(project_structure, indent=4)
        return project_structure_json

    def read_jinja_files(self, files_names, *args):
        path = os.path.join(self.templates_dir, *args)
        tree = {}

        try:
            for entry in os.scandir(path):
                if entry.is_file() and entry.name.split('.')[0] in files_names:
                    with open(entry.path, "r") as file:
                        tree[entry.name] = file.read()
        except Exception as e:
            print(e)
            return {"error": "Permission denied"}

        return tree

    # request = {
    #    "projectName": "test",
    #    "backend": "flask",
    #    "backend_dependencies": ["swagger"],
    #    "frontend": "react",
    #    "frontend_dependencies": ["react-router-dom", "axios"],
    # }

    # def render_template(self, request : dict) -> dict:
    #     root_dir = os.path.dirname(os.path.realpath(__file__))
    #     file_content = open(os.path.join(root_dir, 'templates', 'backend', request["backend"], request["backend"] + '.json')).read()
    #     temp = Template(file_content)

    #     deps_json = {}
    #     for dep in request["backendDeps"]:
    #         content = open(os.path.join(root_dir, 'templates', 'backend', request["backend"], 'dependencies',dep+'.json')).read()
    #         content = json.loads(content)
    #         deps_json[dep] = content

    #     deps_string = ""
    #     config_string = ""
    #     imports_string = ""

    #     for dep in deps_json:
    #         deps_string += deps_json[dep]["name"] + " = " + "\\\"" + deps_json[dep]["version"] + "\\\"" + "\\" + "n"
    #         config_string += deps_json[dep]["appConfig"] + "\\" + "n"
    #         imports_string += deps_json[dep]["mainImports"] + "\\" + "n"

    #     context = {'projectName' : request["projectName"], 'poetryDependencies' : deps_string, 'appConfig' : config_string, 'mainImports' : imports_string}
    #     # print(temp.render(context))
    #     return ast.literal_eval(temp.render(context))

    
    def render_template(self, request : dict) -> dict:
        backend_dependencies = self.read_jinja_files(request["backend_dependencies"],'backend', request["backend"], 'dependencies')
        frontend_dependencies = self.read_jinja_files(request["frontend_dependencies"], 'frontend', request["frontend"], 'dependencies')

        backend_template = Template(self.read_jinja_files([request["backend"]], 'backend', request["backend"]).popitem()[1])
        frontend_template = Template(self.read_jinja_files([request["frontend"]], 'frontend', request["frontend"]).popitem()[1])
        
        backend_context = {}
        backend_context["dependencies"] = backend_dependencies
        # for javaee 
        backend_context["groupId"] = "scaffold"
        
        frontend_context = {}
        frontend_context["dependencies"] = frontend_dependencies
        
        backend = ast.literal_eval(backend_template.render(backend_context))
        frontend = ast.literal_eval(frontend_template.render(frontend_context))
        
        master = {}
        master["projectName"] = request["projectName"]
        master["backend"] = backend
        master["frontend"] = frontend
        master["README"] = "This is a test README file"

        return master