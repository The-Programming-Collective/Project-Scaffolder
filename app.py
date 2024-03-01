import io
import json
import os
from flask import Flask, jsonify, render_template, current_app
import shutil
from classes.directory import Directory
from classes.file import File

app = Flask(__name__)


@app.route("/")
def helloWorld():
    return render_template("index.html")


@app.route("/download", methods=["GET"])
def download_file(project_path):
    directory_path = os.path.join(app.root_path, "temp", "project")
    os.mkdir(directory_path)
    file_path = os.path.join(directory_path, "test.txt")
    file_writer = open(file_path, "w")
    file_writer.write("Hello World")
    file_writer.close()

    # Zip file
    target_path = os.path.join(app.root_path, "temp", "project")
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

test = Directory("test")
test.add(File("test1.txt"))
test.add(File("test2.txt"))
test.add(Directory("testDir"))
test.childern[2].add(File("test3.txt"))

@app.route("/test", methods=["GET"])
def lol():
    schema_str = test.print_structure()
    return jsonify({"schema": schema_str})


if __name__ == "__main__":
    app.run(debug=True)
