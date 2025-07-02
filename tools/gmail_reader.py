from utils.auth import authenticate_google
import base64
from email import message_from_bytes
from langchain_core.tools import tool

@tool
def get_latest_emails(task: str = "") -> str:
    """
    Fetch summaries of the most recent 5 emails from the Gmail inbox.
    """
    try:
        service = authenticate_google("gmail", "v1")
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
        messages = results.get('messages', [])

        if not messages:
            return "📭 No recent emails found."

        emails = []
        for msg in messages:
            msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            headers = msg_detail['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
            from_ = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
            date_ = next((h['value'] for h in headers if h['name'] == 'Date'), '(Unknown Date)')
            snippet = msg_detail.get('snippet', '')

            emails.append(f"📧 *Subject:* {subject}\n   *From:* {from_}\n   *Date:* {date_}\n   *Snippet:* {snippet}\n")

        return "\n".join(emails)
    except Exception as e:
        return f"⚠️ Error fetching emails: {e}"


@tool
def read_full_latest_email(task: str = "") -> str:
    """
    Read the full body content of the most recent email in the Gmail inbox.
    """
    try:
        service = authenticate_google("gmail", "v1")
        results = service.users().messages().list(userId='me', maxResults=1).execute()
        messages = results.get('messages', [])
        if not messages:
            return "📭 No recent emails found."

        msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
        payload = msg['payload']
        headers = payload.get("headers", [])

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(Unknown Sender)")

        parts = payload.get("parts", [])
        body_data = None

        for part in parts:
            if part["mimeType"] == "text/plain" and "data" in part["body"]:
                body_data = part["body"]["data"]
                break

        if not body_data:
            body_data = payload.get("body", {}).get("data")

        if body_data:
            body = base64.urlsafe_b64decode(body_data.encode('UTF-8')).decode('utf-8')
        else:
            body = "[No body content found]"

        return f"📧 *From:* {sender}\n*Subject:* {subject}\n\n📩 *Body:* {body}"
    except Exception as e:
        return f"⚠️ Error reading full email: {e}"
