import sqlite3
from datetime import datetime

def connect_db():
    conn = sqlite3.connect('issues.db')
    return conn

def create_table_if_not_exists(repo_full_name):
    conn = connect_db()
    cur = conn.cursor()

    query = f"""
    CREATE TABLE IF NOT EXISTS "{repo_full_name}" (
        issue_id INTEGER PRIMARY KEY,
        issue_title TEXT NOT NULL,
        issue_body TEXT,
        created_at DATETIME NOT NULL,
        issue_url TEXT,
        issue_labels TEXT
    );
    """
    cur.execute(query)
    conn.commit()
    conn.close()

def is_table_exists(repo_full_name):
    conn = connect_db()
    cur = conn.cursor()

    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{repo_full_name}';"
    cur.execute(query)
    result = cur.fetchone()
    conn.close()
    return result is not None

def insert_issue_to_db(repo_full_name, issue_id, issue_title, issue_body, created_at, issue_url, issue_labels):
    conn = connect_db()
    cur = conn.cursor()

    if isinstance(created_at, datetime):
        created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')

    issue_labels_str = ','.join(issue_labels)

    query = f"""
    INSERT INTO "{repo_full_name}" (issue_id, issue_title, issue_body, created_at, issue_url, issue_labels)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    cur.execute(query, (issue_id, issue_title, issue_body, created_at, issue_url, issue_labels_str))
    conn.commit()
    conn.close()

    print(f'Issue {issue_id} inserted successfully in table {repo_full_name}')

def fetch_all_bug_reports_from_db(repo_full_name):
    try:
        conn = connect_db()
        cur = conn.cursor()

        query = f"SELECT * FROM '{repo_full_name}';"
        cur.execute(query)
        issues = cur.fetchall()
        conn.close()

        return issues

    except Exception as e:
        print(f"An error occurred while fetching bug reports from the database: {str(e)}")
        return None


def delete_issue_from_db(repo_full_name, issue_id):
    conn = connect_db()
    cur = conn.cursor()

    query = f"DELETE FROM '{repo_full_name}' WHERE issue_id = ?;"
    
    try:
        cur.execute(query, (issue_id,))
        conn.commit()
        if cur.rowcount > 0:
            print(f'Issue {issue_id} deleted successfully from table {repo_full_name}')
        else:
            print(f'Issue {issue_id} not found in table {repo_full_name}')
    except Exception as e:
        print(f"Error occurred while deleting issue: {e}")
    finally:
        conn.close()

def delete_table(repo_full_name):
    try:
        with sqlite3.connect('issues.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {repo_full_name}")
            print(f"Table for {repo_full_name} deleted.")
    except Exception as e:
        print(f"Error deleting table {repo_full_name}: {e}")
