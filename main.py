# ai_executive_assistant/main.py

import os
from dotenv import load_dotenv
from agent.graph_agent import run_agent
from tools.contacts import get_email_for_contact
from tools.gmail_sender import send_email
import re

load_dotenv()

def display_result(output):
    if isinstance(output, dict) and "content" in output:
        print("\n✅ Result:\n", output["content"].strip(), "\n")
    else:
        print("\n✅ Result:\n", str(output).strip(), "\n")

def email_interaction_flow(output, original_task):
    if not isinstance(output, dict) or "content" not in output:
        display_result(output)
        return

    email_body = output["content"]
    recipient_email = output.get("recipient")
    subject = "Quick Update"

    # Try to extract subject if present
    subject_match = re.search(r"Subject:\s*(.*)", email_body)
    if subject_match:
        subject = subject_match.group(1).strip()

    # Extract body (after "Body:")
    body_match = re.search(r"Body:\s*(.*)", email_body, re.DOTALL)
    email_text = body_match.group(1).strip() if body_match else email_body

    print("\n📝 Drafted Email:\n")
    print(f"To: {recipient_email or '[Not specified]'}")
    print(f"Subject: {subject}")
    print(f"Body:\n{email_text}")

    while True:
        user_input = input("\nWould you like to [send], [edit], [add more], or [cancel]? ").strip().lower()

        if user_input == "send":
            if not recipient_email:
                recipient_email = input("Enter recipient email: ").strip()
            send_email(to=recipient_email, subject=subject, body=email_text)
            print("✅ Email sent.")
            break

        elif user_input == "edit":
            print("✏️  Enter the revised email (end with a blank line):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            email_body = "\n".join(lines)
            print("✅ Email updated.")

        elif user_input == "add more":
            print("➕ Enter additional content to append (end with a blank line):")
            additions = []
            while True:
                line = input()
                if line == "":
                    break
                additions.append(line)
            email_body += "\n\n" + "\n".join(additions)
            print("✅ Content added.")

        elif user_input == "cancel":
            print("❌ Email sending cancelled.")
            break

        else:
            print("Please type: send / edit / add more / cancel.")

def main():
    print("\n🤖 Welcome to your AI Executive Assistant")
    print("Type your request or type 'exit' to quit.\n")

    while True:
        task = input("🗣️  What would you like me to help you with?\n> ").strip()
        if task.lower() in {"exit", "quit"}:
            print("👋 Goodbye! Have a productive day.")
            break

        normalized_task = task.lower().replace("’", "'").strip()
        output = run_agent(task)

        if any(phrase in normalized_task for phrase in ["write an email", "send an email", "email to", "send mail", "compose email"]):
            email_interaction_flow(output, task)
        else:
            display_result(output)

if __name__ == "__main__":
    main()
