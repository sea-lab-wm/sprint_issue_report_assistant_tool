import os
import requests
from dotenv import load_dotenv
from app_authentication import authenticate_github_app

load_dotenv()

def create_comment(repo_full_name, issue_number, comment_text, BRSeverity):
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
    create_label(repo_full_name, issue_number, BRSeverity, auth_token)


    if response.status_code == 201:
        print("Comment created successfully.")
    else:
        print(response.text)



def create_similarity_string(duplicateIssues):
    # Simple title using HTML and Markdown-like formatting for emphasis
    similarity_string = "## 🎯 Similar Issues:\n"

    for idx, result in enumerate(duplicateIssues, start=1):
        issue_id = result['issue_id']
        issue_title = result['issue_title']
        issue_url = result['issue_url']
        issue_label = result['issue_label']

        labels = [label.strip() for label in issue_label.split(',')]
        filtered_labels = [label for label in labels if label.lower() != 'duplicate' and label.strip()]

        # If there are filtered labels, join them; otherwise, display 'No Label Found'
        if filtered_labels:
            issue_label_str_values = ', '.join(filtered_labels)
            issue_label_str = f"<b>({issue_label_str_values})</b>"
        else:
            issue_label_str = " <b>(No Label found)</b>"

        # Use <code> tags and HTML for consistent formatting
        similarity_string += (
            f"### "
            f"<code style='display: block; border: 1px solid #ddd; border-radius: 5px; "
            f"margin: 10px 0; padding: 10px; font-size: 16px;'>"
            f"<b> <a href='{issue_url}' style='text-decoration: none;'>📝  <b>#{issue_id}</b> - {issue_title}</b></a>"
            f"{issue_label_str}"
            f"</code>"
            f"<hr>\n"  # Add a horizontal line for separation
        )

    return similarity_string





def add_label_to_issue(repo_full_name, issue_number, label_name, auth_token):
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/labels'
    
    # private_key = os.environ.get('GITHUB_PRIVATE_KEY')
    
    # if private_key is None:
    #     raise ValueError("GitHub private key is not set in the .env file")
    
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
    
    # private_key = os.environ.get('GITHUB_PRIVATE_KEY')
    
    # if private_key is None:
    #     raise ValueError("GitHub private key is not set in the .env file")
    
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
        'Blocker': '880808',    # deep red
        'Critical': 'D22B2B',   # cadmium red 
        'Major': 'A52A2A',      # brown
        'Minor': 'CC5500',      # burnt orange
        'Trivial': 'E97451'     # burnt sienna
    }
    

    label_color = label_colors.get(label_name, '000000')  
    
    create_or_update_label(repo_full_name, label_name, label_color, auth_token)
    add_label_to_issue(repo_full_name, issue_number, label_name, auth_token)



    # ⚠️<b>(<span style='color: red;'>{issue_label_str}</span>)</b>⚠️



# similarity_string += (
#             f"🔗 **(#{issue_id}) "
#             f"[{issue_title}]({issue_url})** &nbsp;&nbsp;&nbsp; **{issue_label_str}**\n\n"
#             "---\n"  # Horizontal line to separate each issue visually
#         )