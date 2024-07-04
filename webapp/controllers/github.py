import json
import os
import requests
import base64


class Github:
    def __init__(self, info) -> None:
        self.headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {info["token"]}',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        self.repo_name = info["repo_name"]
        self.description = info["description"]
        self.is_private = info["is_private"]
        self.username = info["username"]
        self.files_path = info["files_path"]
        pass

    def __create_repo(self):

        url = 'https://api.github.com/user/repos'
        data = {
            'name': self.repo_name,
            'description': self.description,
            'private': self.is_private,
            'auto_init': True,
        }

        response = requests.post(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 201:
            print(f'Repository {self.repo_name} created successfully!')
        else:
            print(f'Failed to create repository: {response.json()}')
            
    def __create_blob(self, file_path):
        with open(file_path, 'rb') as file:
            content = base64.b64encode(file.read()).decode('utf-8')
        url = f'https://api.github.com/repos/{self.username}/{self.repo_name}/git/blobs'
        data = {
            'content': content,
            'encoding': 'base64'
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            return response.json()['sha']
        else:
            print(f'Failed to create blob for {file_path}: {response.json()}')
    
    def __create_tree(self, blobs):
        url = f'https://api.github.com/repos/{self.username}/{self.repo_name}/git/trees'
        tree = []
        for file_path, blob_sha in blobs.items():
            tree.append({
                'path': os.path.relpath(file_path, self.files_path).replace('\\', '/'),
                'mode': '100644',
                'type': 'blob',
                'sha': blob_sha
            })
        data = {
            'tree': tree
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            return response.json()['sha']
        else:
            print(f'Failed to create tree: {response.json()}')
            
    def __create_commit(self, tree_sha):
        url = f'https://api.github.com/repos/{self.username}/{self.repo_name}/git/commits'
        data = {
            'message': 'Initial commit',
            'tree': tree_sha
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            return response.json()['sha']
        else:
            print(f'Failed to create commit: {response.json()}')
            
    def __update_reference(self, commit_sha):
        url = f'https://api.github.com/repos/{self.username}/{self.repo_name}/git/refs/heads/main'
        data = {
            'sha': commit_sha,
            'force': True
        }
        response = requests.patch(url, headers=self.headers, json=data)
        if response.status_code == 200:
            print(f'Reference updated to new commit SHA: {commit_sha}')
        else:
            print(f'Failed to update reference: {response.json()}')

    def upload_project(self):
        self.__create_repo()
        blobs = {}
        for root, _, files in os.walk(self.files_path):
            for file in files:
                file_path = os.path.join(root, file)
                blobs[file_path] = self.__create_blob(file_path)
        tree_sha = self.__create_tree(blobs)
        commit_sha = self.__create_commit(tree_sha)
        self.__update_reference(commit_sha)