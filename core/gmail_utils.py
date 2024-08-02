import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import smtplib
import logging

logger = logging.getLogger(__name__)

def get_gmail_service(client_id, client_secret, refresh_token):
    creds = Credentials.from_authorized_user_info(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        },
        ["https://www.googleapis.com/auth/gmail.send"]
    )
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

def send_gmail(sender, to, subject, body, creds):
    try:
        message = MIMEText(body)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.ehlo()
        server.docmd('AUTH', 'XOAUTH2 ' + creds.token)
        server.sendmail(sender, to, message.as_string())
        server.quit()

        logger.info(f"Email sent successfully to {to}")
        return True
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return False