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

directory_path = "backend/templates/flask-template"
context = {'variable_name': 'value'}
project_structure_with_jinja = traverse_directory_with_jinja(directory_path, context)
project_structure_json_with_jinja = json.dumps(project_structure_with_jinja, indent=4)
print(project_structure_json_with_jinja)
