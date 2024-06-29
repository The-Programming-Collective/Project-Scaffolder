import random, string, os, json


def randomword(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def allowed_file(filename, allowedExtensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowedExtensions


def get_frameworks():
    dirs = os.listdir(os.path.join(os.path.dirname(__file__), "engine", "templates"))

    all = {}

    for dir in dirs:
        if os.path.isdir(
            os.path.join(os.path.dirname(__file__), "engine", "templates", dir)
        ):
            all[dir] = os.listdir(
                os.path.join(os.path.dirname(__file__), "engine", "templates", dir)
            )

    return all


# Function to load JSON files from specified subdirectories
def load_json_files(directory_path, stack_names):
    json_files = {}

    for category, stack in stack_names:
        stack_path = os.path.join(directory_path, category, stack)
        if os.path.isdir(stack_path):
            for file in os.listdir(stack_path):
                if file.endswith(".json"):
                    file_path = os.path.join(stack_path, file)
                    with open(file_path, "r") as f:
                        file_content = json.load(f)
                        json_files[category] = file_content
                    break  # Only process one JSON file per subdirectory

    return json_files
