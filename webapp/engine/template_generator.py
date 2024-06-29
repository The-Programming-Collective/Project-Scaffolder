# Generates JSON template from existing project and renders jinja if any jinja code exists

from jinja2 import Template
import json, os

def process_file_with_jinja(file_content, context):
    template = Template(file_content)
    return template.render(context)

def traverse_directory_with_jinja(directory_path, context):
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
                processed_content = process_file_with_jinja(file_content, context)
                current_level[f] = processed_content

    return project_structure

def generate_template() : 
  directory_path = "webapp/engine/templates/backend/flask"
  context = {'variable_name': 'value'}
  project_structure_with_jinja = traverse_directory_with_jinja(directory_path, context)
  project_structure_json_with_jinja = json.dumps(project_structure_with_jinja, indent=4)
  return project_structure_json_with_jinja


root_dir = os.path.dirname(os.path.realpath(__file__))
file_content = open(os.path.join(root_dir, 'templates','backend','flask','flask.json')).read()
temp = Template(file_content)

deps = ["swagger"]
deps_json = {}
for dep in deps:
     content = open(os.path.join(root_dir, 'templates','backend','flask','dependencies',dep+'.json')).read()
     content = json.loads(content)
     deps_json[dep] = content

deps_string = ""
config_string = ""
imports_string = ""

for dep in deps_json:
    deps_string += deps_json[dep]["name"] + " = " + deps_json[dep]["version"] + "\n"
    config_string += deps_json[dep]["appConfig"] + "\n"
    imports_string += deps_json[dep]["mainImports"] + "\n"

context = {'projectName' : 'test', 'poetryDependencies' : deps_string, 'appConfig' : config_string, 'mainImports' : imports_string}
# print(temp.render(context))
