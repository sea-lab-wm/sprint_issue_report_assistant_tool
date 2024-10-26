import os
import jwt
import time
import requests
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

load_dotenv()

def generate_jwt():
    try:
        iat = int(time.time())
        exp = iat + 60 * 10
        iss = os.environ.get('GITHUB_APP_ID')

        with open('sprint-issue-report-assistant.2024-07-08.private-key.pem', 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        payload = {
            "iat": iat,
            "exp": exp,
            "iss": iss
        }

        # Encode JWT
        token = jwt.encode(payload, private_key, algorithm="RS256")

        # Decode the token if it is in bytes
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return token
    except Exception as e:
        print(f"Error in generate_jwt: {e}")
        raise


def get_installation_id(repo_full_name, jwt_token):
    try:
        url = f'https://api.github.com/repos/{repo_full_name}/installation'
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get(url, headers=headers)
        # print(f"Response from get_installation_id: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()['id']
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed in get_installation_id: {e}")
        print(f"Response content: {response.content}")
        raise
    except Exception as e:
        print(f"Error in get_installation_id: {e}")
        raise

def get_installation_access_token(installation_id, jwt_token):
    try:
        url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.post(url, headers=headers)
        # print(f"Response from get_installation_access_token: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()['token']
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed in get_installation_access_token: {e}")
        print(f"Response content: {response.content}")
        raise
    except Exception as e:
        print(f"Error in get_installation_access_token: {e}")
        raise

def authenticate_github_app(repo_full_name):
    try:
        jwt_token = generate_jwt()
        installation_id = get_installation_id(repo_full_name, jwt_token)
        access_token = get_installation_access_token(installation_id, jwt_token)
        return access_token
    except Exception as e:
        print(f"Error in authenticate_github_app: {e}")
        raise
