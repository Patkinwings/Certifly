import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def send_email(to, subject, body):
    logger.info(f"Attempting to send email: to={to}, subject={subject}")
    
    if not to:
        logger.error("To is None or empty")
    if not subject:
        logger.error("Subject is None or empty")
    if not body:
        logger.error("Body is None or empty")
    
    if not all([to, subject, body]):
        logger.error("One or more required parameters are None or empty")
        return False

    try:
        logger.info(f"Attempting to send email to {to}")
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [to],
            fail_silently=False,
        )
        
        logger.info("Email sent successfully")
        return True
    except Exception as e:
        logger.error(f"An error occurred while sending email: {str(e)}")
        return False