import requests
from dotenv import load_dotenv
from .app_authentication import authenticate_github_app


def CreateCommentBL(repo_full_name, issue_branch, issue_number, code_files, paths_only):
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

        formatted_code_files = ""
        for idx, file_path in enumerate(filtered_code_files, start=1):
            file_name = file_path.split('/')[-1]


            code_file_path = None
            for index, path in enumerate(paths_only):
                if file_name in path:
                    code_file_path = path
                    break

            if not code_file_path:
                continue

            file_url = f"https://github.com/{repo_full_name}/blob/{issue_branch}/{code_file_path}"

            formatted_code_files += (
                f"**🔗 [{file_name}]({file_url})**\n\n"
                "---\n"
            )

        
            comment_body = f"## **🐞 Potential Buggy Code Files:**\n\n**The following code files may contain the bug or related to the bug in the given issue:**\n\n{formatted_code_files}"
    else:
        print("Invalid type for code_files. Must be a list or string.")
        return

    payload = {
        'body': comment_body
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    if response.status_code == 201:
        print("Comment created successfully.")
    else:
        print(response.text)



def BLStartingCommentForWaiting(repo_full_name, issue_number):
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/comments'
    auth_token = authenticate_github_app(repo_full_name)

    headers = {
        'Authorization': f'token {auth_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    comment_body = (
        "## ⏳ **Please hang on a little!**\n\n"
        "**SPRINT** is analyzing your issue and will provide the list of potential buggy files "
        "in about **1–2 minutes**.\n\n"
    )

    payload = {
        'body': comment_body
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    if response.status_code == 201:
        print("Waiting comment created successfully.")
    else:
        print(response.text)