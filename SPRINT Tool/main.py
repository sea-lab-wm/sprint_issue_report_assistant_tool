from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor
from processIssueEvents import process_issue_event
from getAllIssues import fetch_repository_issues
from dbOperations import insert_issue_to_db, create_table_if_not_exists, delete_table
import platform
import multiprocessing
import torch


cuda_available = torch.cuda.is_available()
os_name = platform.system()


if os_name == 'Linux' and cuda_available:
    multiprocessing.set_start_method('spawn', force=True)
elif os_name == 'Windows':
    multiprocessing.set_start_method('spawn', force=True)

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=4)  


@app.route('/', methods=['POST'])
def api_git_msg():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        event = request.headers.get('X-GitHub-Event', '')
        action = data.get('action', '')

        if event == 'installation' and action == 'created':
            installed_repos = data['repositories']
            for repo in installed_repos:
                repo_full_name = repo['full_name']
                create_table_if_not_exists(repo_full_name)
                issues_data = fetch_repository_issues(repo_full_name)
                
                for issue in issues_data:
                    issue_id = issue['number']
                    issue_title = issue['title'] or ""
                    issue_body = issue['body'] or ""
                    created_at = issue['created_at']
                    issue_url = issue['html_url']  
                    issue_labels = [label['name'] for label in issue.get('labels', [])]

                    insert_issue_to_db(repo_full_name, issue_id, issue_title, issue_body, created_at, issue_url, issue_labels)
            
            return "Installation event handled", 200

        elif event == 'installation' and action == 'deleted':
            removed_repos = data['repositories']
            for repo in removed_repos:
                repo_full_name = repo['full_name']
                delete_table(repo_full_name)
            
            return "Uninstallation event handled, tables deleted", 200

        elif event == 'issues':
            repo_full_name = data['repository']['full_name']
            issue_number = data['issue']['number']
            issue_title = data['issue']['title']
            issue_body = data['issue']['body']
            issue_creation_time = data['issue']['created_at']  
            issue_url = data['issue']['html_url']
            issue_labels = [label['name'] for label in data['issue'].get('labels', [])]

            input_issue = {
                'issue_number': issue_number,
                'issue_title': issue_title,
                'issue_body': issue_body,
                'created_at': issue_creation_time,
                'issue_url': issue_url,
                'issue_labels': issue_labels
            }

            # Submit the issue processing task to the executor
            executor.submit(process_issue_event, repo_full_name, input_issue, action)

            return "Issue event handled", 200
        else:
            return "Not a relevant event, no action required.", 200
    else:
        return "415 Unsupported Media Type ;)", 415


if __name__ == '__main__':
    app.run(debug=True, port=5000)


# https://github.com/apps/sprint-issue-report-assistant
