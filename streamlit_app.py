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
st.set_page_config(page_title="AI Executive Agent", page_icon="🤖", layout="wide")

# --- TTS Engine Setup ---
engine = pyttsx3.init()
engine.setProperty("rate", 175)

def speak_text(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"🔊 Speech Error: {e}")

# --- Voice Input ---
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

# --- Clean Output Helpers ---
def clean_markdown(text):
    return text.replace("*", "").replace("```", "").replace("\\n", "\n").replace("\\", "").strip()

def clean_for_speech(text):
    return text.replace("*", "").replace("```", "").replace("\\n", ". ").replace("\\", "").replace("\n", ". ").strip()

# --- Dummy Email Sender (Replace with real logic) ---
def send_email_function(result):
    # Replace with your actual email sending code
    st.info("📤 Simulated email send...")
    return True

def parse_and_send_edited_email(text):
    # Example: parse subject, recipient, body from text and send
    st.info("📤 Simulated sending edited email...")
    return True

# --- Sidebar Settings ---
with st.sidebar:
    st.title("⚙️ Settings")
    voice_input_enabled = st.session_state.get("voice_enabled", False)
    if st.button("🎙️ Toggle Voice Assistant", key="voice_toggle"):
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

# --- App Title ---
st.title("🤖 Voice-Enabled AI Executive Agent")
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

    # --- Clean and Display Output ---
    if isinstance(result, dict) and "content" in result:
        raw_response = result["content"]
    else:
        raw_response = str(result)

    clean_display = clean_markdown(raw_response)
    clean_speak = clean_for_speech(raw_response)

    st.markdown("## ✅ Assistant's Response")
    st.markdown(f"#### 🧠 Output\n\n{clean_display}")

    if auto_speak_enabled and clean_speak:
        speak_text(clean_speak)

    # --- Email Confirmation Logic ---
    if "To:" in clean_display and "Subject:" in clean_display and "Body:" in clean_display:
        st.markdown("### ✉️ Do you want to send this email?")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Send Email"):
                try:
                    send_result = send_email_function(result)
                    st.success("📤 Email sent successfully!")
                    if auto_speak_enabled:
                        speak_text("Your email has been sent.")
                except Exception as e:
                    st.error(f"Failed to send email: {e}")

        with col2:
            if st.button("📝 Edit Email"):
                st.session_state.draft_email = clean_display
                st.text_area("✏️ Edit your email before sending:", value=st.session_state.draft_email, key="edited_email")

                if st.button("📨 Send Edited Email"):
                    try:
                        send_result = parse_and_send_edited_email(st.session_state.edited_email)
                        st.success("📤 Edited email sent!")
                        if auto_speak_enabled:
                            speak_text("Your edited email has been sent.")
                    except Exception as e:
                        st.error(f"Failed to send edited email: {e}")

        with col3:
            if st.button("❌ Cancel Email"):
                st.info("Email sending canceled.")
                if auto_speak_enabled:
                    speak_text("Email sending canceled.")

    # --- Optional Debug Info ---
    with st.expander("🧪 View Raw Agent Output"):
        st.write(result)

# --- Footer ---
st.markdown("---")
st.caption("🚀 Built with ❤️ by Arif Ahmad Khan")
