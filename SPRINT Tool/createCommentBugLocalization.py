import os
import requests
from dotenv import load_dotenv
from app_authentication import authenticate_github_app


def CreateCommentBL(repo_full_name, issue_number, code_files):
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/comments'
    auth_token = authenticate_github_app(repo_full_name)

    headers = {
        'Authorization': f'token {auth_token}',
        'Accept': 'application/vnd.github.v3+json'
    }


    if not code_files:
        return


    top_files = code_files[:5]

    if not top_files:
        return

    formatted_code_files = ""
    for idx, file_path in enumerate(top_files, start=1):
        file_name = file_path.split('/')[-1]  
        file_url = f"https://github.com/{repo_full_name}/blob/main/{file_path}"  
        formatted_code_files += (
            f"**🔗 "
            f"[{file_name}]({file_url})**\n\n"
            "---\n"  
        )

    comment_body = f"## **🐞 Potential Buggy Code Files:**\n\n{formatted_code_files}"

    payload = {
        'body': comment_body
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    if response.status_code == 201:
        print("Comment created successfully.")
    else:
        print(response.text)

