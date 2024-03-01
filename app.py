import io
import json
import os
from flask import Flask, jsonify, render_template, current_app
from jinja2 import Template,Environment ,FileSystemLoader
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

def render_schema_template(schema, project_name):
    # Jinja template string
    template_str = """
    {
      "projectName": "{{ projectName }}",
      "schema": [
        {
          "root": "{{ schema.name }}",
          "content": [
            {% for entry in schema %}
            {
                "name": "{{ entry.name }}",
                {% if entry.children %}
                "content": [
                    {% for subitem in entry.children %}
                        {
                        "name": "{{ subitem.name }}",
                        {% if subitem.children %}
                            "content": [
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

    # Create a Jinja environment
    env = Environment(loader=FileSystemLoader("./templates"))

    # Load the template
    html_template = env.get_template("schema.html")

    # Render the HTML template with the provided data
    rendered_html = html_template.render(projectName=project_name, renderedSchema=rendered_schema)

    return rendered_html

test = Directory("myroot")
test.add(File("file1.txt"))
test.add(File("file2.txt"))
test.add(Directory("dir1"))
test.add(Directory("dir2"))
test.children[2].add(File("file3.txt")) #dir1
test.children[2].add(Directory("dir3"))
test.children[2].children[1].add(File("file4"))
test.children[2].children[1].add(File("file5"))

@app.route("/test", methods=["GET"])
def lol():
    rendered_schema = render_schema_template(test,"testproject")
    rendered_html = render_html_template(rendered_schema,"myProject")

    return rendered_html


if __name__ == "__main__":
    app.run(debug=True)
