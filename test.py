from getAllIssues import fetch_repository_issues
from getCodeFiles import fetch_all_code_files
from dupBRDetection import DuplicateDetection
from BRSeverityPred import SeverityPrediction
from createCommentBugLocalization import CreateCommentBL
from createComment import create_comment
import multiprocessing
from functools import partial
from dbOperations import create_table_if_not_exists, is_table_exists, insert_issue_to_db, fetch_all_bug_reports_from_db


def process_issue_event(repo_full_name, issue_number, action):
    if action == 'opened':
        # Check if the table for the repository exists
        if not is_table_exists(repo_full_name):
            print(f"Table for {repo_full_name} does not exist. Creating the table and fetching issues.")
            create_table_if_not_exists(repo_full_name)

            # Fetch issues from GitHub and insert them into the database
            issues_data = fetch_repository_issues(repo_full_name)
            for issue in issues_data:
                issue_id = issue['number']
                issue_title = issue['title'] or ""
                issue_body = issue['body'] or ""
                created_at = issue['created_at']

                insert_issue_to_db(repo_full_name, issue_id, issue_title, issue_body, created_at)

        else:
            print(f"Table for {repo_full_name} already exists. Fetching issues from the database.")
            issues_data = fetch_all_bug_reports_from_db(repo_full_name)

        # Get the data for the opened issue (not fetching all issues again)
        opened_issue = next((issue for issue in issues_data if issue['number'] == issue_number), None)
        if opened_issue:
            issue_id = opened_issue[0]  # issue_id
            issue_title = opened_issue[1]  # issue_title
            issue_body = opened_issue[2]  # issue_body
            created_at = opened_issue[3]  # created_at

            # Insert the newly opened issue into the database
            insert_issue_to_db(repo_full_name, issue_id, issue_title, issue_body, created_at)

        # Continue with other actions (severity prediction, comment creation)
        code_files = fetch_all_code_files(repo_full_name)

        input_issue_title = issue_title
        input_issue_body = issue_body
        input_issue_data_for_model = input_issue_title + "\n" + input_issue_body

        issue_chunks = chunkify(issues_data, 4)
        pool = multiprocessing.Pool(processes=4)

        duplicate_detection_task = partial(process_issues_chunk, input_issue_data_for_model)
        results = pool.map(duplicate_detection_task, issue_chunks)

        pool.close()
        pool.join()

        duplicate_issue_list = [issue for result in results for issue in result]

        BRSeverity = SeverityPrediction(input_issue_data_for_model)

        create_comment(repo_full_name, issue_number, duplicate_issue_list, BRSeverity)
        CreateCommentBL(repo_full_name, issue_number, code_files)


def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]


def process_issues_chunk(input_issue_data_for_model, issues_chunk):
    duplicate_issue_list = []
    
    process_name = multiprocessing.current_process().name

    for issue in issues_chunk:
        issue_id = issue['number']
        issue_title = issue['title']
        issue_body = issue['body']
        issue_labels = [label['name'] for label in issue.get('labels', [])]
        issue_url = issue['html_url']

        if issue_title is None:
            issue_title = ""
        if issue_body is None:
            issue_body = ""

        issue_data_for_model = issue_title + "\n" + issue_body

        print(f"Process {process_name} is handling issue number {issue_id}")

        duplicatePrediction = DuplicateDetection(input_issue_data_for_model, issue_data_for_model)

        if duplicatePrediction == [1]:
            duplicate_issue_list.append({
                "issue_id": issue_id,
                "issue_title": issue_title,
                "issue_url": issue_url,
                "issue_label": issue_labels,
            })
    
    print(f"Process {process_name} processed {len(issues_chunk)} issues in total.")
    return duplicate_issue_list
