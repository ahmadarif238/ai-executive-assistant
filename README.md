# ai-executive-assistant
Voice-Enabled AI Executive Assistant with email, calendar, web search, and document querying features using LLMs
# 🤖 Voice-Enabled AI Executive Assistant

This is a smart assistant built with Python, Streamlit, and Groq's LLaMA3 model. It combines voice interaction with real-time access to:
- 🗓️ Google Calendar
- 📩 Gmail (read + send)
- 🌐 Web search
- 📄 Document summarization (PDF)
- ✉️ Smart Email Drafting

![Demo](assets/demo.gif)

---

## 🚀 Features

- 🎤 Voice input and text input
- 🗣️ gTTS-based voice output
- 🔎 Web search using LLM
- 📅 View and summarize calendar events
- 📧 Read recent emails or full content
- ✍️ Draft and send emails with editable flows
- 📚 Summarize uploaded documents

---

## 🛠️ Tech Stack

- `Python`
- `Streamlit`
- `Groq LLaMA3-70B` via LangChain
- `Google Calendar API`
- `Gmail API`
- `gTTS` + `SpeechRecognition`
- `LangGraph` + `LangChain`

---

## 🔧 Setup

```bash
git clone https://github.com/yourusername/ai-executive-assistant
cd ai-executive-assistant
pip install -r requirements.txt
