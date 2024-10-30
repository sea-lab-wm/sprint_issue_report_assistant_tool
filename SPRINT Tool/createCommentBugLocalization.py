import os
import requests
from dotenv import load_dotenv
from app_authentication import authenticate_github_app


def CreateCommentBL(repo_full_name, issue_branch, issue_number, code_files):
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/comments'
    auth_token = authenticate_github_app(repo_full_name)

    headers = {
        'Authorization': f'token {auth_token}',
        'Accept': 'application/vnd.github.v3+json'
    }


    if isinstance(code_files, str):
        comment_body = code_files
    elif isinstance(code_files, list):
        if not code_files:
            return

        filtered_code_files = [
            file for file in code_files
            if not (file.lower().endswith('readme.md') or file.lower().endswith('.txt'))
        ]

        if not filtered_code_files:
            return


        # Format the list of code files into markdown
        formatted_code_files = ""
        for idx, file_path in enumerate(filtered_code_files, start=1):
            file_name = file_path.split('/')[-1]
            file_url = f"https://github.com/{repo_full_name}/blob/{issue_branch}/{file_path}"
            formatted_code_files += (
                f"**🔗 [{file_name}]({file_url})**\n\n"
                "---\n"
            )
        
        comment_body = f"## **🐞 Potential Buggy Code Files:**\n\n{formatted_code_files}"
    else:
        print("Invalid type for code_files. Must be a list or string.")
        return

    # Prepare the payload and post the comment
    payload = {
        'body': comment_body
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    if response.status_code == 201:
        print("Comment created successfully.")
    else:
        print(response.text)

