from Issue_Indexer.getAllIssues import fetch_repository_issues
from .getCodeFiles import fetch_all_code_files
from Feature_Components.dupBRDetection import DuplicateDetection
from Feature_Components.BRSeverityPred import SeverityPrediction
from .createCommentBugLocalization import CreateCommentBL, BLStartingCommentForWaiting
from .createComment import create_comment, DupStartingCommentForWaiting
import multiprocessing
from functools import partial
from .app_authentication import authenticate_github_app
from .createComment import create_label
from Feature_Components.bugLocalization import BugLocalization
from Data_Storage.dbOperations import create_table_if_not_exists, is_table_exists, insert_issue_to_db, fetch_all_bug_reports_from_db, delete_issue_from_db

def process_issue_event(repo_full_name, input_issue, action):
    try:    
        if action == 'opened':
            if not is_table_exists(repo_full_name):
                print(f"Table for {repo_full_name} does not exist. Creating the table and fetching issues.")
                create_table_if_not_exists(repo_full_name)

                issues_data = fetch_repository_issues(repo_full_name)
                for issue in issues_data:

                    if issue['number'] == input_issue['issue_number']:
                        print(f"Skipping issue {issue['number']} as it matches the input issue title.")
                        continue  

                    issue_id = issue['number']
                    issue_title = issue['title'] or ""
                    issue_body = issue['body'] or ""
                    created_at = issue['created_at']  
                    issue_url = issue['html_url']  
                    issue_labels = [label['name'] for label in issue.get('labels', [])]

                    insert_issue_to_db(repo_full_name, issue_id, issue_title, issue_body, created_at, issue_url, issue_labels)
                issues_data = fetch_all_bug_reports_from_db(repo_full_name)
                if issues_data:
                    DupStartingCommentForWaiting(repo_full_name, input_issue['issue_number'])

            else:
                print(f"Table for {repo_full_name} already exists. Fetching issues from the database.")
                issues_data = fetch_all_bug_reports_from_db(repo_full_name)
                if issues_data:
                    DupStartingCommentForWaiting(repo_full_name, input_issue['issue_number'])


            code_files = fetch_all_code_files(repo_full_name, input_issue['issue_branch'])

            input_issue_title = input_issue['issue_title'] or ""
            input_issue_body = input_issue['issue_body'] or ""
            input_issue_data_for_model = input_issue_title + "\n" + input_issue_body

            issue_chunks = chunkify(issues_data, 4)
            
            pool = multiprocessing.Pool(processes=4)

            duplicate_detection_task = partial(process_issues_chunk, input_issue_data_for_model)
            results = pool.map(duplicate_detection_task, issue_chunks)

            pool.close()
            pool.join()

            duplicate_issue_list = [issue for result in results for issue in result]

            try:
                    insert_issue_to_db(
                        repo_full_name,
                        input_issue['issue_number'],
                        input_issue['issue_title'],
                        input_issue['issue_body'],
                        input_issue['created_at'],
                        input_issue['issue_url'],
                        input_issue['issue_labels']
                    )
                    
            except Exception as e:
                print(f"An error occurred while inserting the issue: {e}")

            auth_token = authenticate_github_app(repo_full_name)

            # Severity Prediction
            BRSeverity = SeverityPrediction(input_issue_data_for_model)
            create_label(repo_full_name, input_issue['issue_number'], BRSeverity, auth_token)

            if duplicate_issue_list:
                duplicate_issue_list = duplicate_issue_list[:10]
                create_comment(repo_full_name, input_issue['issue_number'], duplicate_issue_list)
            
            paths_only = [file['path'] for file in code_files]

            # Bug localization 
            if paths_only:
                BLStartingCommentForWaiting(repo_full_name, input_issue['issue_number'])
                buggy_code_files_list = BugLocalization(input_issue_data_for_model, repo_full_name, paths_only)
                CreateCommentBL(repo_full_name, input_issue['issue_branch'], input_issue['issue_number'], buggy_code_files_list, paths_only)
        
        elif action == 'deleted':
            delete_issue_from_db(repo_full_name, input_issue['issue_number'])
            print(f"Deleted issue {input_issue['issue_number']} from the database.")
    except Exception as e:
        print(f"An error occurred in process_issue_event: {e}")




def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]


def process_issues_chunk(input_issue_data_for_model, issues_chunk):
    duplicate_issue_list = []
    process_name = multiprocessing.current_process().name

    for issue in issues_chunk:
        issue_id = issue[0]     
        issue_title = issue[1]  
        issue_body = issue[2]
        issue_created = issue[3]    
        issue_url = issue[4]
        issue_labels = issue[5]

        issue_title = issue_title or ""
        issue_body = issue_body or ""
        issue_data_for_model = issue_title + "\n" + issue_body

        print(f"Process {process_name} is handling issue number {issue_id}")

        duplicatePrediction = DuplicateDetection(input_issue_data_for_model, issue_data_for_model, issue_id)

        if duplicatePrediction == [1]:
            duplicate_issue_list.append({
                "issue_id": issue_id,
                "issue_title": issue_title,
                "issue_created": issue_created,
                "issue_url": issue_url,
                "issue_label": issue_labels,
            })
    
    print(f"Process {process_name} processed {len(issues_chunk)} issues in total.")
    return duplicate_issue_list  