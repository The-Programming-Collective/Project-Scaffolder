import json
import os
from flask import Flask, jsonify, render_template, current_app, request
from jinja2 import Template,Environment ,FileSystemLoader
import shutil
from classes.directory import Directory
from classes.file import File
from util import randomword, get_frameworks, allowed_file, load_json_files

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.zip', '.rar']                                                                   
app.config['TEMP_PATH'] = os.path.join(app.root_path, "temp")

@app.route("/")
def home():
    return render_template("index.html",\
        frameworks=get_frameworks(),\
        allowedUploadExtentions=",".join(app.config['UPLOAD_EXTENSIONS']),\
        maxContentLength=app.config['MAX_CONTENT_LENGTH'])

@app.route("/upload", methods=["POST"])
def upload_file():
    if not allowed_file(request.files["file"].filename,app.config['UPLOAD_EXTENSIONS']):
        return jsonify({"error": "File type not allowed"}), 400
    uploaded_file = request.files["file"]
    file_path = os.path.join(app.config['TEMP_PATH'], uploaded_file.filename)
    uploaded_file.save(file_path)
    return jsonify({"message": "File uploaded successfully"})

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



@app.route('/generate_project', methods=['POST'])
def generate_project():
    try:
        # Get the JSON object from the request
        stack_info = request.json
        required_keys = ["projectName", "frontend", "backend", "database"]
        if not all(key in stack_info for key in required_keys):
            return jsonify({"error": "Input JSON must contain projectName, frontend, backend, and database"}), 400

        # Extract stack names
        project_name = stack_info["projectName"]
        frontend = ["frontend", stack_info["frontend"]]
        backend = ["backend", stack_info["backend"]]
        database = ["database", stack_info["database"]]
        
        stack_names = [frontend, backend, database]

        # Load JSON files from the stacks directory
        REPO_DIR = os.path.join(os.path.dirname(__file__), 'engine', 'templates')
        json_files = load_json_files(REPO_DIR, stack_names)

        # Ensure all required stacks are found
        if not all(category in json_files for category, _ in stack_names):
            return jsonify({"error": "One or more stacks not found"}), 404

        # Construct the project JSON structure
        project_structure = {
            project_name: {
                "backend": json_files.get("backend", {}),
                "frontend": json_files.get("frontend", {}),
                "database": json_files.get("database", {})
            }
        }

        return jsonify(project_structure)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
