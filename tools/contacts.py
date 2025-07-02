# tools/contacts.py

CONTACTS = {
    "maaz": "muhammadmaaz724@gmail.com",
    "manager": "manager@yourcompany.com",
    # Add more contacts as needed
}

import json
import os

def get_email_for_contact(name: str) -> str:
    name = name.lower().strip()
    path = os.path.join("data", "contacts.json")
    try:
        with open(path, "r") as f:
            contacts = json.load(f)
        email = contacts.get(name)
        if email:
            print(f"📬 Found email for '{name}': {email}")
            return email
        else:
            print(f"⚠️ Contact '{name}' not found in contacts.json.")
            return None
    except Exception as e:
        print(f"❌ Error reading contacts.json: {e}")
        return None
