import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

email_user = os.getenv('EMAIL_HOST_USER')
email_password = os.getenv('EMAIL_HOST_PASSWORD')

print(f"Email user: {email_user}")
print(f"Email password: {'*' * len(email_password) if email_password else 'Not set'}")

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        print("Connected to SMTP server")
        server.ehlo()
        print("EHLO successful")
        server.starttls()
        print("STARTTLS successful")
        server.login(email_user, email_password)
        print("Login successful")
except Exception as e:
    print(f"An error occurred: {e}")