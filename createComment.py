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
    similarity_string = "### The Most Similar Issues\n\n"

    string_after_bug_localization = ""
    
    for result in duplicateIssues:
        issue_id = result['issue_id']
        issue_title = result['issue_title']
        issue_url = result['issue_url']
        issue_label = result['issue_label']
        
        # Filter out the 'duplicate' label and convert the list to a comma-separated string, or use 'No labels' if empty
        filtered_labels = [label for label in issue_label if label != 'duplicate']
        
        if filtered_labels:
            issue_label_str = ', '.join(filtered_labels)
        else:
            issue_label_str = 'No Severity Label Found'
        
        # Construct the string with Markdown syntax for headings and links
        similarity_string += f"<code style='color: red;'>📝 [{issue_title}]({issue_url}) 📝 ⚠️<b>({issue_label_str})</b>⚠️</code>\n\n"
        string_after_bug_localization = similarity_string
    

    similarity_string += "\n\n\n🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\n"
    similarity_string += "\n\n\n### The potential bug occuring files: \n\n"    

    
    return similarity_string



def generateBugLocalizationComment(string_after_bug_localization):
    string_after_bug_localization += "\n\n\n🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩#### The potential bug occuring files: 🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩\n\n"



# def create_label(repo_full_name, issue_number, labelName):
#     url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/labels'

#     private_key = os.environ.get('GITHUB_PRIVATE_KEY')

#     if private_key is None:
#         raise ValueError("GitHub private key is not set in the .env file")

#     headers = {
#         'Authorization': f'Bearer {private_key}',
#         'Accept': 'application/vnd.github.v3+json',
#         'X-GitHub-Api-Version': '2022-11-28'
#     }

#     label_name = labelName

#     data = {
#         'labels': [label_name]
#     }

#     response = requests.post(url, headers=headers, json=data)

#     if response.status_code == 201 or response.status_code == 200:
#         print(f"Label '{label_name}' created successfully on issue #{issue_number}.")
#     else:
#         print(f"Failed to create label '{label_name}':", response.status_code, response.text)



def add_label_to_issue(repo_full_name, issue_number, label_name):
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/labels'
    
    private_key = os.environ.get('GITHUB_PRIVATE_KEY')
    
    if private_key is None:
        raise ValueError("GitHub private key is not set in the .env file")
    
    headers = {
        'Authorization': f'Bearer {private_key}',
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



def create_or_update_label(repo_full_name, label_name, label_color):
    url = f'https://api.github.com/repos/{repo_full_name}/labels/{label_name}'
    
    private_key = os.environ.get('GITHUB_PRIVATE_KEY')
    
    if private_key is None:
        raise ValueError("GitHub private key is not set in the .env file")
    
    headers = {
        'Authorization': f'Bearer {private_key}',
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





def create_label(repo_full_name, issue_number, label_name):
    label_colors = {
        'Duplicate': '6B8E23',  # olive
        'Blocker': '880808',    # deep red
        'Critical': 'D22B2B',   # cadmium red 
        'Major': 'A52A2A',      # brown
        'Minor': 'CC5500',      # burnt orange
        'Trivial': 'E97451'     # burnt sienna
    }
    

    label_color = label_colors.get(label_name, '000000')  
    
    create_or_update_label(repo_full_name, label_name, label_color)
    add_label_to_issue(repo_full_name, issue_number, label_name)