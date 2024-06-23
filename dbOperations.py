from sqlalchemy.exc import OperationalError
from models import BugReport
from db_config import db
import json

class BugReportObject:
    def __init__(self, issueId, issueTitle, issueBody, issueURL, embedding):
        self.issueId = issueId
        self.issueTitle = issueTitle
        self.issueBody = issueBody
        self.issueURL = issueURL
        self.embedding = embedding



def is_bug_report_table_empty():
    try:
        first_bug_report = BugReport.query.first()
        return first_bug_report is None
    except OperationalError:
        return True
    


def insert_issue_to_db(issue_id, issue_title, issue_body, issue_url, embedding):
    try:
        embedding_list = embedding.tolist()
        embedding_json = json.dumps(embedding_list)

        bug_report = BugReport(
            issueId=issue_id,
            issueTitle=issue_title,
            issueBody=issue_body,
            issueURL=issue_url,
            embedding=embedding_json
        )

        db.session.add(bug_report)
        db.session.commit()
        print('post success')
        return True
    except Exception as e:
        print(f"Error inserting data into the database: {str(e)}")
        return False
    


def fetch_all_bug_reports():
    print('fetching bug reports')
    try:
        bug_reports = BugReport.query.all()
        bug_report_objects = []

        for bug_report in bug_reports:
            bug_report_objects.append(BugReportObject(
                issueId=bug_report.issueId,
                issueTitle=bug_report.issueTitle,
                issueBody=bug_report.issueBody,
                issueURL=bug_report.issueURL,
                embedding=bug_report.embedding
            ))

        return bug_report_objects
    except Exception as e:
        print(f"Error fetching bug reports from the database: {str(e)}")
        return []