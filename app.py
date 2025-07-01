
# Real-Time GenAI Teleprompter (Lightweight & Plagiarism-Free)

# File: app.py
import streamlit as st
import time
import openai
import tempfile
import os
from datetime import datetime

# ========== SETUP ==========
st.set_page_config(page_title="GenAI Teleprompter", layout="wide")
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Add your OpenAI API key in .streamlit/secrets.toml

# ========== UI ELEMENTS ==========
st.title("🎤 Real-Time GenAI Teleprompter")
mic_on = st.toggle("Mic Access", value=False)
start = st.button("Start Session")
stop = st.button("Stop Session")
session_timer = st.empty()
transcript_box = st.empty()
prompt_box = st.empty()

# ========== SESSION STATE ==========
if "transcript" not in st.session_state:
    st.session_state.transcript = []
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# ========== SIMULATED TRANSCRIPTION ==========
def simulate_transcription():
    fake_lines = [
        "Hi, this is Alex from Apex Solutions.",
        "I'm reaching out to help you with your software needs.",
        "We offer customized CRM tools that scale with your business.",
        "Would you be interested in a short demo next week?"
    ]
    for line in fake_lines:
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.transcript.append(f"[{timestamp}] {line}")
        transcript_box.text("\n".join(st.session_state.transcript))
        time.sleep(2)
        fetch_suggestion("\n".join(st.session_state.transcript[-2:]))

# ========== LLM SUGGESTIONS ==========
def fetch_suggestion(latest_text):
    prompt = f"You are a helpful assistant supporting a sales agent on a call. Suggest tips or reminders.\nText: {latest_text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Support a sales agent in live calls."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=50
        )
        reply = response.choices[0].message.content.strip()
        st.session_state.suggestions.append(reply)
        prompt_box.markdown(f"**💡 Suggestion:** {reply}")
    except Exception as e:
        st.error(f"Error from LLM: {e}")

# ========== TIMER ==========
def update_timer():
    if st.session_state.start_time:
        elapsed = int(time.time() - st.session_state.start_time)
        session_timer.write(f"⏱ Session Time: {elapsed}s")

# ========== EXPORT ==========
def export_log():
    log_data = {
        "transcript": st.session_state.transcript,
        "suggestions": st.session_state.suggestions
    }
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    with open(temp_file.name, "w") as f:
        f.write("TRANSCRIPT:\n" + "\n".join(st.session_state.transcript) + "\n\nSUGGESTIONS:\n" + "\n".join(st.session_state.suggestions))
    st.download_button("📁 Download Log", data=open(temp_file.name).read(), file_name="session_log.txt")
    os.unlink(temp_file.name)

# ========== MAIN FLOW ==========
if start:
    st.session_state.start_time = time.time()
    simulate_transcription()

if stop:
    update_timer()
    export_log()
