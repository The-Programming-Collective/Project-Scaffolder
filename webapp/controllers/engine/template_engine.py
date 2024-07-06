# Generates JSON template from existing project and renders jinja if any jinja code exists

from jinja2 import Template
import json, os, ast, re

class Template_Engine:
    def __init__(self) -> None:
        self.templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        
    def __traverse_directory(self, directory_path):
        project_structure = {}

        for root, dirs, files in os.walk(directory_path):
            relative_path = os.path.relpath(root, directory_path)
            if relative_path == ".":
                relative_path = ""

            current_level = project_structure
            if relative_path:
                for part in relative_path.split(os.sep):
                    current_level = current_level.setdefault(part, {})

            for d in dirs:
                current_level[d] = {}

            for f in files:
                with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                    file_content = file.read()
                    current_level[f] = file_content

        return project_structure
    
    def generate_template(self, directory_path : str):
        project_structure = self.__traverse_directory(directory_path)
        project_structure_json = json.dumps(project_structure, indent=4)
        return project_structure_json

    def read_jinja_files(self, files_names, *args) -> dict:
        path = os.path.join(self.templates_dir, *args)
        tree = {}

        try:
            if os.path.exists(path):
                for entry in os.scandir(path):
                    if entry.is_file() and ((entry.name.split('.')[0] in files_names) or files_names == "all"):
                        with open(entry.path, "r") as file:
                            content = file.read()
                            if entry.name == 'Dockerfile':
                                tree[entry.name] = content
                                return tree
                            file_name, extention = entry.name.split('.')
                            # software engineered code 101
                            if(extention == 'json'):
                                tree[file_name] = json.loads(content)
                            else:
                                tree[file_name] = content
        except Exception as e:
            # print(e)
            return tree

        return tree

    # request = {
    #    "project_name": "test",
    #    "backend": "flask",
    #    "backend_dependencies": ["swagger"],
    #    "frontend": "react",
    #    "frontend_dependencies": ["react-router-dom", "axios"],
    #    "containerization": true,
    # }
    
    def render_template(self, request : dict) -> dict:
        try:
            master = {}
            
            if(request["backend"] != 'none'):
                backend_dependencies = self.read_jinja_files(request["backend_dependencies"],'backend', request["backend"], 'dependencies')
                backend_template = Template(self.read_jinja_files([request["backend"]], 'backend', request["backend"]).popitem()[1])
                backend_context = {}
                backend_context["dependencies"] = backend_dependencies
                backend_context["projectName"] = request["project_name"]
                # for javaee 
                backend_context["groupId"] = "scaffold"
                backend = ast.literal_eval(backend_template.render(backend_context))
                master["backend"] = backend
                

            if(request["frontend"] != 'none'):
                frontend_dependencies = self.read_jinja_files(request["frontend_dependencies"], 'frontend', request["frontend"], 'dependencies')
                frontend_template = Template(self.read_jinja_files([request["frontend"]], 'frontend', request["frontend"]).popitem()[1])
                frontend_context = {}
                frontend_context["dependencies"] = frontend_dependencies
                frontend_context["projectName"] = request["project_name"]
                frontend = ast.literal_eval(frontend_template.render(frontend_context))
                master["frontend"] = frontend
            
            master["projectName"] = request["project_name"]
            master["README.md"] = "This is a test README file"

            if(request["containerization"]):
                if(request["backend"] != 'none'):
                    backend_dockerfile = self.read_jinja_files(["Dockerfile"], 'backend', request["backend"])
                    backend_dockerfile = backend_dockerfile.popitem()[1] if backend_dockerfile else "No dockerfile found"
                    master["backend"]["Dockerfile"] = backend_dockerfile
                    
                if(request["frontend"] != 'none'):
                    frontend_dockerfile = self.read_jinja_files(["Dockerfile"], 'frontend', request["frontend"])
                    frontend_dockerfile = frontend_dockerfile.popitem()[1] if frontend_dockerfile else "No dockerfile found"
                    master["frontend"]["Dockerfile"] = frontend_dockerfile

                master["README.md"] += "\n\n-This project is containerized using Docker, in order to use containerization ensure that you have docker installed.\n-To run the backend and frontend, first create a Docker image using the provided Dockerfiles using the following commands:\n\n-For the backend(first navigate to the backend directory):\n\n```docker build -t backend .```\n\n-For the frontend(first navigate to the frontend directory):\n\n```docker build -t frontend .```\n\nAfter creating the images, run the containers using the following commands:\n\n-For the backend:\n\n```docker run -p 5000:5000 backend```\n\n-For the frontend:\n\n```docker run -p 3000:3000 frontend```\n\n-After running the containers, you can access the backend at http://localhost:5000 and the frontend at http://localhost:3000\n\nNote: Ensure that the backend is running before running the frontend."
        except Exception as e:
            raise Exception("An error occurred while rendering the template or invalid requested data")
        return master
