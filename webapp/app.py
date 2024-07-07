from flask import Flask, Response, json, jsonify, render_template, request
from controllers.file_system import File_System
from controllers.project_manager import Project_Manager

app = Flask(__name__)
filesystem = File_System()
project_manager = Project_Manager()
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
app.config["UPLOAD_EXTENSIONS"] = [".zip", ".rar"]


@app.route("/")
def home():
    data = {
        "allowedUploadExtensions": ",".join(app.config["UPLOAD_EXTENSIONS"]),
        "maxContentLength": app.config["MAX_CONTENT_LENGTH"],
        "supported_stuff": project_manager.get_supported_stuff(["description", "version"]),
    }
    return render_template("index.html",data=data)


@app.route("/api/upload", methods=["POST"])
def upload_file():
    if not filesystem.allowed_file(
        request.files["file"].filename, app.config["UPLOAD_EXTENSIONS"]
    ):
        return jsonify({"error": "File type not allowed"}), 400
    return project_manager.get_project_structure(request.files["file"]), 200


@app.route("/api/download", methods=["POST"])
def generate_project():
    # request = {
    #     "project_name": "Testing",
    #     "backend": "flask",
    #     "backend_dependencies": ["postgres"],
    #     "frontend": "react",
    #     "frontend_dependencies": [],
    #     "containerization": True,
    #     "github": {
    #         "api_key": "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",
    #         "username": "MainUseless",
    #         "repo_name": "scaffolding122",
    #         "description": "testing 12342",
    #         "is_private": True,
    #     }
    # }
    req = json.loads(request.data)
    if req["project_name"] == "":
        return jsonify({"error": "Please provide a project name"}), 400
    if req["frontend"] == "none" and req["backend"] == "none":
        return jsonify({"error": "Please select a frontend or backend framework"}), 400
    is_created, result = project_manager.download_project(req)
    if is_created:
        return Response(
            project_manager.clean_up(result),
            mimetype="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename={req["project_name"]}.zip'
            },
        )
    else:
        return jsonify({"error": result}), 500


@app.route("/api/supportlist", methods=["GET"])
def get_supported_frameworks():
    return project_manager.get_supported_stuff(["description", "version"])


if __name__ == "__main__":
    app.run(debug=True)
