import os
import base64
from dotenv import load_dotenv
from email.message import EmailMessage
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

def load_credentials():
    """Load credentials from the JSON file."""
    credentials_file = os.getenv('CREDENTIALS_FILE_PATH')
    return service_account.Credentials.from_service_account_file(credentials_file)

def gmail_send_email(to_email):
    """Send an email using the Gmail API."""
    credentials = load_credentials()

    try:
        # Create Gmail API client
        service = build("gmail", "v1", credentials=credentials)
        message = EmailMessage()
        message.set_content("This is an automated email")
        message["To"] = to_email
        message["From"] = os.getenv('SENDER_EMAIL')
        message["Subject"] = "Automated email"
        # Encode message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        # Send the email
        service.users().messages().send(userId="me", body=create_message).execute()
        print("Email sent successfully!")
    except HttpError as error:
        print(f"An error occurred: {error}")
