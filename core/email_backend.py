from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import base64
import smtplib

class GmailOAuth2Backend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.fail_silently = fail_silently

    def send_messages(self, email_messages):
        sent_count = 0
        for message in email_messages:
            try:
                self._send(message)
                sent_count += 1
            except Exception as e:
                if not self.fail_silently:
                    raise
        return sent_count

    def _send(self, email_message):
        creds = Credentials.from_authorized_user_info(
            {
                "client_id": settings.GMAIL_OAUTH_CLIENT_ID,
                "client_secret": settings.GMAIL_OAUTH_CLIENT_SECRET,
                "refresh_token": settings.GMAIL_OAUTH_REFRESH_TOKEN,
            },
            ["https://mail.google.com/"]
        )

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.docmd('AUTH', 'XOAUTH2 ' + creds.token)
            server.send_message(email_message)
            server.quit()
        except Exception as e:
            if not self.fail_silently:
                raise