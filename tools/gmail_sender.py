from email.mime.text import MIMEText
import base64
from utils.auth import authenticate_google

def send_email(to, subject, body):
    service = authenticate_google("gmail", "v1")

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    send_message = {'raw': raw}
    sent = service.users().messages().send(userId="me", body=send_message).execute()
    return f"✅ Email sent to {to} (ID: {sent['id']})"
