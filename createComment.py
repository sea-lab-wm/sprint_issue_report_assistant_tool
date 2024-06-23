import os
import requests
from dotenv import load_dotenv

load_dotenv()

def create_comment(repo_full_name, issue_number, comment_text, BRSeverity):
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/comments'

    private_key = os.environ.get('GITHUB_PRIVATE_KEY')

    if private_key is None:
        raise ValueError("GitHub private key is not set in the .env file")

    headers = {
        'Authorization': f'Bearer {private_key}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    # response_text = create_similarity_string(comment_text)
    if not comment_text:
        return
    
    comment_body = create_similarity_string(comment_text)
    comment_body += f"\n\n\n**Severity:** {BRSeverity}"

    create_label(repo_full_name, issue_number, "Duplicate")
    create_label(repo_full_name, issue_number, BRSeverity)

    data = {
        'body': comment_body
    }

    response = requests.post(url, headers=headers, json=data)
    print(response)

    if response.status_code == 201:
        print("Comment created successfully.")
    else:
        print("Failed to create comment:", response.status_code, response.text)




def create_similarity_string(duplicateIssues):
    similarity_string = "The most similar bug report issues are given below:\n\n\n"

    # Loop through the first 3 elements in sorted_results
    for result in duplicateIssues:
        issue_id = result['issue_id']
        issue_title = result['issue_title']
        issue_url = result['issue_url']


        similarity_string += f"**Issue ID:** {issue_id}\n"
        similarity_string += f"**Issue Title:** {issue_title}\n"
        similarity_string += f"**Issue URL:** {issue_url}\n"
        

        similarity_string += "\n\n\n"

    
    print(similarity_string)

    return similarity_string



def create_label(repo_full_name, issue_number, labelName):
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/labels'

    private_key = os.environ.get('GITHUB_PRIVATE_KEY')

    if private_key is None:
        raise ValueError("GitHub private key is not set in the .env file")

    headers = {
        'Authorization': f'Bearer {private_key}',
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    label_name = labelName

    data = {
        'labels': [label_name]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201 or response.status_code == 200:
        print(f"Label '{label_name}' created successfully on issue #{issue_number}.")
    else:
        print(f"Failed to create label '{label_name}':", response.status_code, response.text)