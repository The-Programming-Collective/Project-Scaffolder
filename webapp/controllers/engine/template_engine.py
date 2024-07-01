# Generates JSON template from existing project and renders jinja if any jinja code exists

from jinja2 import Template
import json, os, ast

class TemplateEngine:

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
                with open(os.path.join(root, f), 'r') as file:
                    file_content = file.read()
                    current_level[f] = file_content

        return project_structure

    def generate_template(self, framework_name : str) -> dict: 
        directory_path =  "webapp/controllers/engine/templates/backend/" + framework_name
        project_structure = self.traverse_directory(directory_path)
        project_structure_json = json.dumps(project_structure, indent=4)
        return project_structure_json


    # request = {
    #    "projectName": "test",
    #     "backend": "flask",
    #     "backendDeps": ["swagger"],
    #     "frontend": "react",
    # }

    def render_template(self, request : dict) -> dict:
        root_dir = os.path.dirname(os.path.realpath(__file__))
        file_content = open(os.path.join(root_dir, 'templates', 'backend', request["backend"], request["backend"] + '.json')).read()
        temp = Template(file_content)

        deps_json = {}
        for dep in request["backendDeps"]:
            content = open(os.path.join(root_dir, 'templates', 'backend', request["backend"], 'dependencies',dep+'.json')).read()
            content = json.loads(content)
            deps_json[dep] = content

        deps_string = ""
        config_string = ""
        imports_string = ""

        for dep in deps_json:
            deps_string += deps_json[dep]["name"] + " = " + "\\\"" + deps_json[dep]["version"] + "\\\"" + "\\" + "n"
            config_string += deps_json[dep]["appConfig"] + "\\" + "n"
            imports_string += deps_json[dep]["mainImports"] + "\\" + "n"

        context = {'projectName' : request["projectName"], 'poetryDependencies' : deps_string, 'appConfig' : config_string, 'mainImports' : imports_string}
        # print(temp.render(context))
        return ast.literal_eval(temp.render(context))
