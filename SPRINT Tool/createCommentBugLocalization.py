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

    # If no code files are provided, do not proceed.
    if not code_files:
        return

    # Filter out non-code files such as .txt and .md files
    filtered_files = [
        file for file in code_files 
        if not (file['path'].endswith('.txt') or file['path'].endswith('.md'))
    ]

    # Select the top 5 files
    top_files = filtered_files[:5]

    # If there are no filtered files left after filtering, do not proceed
    if not top_files:
        return

    # Create the formatted list of buggy files with normal text formatting
    formatted_code_files = ""
    for idx, file in enumerate(top_files, start=1):
        file_name = file['path'].split('/')[-1]  # Extract just the file name
        file_url = file['url']  # The file URL
        formatted_code_files += (
            f"**🔗 "
            f"[{file_name}]({file_url})**\n\n"
            "---\n"  # Horizontal line to separate each file visually
        )



    # Create the comment body without a large header or bold text
    comment_body = f" ## **🐞 Potential Buggy Code Files:**\n\n{formatted_code_files}"

    # Create the payload to send to the GitHub API
    payload = {
        'body': comment_body
    }

    # Post the comment to the GitHub issue
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    if response.status_code == 201:
        print("Comment created successfully.")
    else:
        print(response.text)



# formatted_code_files += (
#             f"**🔗 "
#             f"[{file_name}]({file_url})**\n\n"
#             "---\n"  # Horizontal line to separate each file visually
#         )