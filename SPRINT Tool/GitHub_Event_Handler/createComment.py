import requests
from dotenv import load_dotenv
from .app_authentication import authenticate_github_app

load_dotenv()

def create_comment(repo_full_name, issue_number, comment_text):
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/comments'


    auth_token = authenticate_github_app(repo_full_name)

    headers = {
        'Authorization': f'token {auth_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    if not comment_text:
        return
    
    
    comment_body = create_similarity_string(comment_text)

    print(comment_text)

    payload = {
        'body': comment_body
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    

    create_label(repo_full_name, issue_number, "Duplicate", auth_token)


    if response.status_code == 201:
        print("Comment created successfully.")
    else:
        print(response.text)



def create_similarity_string(duplicateIssues):
    similarity_string = "## 🎯 Similar Issues:\n"
    similarity_string += "**The following issues are potentially similar to the given issue:**\n\n"

    for idx, result in enumerate(duplicateIssues, start=1):
        issue_id = result['issue_id']
        issue_title = result['issue_title']
        issue_url = result['issue_url']
        issue_label = result['issue_label']

        labels = [label.strip() for label in issue_label.split(',')]
        filtered_labels = [label for label in labels if label.lower() != 'duplicate' and label.strip()]

        if filtered_labels:
            issue_label_str_values = ', '.join(filtered_labels)
            issue_label_str = f"<b>({issue_label_str_values})</b>"
        else:
            issue_label_str = ""

        similarity_string += (
            f"### "
            f"<code style='display: block; border: 1px solid #ddd; border-radius: 5px; "
            f"margin: 10px 0; padding: 10px; font-size: 16px;'>"
            f"<b> <a href='{issue_url}' style='text-decoration: none;'>📝  <b>#{issue_id}</b> - {issue_title}</b></a>"
            f"{issue_label_str}"
            f"</code>"
            f"<hr>\n"  
        )

    return similarity_string





def add_label_to_issue(repo_full_name, issue_number, label_name, auth_token):
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/labels'

    
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'labels': [label_name]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"Label '{label_name}' added to issue #{issue_number} successfully.")
    else:
        print(f"Failed to add label '{label_name}' to issue #{issue_number}:", response.status_code, response.text)



def create_or_update_label(repo_full_name, label_name, label_color, auth_token):
    url = f'https://api.github.com/repos/{repo_full_name}/labels/{label_name}'

    
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    data = {
        'name': label_name,
        'color': label_color
    }
    
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"Label '{label_name}' created or updated successfully.")
    else:
        print(f"Failed to create or update label '{label_name}':", response.status_code, response.text)





def create_label(repo_full_name, issue_number, label_name, auth_token):
    label_colors = {
        'Duplicate': '33ffa8',  # olive
        'Blocker': 'ba4a00',    # deep red
        'Critical': 'e67e22 ',   # cadmium red 
        'Major': 'f5b041',      # brown
        'Minor': 'd4ac0d',      # burnt orange
        'Trivial': 'f7dc6f'     # burnt sienna
    }
    

    label_color = label_colors.get(label_name, '000000')  
    
    create_or_update_label(repo_full_name, label_name, label_color, auth_token)
    add_label_to_issue(repo_full_name, issue_number, label_name, auth_token)


def DupStartingCommentForWaiting(repo_full_name, issue_number):
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/comments'
    auth_token = authenticate_github_app(repo_full_name)

    headers = {
        'Authorization': f'token {auth_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    comment_body = (
        "## ⏳ **Please hang on a little!**\n\n"
        "**SPRINT** is analyzing your issue and will provide the list of potential similar issues soon\n\n"
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