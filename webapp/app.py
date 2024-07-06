from http.client import HTTPException
from flask import Flask, Response, jsonify, render_template, request
from controllers.file_system import File_System
from controllers.project_manager import Project_Manager

app = Flask(__name__)
filesystem = File_System()
project_manager = Project_Manager()
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
app.config["UPLOAD_EXTENSIONS"] = [".zip", ".rar"]

# @app.errorhandler(Exception)
# def handle_exception(e):
#     if isinstance(e, HTTPException):
#         response = e.get_response()
#         response.data = jsonify({
#             "code": e.code,
#             "name": e.name,
#             "description": e.description,
#         }).data
#         response.content_type = "application/json"
#         return response

#     return jsonify({
#         "code": 500,
#         "name": "Internal Server Error",
#         "description": "An internal server error occurred",
#     }), 500


@app.route("/")
def home():
    data = {
        "allowedUploadExtensions": ",".join(app.config["UPLOAD_EXTENSIONS"]),
        "maxContentLength": app.config["MAX_CONTENT_LENGTH"],
    }
    return render_template("index.html")


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
        "backend": "flask",
        "backend_dependencies": ["postgres"],
        "frontend": "react",
        "frontend_dependencies": [],
        "containerization": True,
    }
    github = {
        "token": "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",
        "username": "MainUseless",
        "repo_name": "scaffolding122",
        "description": "testing 12342",
        "is_private": True,
    }
    github = None
    is_created, result = project_manager.download_project(request, github)
    if is_created:
        return Response(
            project_manager.clean_up(result),
            mimetype="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename={request["projectName"]}.zip'
            },
        )
    else:
        return jsonify({"error": result}), 500


@app.route("/api/supportlist", methods=["GET"])
def get_supported_frameworks():
    return project_manager.get_supported_stuff(["description", "version"])


if __name__ == "__main__":
    app.run(debug=True)
