import os
from flask import Flask, Response, jsonify, render_template, request
from controllers.file_system import FileSystem
from controllers.engine.template_engine import TemplateEngine
from controllers.project_manager import ProjectManager

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
app.config["UPLOAD_EXTENSIONS"] = [".zip", ".rar"]
app.config["TEMP_PATH"] = os.path.join(app.root_path, "temp")
filesystem = FileSystem()
project_manager = ProjectManager()
template_engine = TemplateEngine()


@app.route("/")
def home():
    return render_template(
        "index.html",
        frameworks=filesystem.traverse_directory(
            root="controllers/engine/templates", levels=3
        ),
        allowedUploadExtensions=",".join(app.config["UPLOAD_EXTENSIONS"]),
        maxContentLength=app.config["MAX_CONTENT_LENGTH"],
    )


@app.route("/upload", methods=["POST"])
def upload_file():
    if not filesystem.allowed_file(
        request.files["file"].filename, app.config["UPLOAD_EXTENSIONS"]
    ):
        return jsonify({"error": "File type not allowed"}), 400

    uploaded_file = request.files["file"]
    randFile, randDir = filesystem.generate_random_directory()
    file_path = os.path.join(randDir,uploaded_file.filename)
    uploaded_file.save(file_path)
    filesystem.extract_zip_file(file_path, os.path.join(randDir, uploaded_file.filename.split(".")[0]))
    return (template_engine.generate_template(os.path.join(randDir, uploaded_file.filename.split(".")[0])))
    return jsonify({"message": "File uploaded successfully"})


@app.route("/download", methods=["GET"])
def generate_project():
    request = {
        "projectName": "Testing",
        "backend": "javaee10",
        "backend_dependencies": ["junit"],
        "frontend": "react",
        "frontend_dependencies": []
    }
    return Response(
        project_manager.download_project(request),
        mimetype="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename={request["projectName"]}.zip'
        },
    )


# {
# "projectName" : "MERN Project",
# "frontend" : "react",
# "backend" : "node",
# "database" : "mongo",
# "description" : "A simple MERN stack project"
# }

if __name__ == "__main__":
    app.run(debug=True)
