import concurrent.futures

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

        # Split the issues_data (excluding the first one) into 4 parts for parallel processing
        issues_to_process = issues_data[1:]
        num_issues = len(issues_to_process)
        split_size = max(1, num_issues // 4)
        issue_chunks = [issues_to_process[i:i + split_size] for i in range(0, num_issues, split_size)]

        def analyze_issues(issue_chunk):
            local_duplicate_list = []
            for issue in issue_chunk:
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

                duplicatePrediction = DuplicateDetection(input_issue_data_for_model, issue_data_for_model)

                if duplicatePrediction == [1]:
                    local_duplicate_list.append({
                        "issue_id": issue_id,
                        "issue_title": issue_title,
                        "issue_url": issue_url,
                        "issue_label": issue_labels,
                    })
            return local_duplicate_list

        # Use ProcessPoolExecutor for concurrent processing
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Submit each chunk for parallel processing
            futures = [executor.submit(analyze_issues, chunk) for chunk in issue_chunks]

            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                result = future.result()
                print(f"Chunk {i + 1} processed: {len(result)} duplicates found.")
                duplicate_issue_list.extend(result)

        BRSeverity = SeverityPrediction(input_issue_data_for_model)

        create_comment(repo_full_name, issue_number, duplicate_issue_list, BRSeverity)
        CreateCommentBL(repo_full_name, issue_number, code_files)













        import requests, os, time

# Function to fetch issues from a GitHub repository with pagination
def fetch_repository_issues(repo_full_name):
    private_key = os.environ.get('GITHUB_PRIVATE_KEY')
    issues_url = f"https://api.github.com/repos/{repo_full_name}/issues"
    headers = {
        'Authorization': f'Bearer {private_key}',
    }

    issues_data = []
    page = 1
    per_page = 50  
    max_pages = 100  

    print('dhuke 1')

    while page <= max_pages: 
        # Add pagination parameters to the request
        print('dhuke 2')
        params = {
            'page': page,
            'per_page': per_page
        }

        response = requests.get(issues_url, headers=headers, params=params)
        print(response)

        if response.status_code == 200:
            issues_page_data = response.json()
            
            # Break if no more issues are returned
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