import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from django.conf import settings

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.send'])
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
                ['https://www.googleapis.com/auth/gmail.send'])
            flow.run_local_server(port=8080)
            creds = flow.credentials

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds