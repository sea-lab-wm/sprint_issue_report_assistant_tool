import requests
from .app_authentication import authenticate_github_app

def fetch_all_code_files(repo_full_name, branch='main'):
    try:
        url = f'https://api.github.com/repos/{repo_full_name}/git/trees/{branch}?recursive=1'
        auth_token = authenticate_github_app(repo_full_name)

        headers = {
            'Authorization': f'token {auth_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  

        tree_data = response.json().get('tree', [])

        code_files = []
        for item in tree_data:
            if item['type'] == 'blob':
                file_path_url = f"https://github.com/{repo_full_name}/blob/{branch}/{item['path']}"
                code_files.append({
                    'path': item['path'],
                    'url': file_path_url
                })

        for file in code_files:
            print(f"File: {file['path']}, URL: {file['url']}")

        return code_files

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        print(f"Error parsing JSON response: {json_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

    return []

