import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

def sendEmail(to_email, docket_id):
    try:
        # Info
        sender_email = os.getenv('EMAIL')
        sender_password = os.getenv('PASSWORD')
        # Content
        subject = "Mirrulations Download Started!"
        message = "Your download for docket " + docket_id + " has begun and will be done shortly. Hang tight!"
        # Connect to the Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            # Compose the email
            email = f'Subject: {subject}\n\n{message}'
            # Send the email
            server.sendmail(sender_email, to_email, email)
        return "Email sent successfully!"
    except Exception as e:
        print(f"An error occurred while sending email: {e}")
        return f"Failed to send email: {e}"

