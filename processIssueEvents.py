from getAllIssues import fetch_repository_issues
from getCodeFiles import fetch_all_code_files
from dupBRDetection import DuplicateDetection
from BRSeverityPred import SeverityPrediction
from createCommentBugLocalization import CreateCommentBL
from createComment import create_comment



def process_issue_event(repo_full_name, issue_number, action):
    if action == 'opened':
        issues_data = fetch_repository_issues(repo_full_name)
        code_files = fetch_all_code_files(repo_full_name)

        input_issue_title = issues_data[0]['title']
        input_issue_body = issues_data[0]['body']

        if input_issue_title is None:
            input_issue_title = ""
        if input_issue_body is None:
            input_issue_body = ""

        input_issue_data_for_model = input_issue_title + "\n" + input_issue_body

        duplicate_issue_list = []

        for issue in issues_data[1:]:
            issue_id = issue['number']
            issue_title = issue['title']
            issue_body = issue['body']
            issue_labels = [label['name'] for label in issue.get('labels', [])]
            print(issue_labels)
            issue_url = issue['html_url']

            if issue_title is None:
                issue_title = ""
            if issue_body is None:
                issue_body = ""

            issue_data_for_model = issue_title + "\n" + issue_body

            duplicatePrediction = DuplicateDetection(input_issue_data_for_model, issue_data_for_model)

            if duplicatePrediction == [1]:
                duplicate_issue_list.append({
                    "issue_id": issue_id,
                    "issue_title": issue_title,
                    "issue_url": issue_url,
                    "issue_label": issue_labels,
                })

        BRSeverity = SeverityPrediction(input_issue_data_for_model)

        create_comment(repo_full_name, issue_number, duplicate_issue_list, BRSeverity)
        CreateCommentBL(repo_full_name, issue_number, code_files)