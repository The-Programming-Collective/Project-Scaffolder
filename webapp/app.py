import os
from flask import Flask, Response, jsonify, render_template, request
from controllers.file_system import FileSystem
from controllers.engine.template_engine import TemplateEngine

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
app.config["UPLOAD_EXTENSIONS"] = [".zip", ".rar"]
app.config["TEMP_PATH"] = os.path.join(app.root_path, "temp")
filesystem = FileSystem()


@app.route("/")
def home():
    return render_template(
        "index.html",
        frameworks=filesystem.traverse_directory(
            root="controllers/engine/templates", levels=3
        ),
        allowedUploadExtentions=",".join(app.config["UPLOAD_EXTENSIONS"]),
        maxContentLength=app.config["MAX_CONTENT_LENGTH"],
    )


@app.route("/upload", methods=["POST"])
def upload_file():
    if not filesystem.allowed_file(
        request.files["file"].filename, app.config["UPLOAD_EXTENSIONS"]
    ):
        return jsonify({"error": "File type not allowed"}), 400

    uploaded_file = request.files["file"]
    file_path = os.path.join(app.config["TEMP_PATH"], uploaded_file.filename)
    uploaded_file.save(file_path)
    return jsonify({"message": "File uploaded successfully"})


@app.route("/download", methods=["GET"])
def download_file():
    request = {
        "projectName": "Testing",
        "backend": "javaee10",
        "backend_dependencies": ["junit"],
        "frontend": "react",
        "frontend_dependencies": []
    }
    return Response(
        filesystem.download_project(TemplateEngine().render_template2(request)),
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
