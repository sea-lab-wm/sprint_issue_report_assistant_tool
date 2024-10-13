import requests
from app_authentication import authenticate_github_app

def fetch_all_code_files(repo_full_name, branch='main'):

    url = f'https://api.github.com/repos/{repo_full_name}/git/trees/{branch}?recursive=1'
    auth_token = authenticate_github_app(repo_full_name)

    headers = {
        'Authorization': f'token {auth_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching repository tree: {response.status_code} - {response.text}")
        return []

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


