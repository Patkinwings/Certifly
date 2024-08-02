from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from .gmail_utils import get_gmail_service, send_gmail
import logging

logger = logging.getLogger(__name__)

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
                logger.error(f"Error sending email: {str(e)}")
                if not self.fail_silently:
                    raise
        return sent_count

    def _send(self, email_message):
        creds = get_gmail_service(
            settings.GMAIL_OAUTH_CLIENT_ID,
            settings.GMAIL_OAUTH_CLIENT_SECRET,
            settings.GMAIL_OAUTH_REFRESH_TOKEN
        )
        to = email_message.to[0]  # Assuming single recipient
        subject = email_message.subject
        body = email_message.body
        sender = email_message.from_email

        success = send_gmail(sender, to, subject, body, creds)
        if not success and not self.fail_silently:
            raise Exception("Failed to send email")