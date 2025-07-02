from utils.auth import authenticate_google
from datetime import datetime, timedelta
import dateparser
import re

def fetch_events(start_time: datetime, end_time: datetime) -> str:
    try:
        service = authenticate_google("calendar", "v3")
        now_iso = start_time.isoformat() + "Z"
        end_iso = end_time.isoformat() + "Z"

        events_result = service.events().list(
            calendarId="primary",
            timeMin=now_iso,
            timeMax=end_iso,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        events = events_result.get("items", [])
        if not events:
            return "📅 No events found during that time."

        response = "📅 Your Events:\n"
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "No Title")
            response += f"- {summary} at {start}\n"

        return response
    except Exception as e:
        return f"⚠️ Error fetching calendar events: {e}"


def get_upcoming_events(task: str = "") -> str:
    task = task.lower()
    now = datetime.utcnow()

    if "today" in task:
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        return fetch_events(start, end)

    elif "tomorrow" in task:
        start = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        return fetch_events(start, end)

    elif "this week" in task:
        start = now
        end = now + timedelta(days=7)
        return fetch_events(start, end)

    elif "next week" in task:
        start = now + timedelta(days=(7 - now.weekday()))
        end = start + timedelta(days=7)
        return fetch_events(start, end)

    elif "this weekend" in task:
        saturday = now + timedelta((5 - now.weekday()) % 7)
        sunday = saturday + timedelta(days=1)
        return fetch_events(saturday, sunday + timedelta(days=1))

    match = re.search(r"on (.+)", task)
    cleaned_task = match.group(1) if match else task

    parsed_date = dateparser.parse(cleaned_task, settings={"PREFER_DATES_FROM": "future", "RELATIVE_BASE": now})
    if parsed_date:
        start = parsed_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        return fetch_events(start, end)
    else:
        return "❌ I couldn't understand the date. Try 'next Monday' or 'on July 3'."
