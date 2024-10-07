from db_config import db
from sqlalchemy.dialects.mysql import TEXT  

class BugReport(db.Model):
    issueId = db.Column(db.String(255), primary_key=True)
    issueTitle = db.Column(db.String(255))
    issueBody = db.Column(TEXT)  
    issueURL = db.Column(db.String(255))
    embedding = db.Column(TEXT)  

    def __init__(self, issueId, issueTitle, issueBody, issueURL, embedding):
        self.issueId = issueId
        self.issueTitle = issueTitle
        self.issueBody = issueBody
        self.issueURL = issueURL
        self.embedding = embedding