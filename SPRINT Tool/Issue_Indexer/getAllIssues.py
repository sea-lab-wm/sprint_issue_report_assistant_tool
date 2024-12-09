import requests, time
from GitHub_Event_Handler.app_authentication import authenticate_github_app

# Function to fetch issues from a GitHub repository with page-based indexing
def fetch_repository_issues(repo_full_name):
    auth_token = authenticate_github_app(repo_full_name)
    issues_url = f"https://api.github.com/repos/{repo_full_name}/issues"
    headers = {
        'Authorization': f'token {auth_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    issues_data = []
    page = 1
    per_page = 50  
    max_pages = 100  

    while page <= max_pages: 
        params = {
            'page': page,
            'per_page': per_page
        }

        try:
            response = requests.get(issues_url, headers=headers, params=params)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return
        

        if response.status_code == 200:
            issues_page_data = response.json()
            
            if not issues_page_data:
                print(f"Fetched all issues. Total issues fetched: {len(issues_data)}")
                break

            issues_data.extend(issues_page_data)
            print(f"Page {page} fetched. Total issues so far: {len(issues_data)}")

            page += 1

        elif response.status_code == 403:  
            reset_time = int(response.headers.get('X-RateLimit-Reset', time.time()))
            sleep_time = max(0, reset_time - time.time())
            print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
        else:
            print(f"Failed to fetch issues. Status code: {response.status_code}")
            print(f"Response: {response.json()}")
            break

    return issues_data
