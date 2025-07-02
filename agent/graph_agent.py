# ai_executive_assistant/agent/graph_agent.py

import os
from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

# Import tools
from tools.web_search import search_web
from memory.llama_index_memory import query_documents
from tools.prepare_tool import prepare_for_today
from tools.calendar_tool import get_upcoming_events
from tools.gmail_reader import get_latest_emails, read_full_latest_email
from tools.email_tool import write_email

# Define state schema
class AgentState(TypedDict):
    input: str
    output: str

# Tool definitions
search_tool = Tool(
    name="WebSearch",
    func=search_web,
    description="Useful for answering general questions by searching the web."
)

doc_tool = Tool(
    name="DocQA",
    func=query_documents,
    description="Useful for answering questions based on uploaded documents."
)

prepare_tool = Tool(
    name="PrepareToday",
    func=prepare_for_today,
    description="Checks today’s calendar and gives helpful preparation advice."
)

calendar_tool = Tool(
    name="Calendar",
    func=get_upcoming_events,
    description="Use this to fetch upcoming Google Calendar events."
)

gmail_reader_tool = Tool(
    name="GmailLatest",
    func=read_full_latest_email,
    description="Use this to read the latest email with full body text."
)

gmail_tool = Tool(
    name="GmailOverview",
    func=get_latest_emails,
    description="Use this to get recent emails from your Gmail inbox."
)

email_writer_tool = Tool(
    name="WriteEmail",
    func=write_email,
    description="Composes an email based on user request."
)

# Groq-compatible LLM
llm = ChatOpenAI(
    temperature=0.3,
    model=os.getenv("OPENAI_MODEL", "llama3-70b-8192"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE")
)

# Agent decision logic
def agent_node(state):
    task = state["input"].lower()
    print(f"Thinking... [Input: {task}]")

    if "weather" in task or "temperature" in task or "forecast" in task:
        return {"output": search_tool.run(task)}

    if any(kw in task for kw in ["document", "pdf", "summarize", "chapter", "what does", "based on", "say about"]):
        result = doc_tool.run(task)
        return {"output": result.get("answer", str(result)) if isinstance(result, dict) else str(result)}

    if "prepare" in task and "today" in task:
        return {"output": prepare_tool.run(task)}

    if "search" in task or "find" in task:
        return {"output": search_tool.run(task)}

    if "write an email" in task or "send an email" in task:
        result = email_writer_tool.run(task)
        return {"output": result} if isinstance(result, dict) else {"output": {"content": str(result)}}

    if any(kw in task for kw in [
        "calendar", "event", "schedule", "appointment", "meeting",
        "on my calendar", "on my schedule", "do i have", "anything on", "planned"
    ]):
        return {"output": calendar_tool.run(task)}

    # Place more specific Gmail command first
    if "latest email" in task or "read my email" in task or "full email" in task or "last email" in task:
        return {"output": gmail_reader_tool.run(task)}

    if "emails" in task or "gmail" in task or "recent emails" in task:
        return {"output": gmail_tool.run(task)}

    return {"output": llm.invoke(f"Task: {task}. What should I do?")}

# Build agent graph
workflow = StateGraph(AgentState)
workflow.add_node("start", agent_node)
workflow.set_entry_point("start")
app = workflow.compile()

def run_agent(task):
    result = app.invoke({"input": task})
    return result["output"]
