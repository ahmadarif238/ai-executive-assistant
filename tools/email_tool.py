# tools/email_tool.py

import os
import re
from langchain_openai import ChatOpenAI
from tools.contacts import get_email_for_contact

llm = ChatOpenAI(
    temperature=0.3,
    model=os.getenv("OPENAI_MODEL", "llama3-70b-8192"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE")
)

def extract_recipient_name(task: str) -> str:
    match = re.search(r"email\s+to\s+([a-zA-Z]+)", task.lower()) or \
            re.search(r"to\s+([a-zA-Z]+)", task.lower())
    return match.group(1).lower() if match else None

def write_email(task: str) -> dict:
    name = extract_recipient_name(task)
    email_address = get_email_for_contact(name) if name else None

    if email_address:
        print(f"📬 Found email for '{name}': {email_address}")
    else:
        print(f"⚠️ Contact '{name}' not found in contacts.json.")

    prompt = f"""
You are an assistant that writes emails.

User request:
"{task}"

Generate the email in this format:
To: {email_address}
Subject: [short subject]
Body:
[full body text]
"""

    result = llm.invoke(prompt)

    return {
        "content": result.content.strip(),  # ✅ fixed
        "recipient": email_address
    }
