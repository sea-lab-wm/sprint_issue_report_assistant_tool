import requests, os

# Function to fetch issues from a GitHub repository
def fetch_repository_issues(repo_full_name):
    private_key = os.environ.get('GITHUB_PRIVATE_KEY')
    issues_url = f"https://api.github.com/repos/{repo_full_name}/issues"
    headers = {
        'Authorization': f'Bearer {private_key}',
    }
    response = requests.get(issues_url, headers=headers)

    if response.status_code == 200:
        issues_data = response.json()
        return issues_data
    else:
        print(f"Failed to fetch issues. Status code: {response.status_code}")
        return []

def get_issue_url(repo_full_name, issue_number):
    return f"https://github.com/{repo_full_name}/issues/{issue_number}"