import json
import os
from flask import Flask, jsonify, render_template, current_app, request
from jinja2 import Template,Environment ,FileSystemLoader
import shutil
from classes.directory import Directory
from classes.file import File
from util import randomword,getFrameworks

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html",data=getFrameworks())


@app.route("/download", methods=["GET"])
def download_file():
    # os.mkdir(directory_path)
    # file_path = os.path.join(directory_path, "test.txt")
    # file_writer = open(file_path, "w")
    # file_writer.write("Hello World")
    # file_writer.close()
    randName = randomword(10)
    test = Directory(randName)
    test.add(Directory("myroot"))
    testActual = test.children[0]
    testActual.add(File("file1.txt"))
    testActual.add(File("file2.txt"))
    testActual.add(Directory("dir1"))
    testActual.add(Directory("dir2"))
    testActual.children[2].add(File("file3.txt"))
    testActual.children[2].add(Directory("dir3"))
    testActual.children[2].children[1].add(File("file4"))
    testActual.children[2].children[1].add(File("file5"))

    directory_path = os.path.join(app.root_path, "temp", test.name)
    test.create(directory_path)

    # Zip file
    target_path = os.path.join(app.root_path, "temp", test.name)
    file_path = shutil.make_archive(target_path, "zip", directory_path)
    file_handle = open(target_path + ".zip", "rb")

    # This *replaces* the `remove_file` + @after_this_request code above
    def stream_and_remove_file():
        yield from file_handle
        file_handle.close()
        shutil.rmtree(directory_path)
        os.remove(file_path)

    return current_app.response_class(
        stream_and_remove_file(),
        headers={
            "Content-Disposition": "attachment",
            "filename": "test.txt",
            "Content-Type": "application/zip",
        },
    )

def render_schema_template(schema, project_name):
    # Jinja template string
    template_str = """
    {
      "name": "{{ schema.name }}",
      "children": [
        {% for entry in schema.children %}
        {
            "name": "{{ entry.name }}",
            {% if entry.children %}
            "children": [
                {% for subitem in entry.children %}
                    {
                    "name": "{{ subitem.name }}",
                    {% if subitem.children %}
                        "children": [
                        {% for file_item in subitem.children %}
                            {
                            "name": "{{ file_item.name }}",
                            "content": "{{ file_item.content }}"
                            }{% if not loop.last %},{% endif %}
                        {% endfor %}
                        ]
                    {% else %}
                    "content": "{{ subitem.content }}"
                    {% endif %}
                }{% if not loop.last %},{% endif %}
            {% endfor %}
            ]
            {% else %}
            "content": "{{ entry.content }}"
            {% endif %}
        }{% if not loop.last %},{% endif %}
        {% endfor %}
      ]
    }
    """

    # Create a Jinja template
    template = Template(template_str)

    # Render the template with the provided schema and project name
    rendered_template = template.render(schema=schema, projectName=project_name)

    return rendered_template

# New method to render the HTML
def render_html_template(rendered_schema, project_name):

    templates_path = os.path.join(os.path.dirname(__file__), 'templates')

    env = Environment(loader=FileSystemLoader(templates_path))

    html_template = env.get_template("schema.html")

    # Render the HTML template with the provided data
    rendered_html = html_template.render(projectName=project_name, renderedSchema=rendered_schema)

    return rendered_html

#{
    # "projectName" : "MERN Project",
    # "frontend" : "react",
    # "backend" : "node",
    # "database" : "mongo",  
    # "description" : "A simple MERN stack project"
#}

# Function to load JSON files from specified subdirectories
def load_json_files(directory_path, stack_names):
    json_files = {}
    for stack in stack_names:
        stack_path = os.path.join(directory_path, stack)
        if os.path.isdir(stack_path):
            for file in os.listdir(stack_path):
                if file.endswith(".json"):
                    file_path = os.path.join(stack_path, file)
                    with open(file_path, 'r') as f:
                        file_content = json.load(f)
                        json_files[stack] = file_content
                    break  # Only process one JSON file per subdirectory
    return json_files

@app.route('/generate_project', methods=['POST'])
def generate_project():
    try:
        # Get the JSON object from the request
        stack_info = request.json
        required_keys = ["projectName","frontend", "backend", "database"]
        if not all(key in stack_info for key in required_keys):
            return jsonify({"error": "Input JSON must contain frontend, backend, database"}), 400

        # Extract stack names
        projectName = stack_info["projectName"]
        frontend = stack_info["frontend"]
        backend = stack_info["backend"]
        database = stack_info["database"]
        
        stack_names = [frontend, backend, database]

        # Load JSON files from the stacks directory
        REPO_DIR = 'stacks'
        json_files = load_json_files(REPO_DIR, stack_names)

        # Ensure all required stacks are found
        if not all(stack in json_files for stack in stack_names):
            return jsonify({"error": "One or more stacks not found"}), 404

        # Construct the project JSON structure
        project_structure = {
            projectName: {
                "backend": json_files.get(backend, {}),
                "frontend": json_files.get(frontend, {}),
                "README": json_files.get(database, {}).get("README", "")
            }
        }

        return jsonify(project_structure)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)