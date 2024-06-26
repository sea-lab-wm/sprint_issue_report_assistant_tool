from flask import Flask, request
from createComment import create_comment
# from db_config import db, configure_database
# from models import BugReport
from getAllIssues import fetch_repository_issues
# from dbOperations import is_bug_report_table_empty, insert_issue_to_db, fetch_all_bug_reports
from textModel import calculate_embeddings, calculate_similarity
from dupBRDetection import DuplicateDetection
from BRSeverityPred import SeverityPrediction

app = Flask(__name__)

# configure_database(app)



@app.route('/', methods=['POST'])
def api_git_msg():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        action = data.get('action', '')
        repo_full_name = data['repository']['full_name']
        issue_number = data['issue']['number']

        if action == 'opened':
            issues_data = fetch_repository_issues(repo_full_name)

            input_issue_title = issues_data[0]['title']
            input_issue_body = issues_data[0]['body']

            if input_issue_title is None:
                input_issue_title = ""
            if input_issue_body is None:
                input_issue_body = ""

            input_issue_data_for_model = input_issue_title + "\n" +  input_issue_body

            duplicate_issue_list = []
            
            for issue in issues_data[1:]:
                issue_id = issue['number']
                issue_title = issue['title']
                issue_body = issue['body']
                issue_labels = [label['name'] for label in issue.get('labels', [])]
                print(issue_labels)
                issue_url = issue['html_url']

                if input_issue_title is None:
                    issue_title = ""
                if input_issue_body is None:
                    issue_body = ""

                issue_data_for_model = issue_title + "\n" + issue_body

                # print("\n\n")
                # print(input_issue_data_for_model)
                # print(issue_data_for_model)

                
                duplicatePrediction = DuplicateDetection(input_issue_data_for_model, issue_data_for_model)
                
                # print(duplicatePrediction)

                if duplicatePrediction == [1]:
                    duplicate_issue_list.append({
                        "issue_id": issue_id,  
                        "issue_title": issue_title,  
                        "issue_url": issue_url,
                        "issue_label": issue_labels,
                    })

            BRSeverity = SeverityPrediction(input_issue_data_for_model)


            # print(repo_full_name)
            # print(issue_number)
            # print(duplicate_issue_list)
            create_comment(repo_full_name, issue_number, duplicate_issue_list, BRSeverity)
                    


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

        return "Not a new issue, no action required."
    else:
        return "415 Unsupported Media Type ;)"




if __name__ == '__main__':
    app.run(debug=True, port=5000)



# ./ngrok http 5000