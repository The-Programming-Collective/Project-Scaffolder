from http.client import HTTPException
from flask import Flask, Response, jsonify, render_template, request
from controllers.file_system import FileSystem
from controllers.project_manager import ProjectManager

app = Flask(__name__)
filesystem = FileSystem()
project_manager = ProjectManager()
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
app.config["UPLOAD_EXTENSIONS"] = [".zip", ".rar"]
app.config["SUPPORTED_FRAMEWORKS"] = project_manager.get_supported_frameworks()
app.config["SUPPORTED_DEPENDENCIES"] = project_manager.get_supported_dependencies(["description", "version"])


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    elif isinstance(e, FileNotFoundError):
        code = 404
    elif isinstance(e, ValueError):
        code = 400
    elif isinstance(e, KeyError):
        code = 404
    elif isinstance(e, TypeError):
        code = 400
    return jsonify(error=str(e)), code

@app.route("/")
def home():
    return render_template(
        "index.html",
        frameworks=app.config["SUPPORTED_FRAMEWORKS"],
        dependencies=app.config["SUPPORTED_DEPENDENCIES"],
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
        "frontend_dependencies": [],
        "containerization": False,
    }
    github = {
        "token":"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", 
        "username":"MainUseless",
        "repo_name":"scaffolding122", 
        "description":"testing 12342",
        "is_private":True
    }
    return Response(
        project_manager.download_project(request,github),
        mimetype="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename={request["projectName"]}.zip'
        },
    )

if __name__ == "__main__":
    app.run(debug=True)
