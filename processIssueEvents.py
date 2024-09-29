from getAllIssues import fetch_repository_issues
from getCodeFiles import fetch_all_code_files
from dupBRDetection import DuplicateDetection
from BRSeverityPred import SeverityPrediction
from createCommentBugLocalization import CreateCommentBL
from createComment import create_comment
import multiprocessing
from functools import partial



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

        issue_chunks = chunkify(issues_data[1:], 4)  

        pool = multiprocessing.Pool(processes=4)


        duplicate_detection_task = partial(process_issues_chunk, input_issue_data_for_model)
        # Execute the duplicate detection concurrently on the chunks
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
    
    # Get the current process name
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

        # Print which process is handling this issue number
        print(f"Process {process_name} is handling issue number {issue_id}")

        # Call the duplicate detection model
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