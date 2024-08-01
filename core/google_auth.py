import json
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
import base64

logger = logging.getLogger(__name__)

def get_gmail_service():
    try:
        creds = service_account.Credentials.from_service_account_info(
            json.loads(settings.GOOGLE_SERVICE_ACCOUNT_INFO),
            scopes=['https://www.googleapis.com/auth/gmail.send']
        )
        delegated_credentials = creds.with_subject('certiflyreset@gmail.com')
        service = build('gmail', 'v1', credentials=delegated_credentials)
        logger.info("Gmail service created successfully")
        return service
    except Exception as e:
        logger.error(f"Error creating Gmail service: {e}")
        return None

def get_gmail_service_as_user(user_email):
    try:
        creds = service_account.Credentials.from_service_account_info(
            json.loads(settings.GOOGLE_SERVICE_ACCOUNT_INFO),
            scopes=['https://www.googleapis.com/auth/gmail.send'],
            subject=user_email
        )
        service = build('gmail', 'v1', credentials=creds)
        logger.info(f"Gmail service created successfully for {user_email}")
        return service
    except Exception as e:
        logger.error(f"Error creating Gmail service as {user_email}: {e}")
        return None

def send_email(to, subject, body):
    try:
        service = get_gmail_service()
        if not service:
            logger.error("Failed to create Gmail service")
            return False

        message = {
            'raw': base64.urlsafe_b64encode(
                f"To: {to}\r\nSubject: {subject}\r\n\r\n{body}".encode()
            ).decode()
        }
        
        send_message = service.users().messages().send(userId="me", body=message).execute()
        logger.info(f"Email sent successfully. Message Id: {send_message['id']}")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False