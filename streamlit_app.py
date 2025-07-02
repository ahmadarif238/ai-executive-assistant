import os
import platform
import streamlit as st
import pyttsx3
from dotenv import load_dotenv
from agent.graph_agent import run_agent
import speech_recognition as sr

# --- Load Environment Variables ---
load_dotenv()

# --- Streamlit Config ---
st.set_page_config(page_title="AI Executive Assistant", page_icon="🤖", layout="wide")

# --- TTS Engine Setup ---
engine = pyttsx3.init()
engine.setProperty("rate", 175)

def speak_text(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"🔊 Speech Error: {e}")

# --- Voice Input Function ---
def get_voice_input():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    try:
        with mic as source:
            st.info("🎙️ Listening... Please speak clearly.")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError as e:
        return f"Error with speech recognition: {e}"
    except Exception as e:
        return f"🎤 Microphone error: {e}"

# --- Helper: Clean Response ---
def clean_markdown(text):
    return text.replace("*", "").replace("```", "").replace("\\n", "\n").replace("\\", "").strip()

def clean_for_speech(text):
    return text.replace("*", "").replace("```", "").replace("\\n", ". ").replace("\\", "").replace("\n", ". ").strip()

# --- Sidebar Settings ---
with st.sidebar:
    st.title("⚙️ Settings")
    voice_input_enabled = st.session_state.get("voice_enabled", False)
    voice_input_toggle = st.button("🎙️ Toggle Voice Assistant", key="voice_toggle")

    if voice_input_toggle:
        voice_input_enabled = not voice_input_enabled
        st.session_state.voice_enabled = voice_input_enabled

    auto_speak_enabled = st.toggle("🔊 Speak Responses", value=st.session_state.get("speak_enabled", True), key="speak_toggle")
    st.session_state.speak_enabled = auto_speak_enabled

    st.markdown("---")
    st.markdown("📌 **Supported Features:**")
    st.markdown("""
- 📧 **Read Latest Emails**  
- 📤 **Send Email to Anyone**  
- 📅 **View Google Calendar Events**  
- 🌐 **Search the Web**  
- 📄 **Ask Questions in Uploaded Documents**  
- 🧠 **Ask Any General Query**
""")

# --- App Title & Header ---
st.title("🤖 Voice-Enabled AI Executive Assistant")
st.markdown("Use text or voice to access all your tools from one place.")

# --- Input Section ---
st.markdown("## 💬 Input Panel")

task = ""
if voice_input_enabled:
    if st.button("🎙️ Speak Now"):
        task = get_voice_input()
        st.success(f"🗣️ You said: `{task}`")
else:
    task = st.text_input("✍️ Or type your request here:")

# --- Agent Execution ---
if task:
    st.markdown("## 🧠 Processing...")
    with st.spinner("Thinking..."):
        try:
            result = run_agent(task)
        except Exception as e:
            st.error(f"❌ Agent Error: {e}")
            st.stop()

    # Clean response
    # --- Clean and Normalize Agent Response ---
    if isinstance(result, dict) and "content" in result:
        raw_response = result["content"]
    else:
        raw_response = str(result)

    clean_display = clean_markdown(raw_response)
    clean_speak = clean_for_speech(raw_response)


    # --- Display Result ---
    st.markdown("## ✅ Assistant's Response")
    st.markdown(f"#### 🧠 Output\n\n{clean_display}")

    if auto_speak_enabled and clean_speak:
        speak_text(clean_speak)

    # --- Optional Debug View ---
    with st.expander("🧪 View Raw Agent Output"):
        st.write(result)

# --- Footer ---
st.markdown("---")
st.caption("🚀 Built by Arif Ahmad Khan | Powered by Python, Streamlit, LLM, Gmail & Calendar APIs")

