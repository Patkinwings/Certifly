import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

def get_gmail_service():
    try:
        creds = service_account.Credentials.from_service_account_info(
            settings.GOOGLE_SERVICE_ACCOUNT_INFO,
            scopes=['https://www.googleapis.com/auth/gmail.send']
        )
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Error creating Gmail service: {e}")
        return None

# If you need to impersonate a user, add this function:
def get_gmail_service_as_user(user_email):
    try:
        creds = service_account.Credentials.from_service_account_info(
            settings.GOOGLE_SERVICE_ACCOUNT_INFO,
            scopes=['https://www.googleapis.com/auth/gmail.send'],
            subject=user_email
        )
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Error creating Gmail service as {user_email}: {e}")
        return None