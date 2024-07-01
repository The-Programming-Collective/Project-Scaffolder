import os, json


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
