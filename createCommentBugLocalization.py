import os
import requests
from dotenv import load_dotenv
from app_authentication import authenticate_github_app

load_dotenv()

def CreateCommentBL(repo_full_name, issue_number, code_files):
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/comments'
    
    auth_token = authenticate_github_app(repo_full_name)

    headers = {
        'Authorization': f'token {auth_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    if not code_files:
        return


    filtered_files = [
        file for file in code_files 
        if not (file['path'].endswith('.txt') or file['path'].endswith('.md'))
    ]

    top_files = filtered_files[:5]

    if not top_files:
        return

    formatted_code_files = ""
    for idx, file in enumerate(top_files, start=1):
        file_name = file['path'].split('/')[-1]  
        formatted_code_files += f"<b>{idx}. [{file_name}]({file['url']})</b>  &nbsp;&nbsp; \n\n"

  
    comment_body = "### Potential Buggy Files: \n\n" + formatted_code_files

    payload = {
        'body': comment_body
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    if response.status_code == 201:
        print("Comment created successfully.")
    else:
        print(response.text)
