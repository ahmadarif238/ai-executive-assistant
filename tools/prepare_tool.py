# tools/prepare_tool.py
from tools.calendar_tool import get_upcoming_events
from langchain_openai import ChatOpenAI
import os
from datetime import datetime

llm = ChatOpenAI(
    temperature=0.3,
    model=os.getenv("OPENAI_MODEL", "llama3-70b-8192"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE")
)

def prepare_for_today(task: str) -> str:
    # Step 1: Fetch today's calendar events
    today_events = get_upcoming_events("today")

    if not today_events or "❌" in str(today_events):
        return "You don't have any scheduled events today, so no preparation needed."

    # Step 2: Format events for LLM
    formatted = f"Here are the user's events for today:\n{today_events}\n"
    prompt = formatted + "Based on these events, give a helpful preparation checklist."

    # Step 3: Use LLM to generate prep guidance
    result = llm.invoke(prompt)
    return str(result)
