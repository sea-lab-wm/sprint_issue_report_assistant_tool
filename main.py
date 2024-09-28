from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor, as_completed
# from dbOperations import is_bug_report_table_empty, insert_issue_to_db, fetch_all_bug_reports
from textModel import calculate_embeddings, calculate_similarity
from processIssueEvents import process_issue_event


app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=4)  



@app.route('/', methods=['POST'])
def api_git_msg():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        event = request.headers.get('X-GitHub-Event', '')
        action = data.get('action', '')

        # Get the repositories that the app was installed in
        if event == 'installation' and action == 'created':
            installation_repositories = data['repositories']
            return "Installation event handled", 200

        elif event == 'issues':
            repo_full_name = data['repository']['full_name']
            issue_number = data['issue']['number']

            print(f"Action: {action}, Repository: {repo_full_name}, Issue Number: {issue_number}")

            # Submit the issue processing task to the executor
            executor.submit(process_issue_event, repo_full_name, issue_number, action)

            return "Issue event handled", 200
        else:
            return "Not a relevant event, no action required.", 200
    else:
        return "415 Unsupported Media Type ;)", 415
                    


                # insert_issue_to_db(issue_id, issue_title, issue_body, issue_url, embedding)



            # if not is_bug_report_table_empty():
            #     id = data['issue']['number']
            #     title = data['issue']['title']
            #     body = data['issue']['body']
            #     embedding = calculate_embeddings(title+body)
            #     url = data['issue']['html_url']
            #     bug_reports = fetch_all_bug_reports()
            #     insert_issue_to_db(id, title, body, url, embedding)
            #     output = calculate_similarity(body, bug_reports)
            #     create_comment(repo_full_name, issue_number, output)



            # if is_bug_report_table_empty():
            #     issues_data = fetch_repository_issues(repo_full_name)
            #     for issue in issues_data:
            #         issue_id = issue['number']
            #         issue_title = issue['title']
            #         issue_body = issue['body']
            #         embedding = calculate_embeddings(issue_body)
            #         issue_url = issue['html_url']
            #         insert_issue_to_db(issue_id, issue_title, issue_body, issue_url, embedding)




if __name__ == '__main__':
    app.run(debug=True, port=5000)



# ./ngrok http 5000
# https://github.com/apps/sprint-issue-report-assistant
# .env file ta add kora lagbe
