import os
import json
from flask import Flask, Response, jsonify, render_template, current_app, request
from jinja2 import Template,Environment ,FileSystemLoader
from controllers.file_system import FileSystem
from controllers.engine.template_engine import TemplateEngine
from utils import load_json_files

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.zip', '.rar']                                                                   
app.config['TEMP_PATH'] = os.path.join(app.root_path, "temp")
filesystem = FileSystem()

@app.route("/")
def home():
    return render_template("index.html",\
        frameworks=filesystem.getNames(root="controllers/engine/templates",levels=3),\
        allowedUploadExtentions=",".join(app.config['UPLOAD_EXTENSIONS']),\
        maxContentLength=app.config['MAX_CONTENT_LENGTH'])

@app.route("/upload", methods=["POST"])
def upload_file():
    if not filesystem.allowed_file(request.files["file"].filename,app.config['UPLOAD_EXTENSIONS']):
        return jsonify({"error": "File type not allowed"}), 400
    uploaded_file = request.files["file"]
    file_path = os.path.join(app.config['TEMP_PATH'], uploaded_file.filename)
    uploaded_file.save(file_path)
    return jsonify({"message": "File uploaded successfully"})

@app.route("/download", methods=["GET"])
def download_file():
    request = {
        "projectName" : "Testing",
        "backend" : "flask",
        "backendDeps" : ["swagger"]
    }
    return Response(filesystem.download_project(TemplateEngine().render_template(request)), 
        mimetype='application/zip', 
        headers={"Content-Disposition": f'attachment; filename={request["projectName"]}.zip'})

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