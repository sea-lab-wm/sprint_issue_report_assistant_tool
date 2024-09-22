import requests
from app_authentication import authenticate_github_app

def fetch_all_code_files(repo_full_name, branch='main'):

    url = f'https://api.github.com/repos/{repo_full_name}/git/trees/{branch}?recursive=1'
    auth_token = authenticate_github_app(repo_full_name)

    headers = {
        'Authorization': f'token {auth_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Step 2: Make the API request to get the repository tree
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching repository tree: {response.status_code} - {response.text}")
        return []

    # Step 3: Extract the list of files (blobs) from the response
    tree_data = response.json().get('tree', [])
    
    # Step 4: Filter out files (blobs) and collect their paths and URLs
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


