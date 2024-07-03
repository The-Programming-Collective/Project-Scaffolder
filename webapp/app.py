import os
from flask import Flask, Response, jsonify, render_template, request
from controllers.file_system import FileSystem
from controllers.project_manager import ProjectManager

app = Flask(__name__)
filesystem = FileSystem()
project_manager = ProjectManager()
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
app.config["UPLOAD_EXTENSIONS"] = [".zip", ".rar"]
app.config["TEMP_PATH"] = os.path.join(app.root_path, "temp")
app.config["SUPPORTED_FRAMEWORKS"] = project_manager.get_supported_frameworks()


@app.route("/")
def home():
    return render_template(
        "index.html",
        frameworks=app.config["SUPPORTED_FRAMEWORKS"],
        allowedUploadExtensions=",".join(app.config["UPLOAD_EXTENSIONS"]),
        maxContentLength=app.config["MAX_CONTENT_LENGTH"],
    )


@app.route("/api/upload", methods=["POST"])
def upload_file():
    if not filesystem.allowed_file(
        request.files["file"].filename, app.config["UPLOAD_EXTENSIONS"]
    ):
        return jsonify({"error": "File type not allowed"}), 400
    return project_manager.get_project_structure(request.files["file"])


@app.route("/api/download", methods=["GET"])
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

if __name__ == "__main__":
    app.run(debug=True)
