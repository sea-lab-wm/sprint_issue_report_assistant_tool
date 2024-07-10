import os
import jwt
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_jwt():
    iat = int(time.time())
    exp = iat + 60 * 10
    iss = os.environ.get('GITHUB_APP_ID')

    with open('sprint-issue-report-assistant.2024-07-08.private-key.pem', 'r') as key_file:
        private_key = key_file.read()


    payload = {
        "iat": iat,
        "exp": exp,
        "iss": iss
    }

    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token



def get_installation_id(repo_full_name, jwt_token):
    url = f'https://api.github.com/repos/{repo_full_name}/installation'
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['id']



def get_installation_access_token(installation_id, jwt_token):
    url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()['token']


def authenticate_github_app(repo_full_name):
    jwt_token = generate_jwt()
    installation_id = get_installation_id(repo_full_name, jwt_token)
    access_token = get_installation_access_token(installation_id, jwt_token)
    return access_token


# Usage example
# app_id = os.getenv('GITHUB_APP_ID')
# private_key = os.getenv('GITHUB_PRIVATE_KEY').replace('\\n', '\n')
# repo_full_name = 'owner/repo'

# access_token = authenticate_github_app(app_id, private_key, repo_full_name)
# print("Access Token:", access_token)
