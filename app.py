import streamlit as st
import os
import whisper
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import tempfile

# Page Configuration
st.set_page_config(page_title="AI Call Analyzer", page_icon="🎧", layout="wide")

# Title and Description
st.title("🎧 AI Call Analyzer (Design Thinking)")
st.markdown("""
Upload a call recording (Audio) to analyze it using **Whisper** (Transcription) and **Llama-3** (Analysis).
This tool provides deep insights into Founder Context, Emotional State, and more.
""")

# Load Environment Variables
load_dotenv()

# Sidebar for API Key
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Hugging Face API Key", type="password", help="Enter your HF Token here if not set in Secrets/Env")

# Helper: Get API Key
def get_api_key():
    # Priority: 1. User Input, 2. Streamlit Secrets, 3. Local Env
    if api_key:
        return api_key
    if "HUGGINGFACE_API_KEY" in st.secrets:
        return st.secrets["HUGGINGFACE_API_KEY"]
    if os.getenv("HUGGINGFACE_API_KEY"):
        return os.getenv("HUGGINGFACE_API_KEY")
    return None

# System Prompt (Same as before)
SYSTEM_PROMPT = """
You are not a chatbot.
You are a Design Thinking Fellow analyzing a real conversation between a team member and a business founder.

Your job is NOT to summarize the conversation.
Your job is to deeply understand what was FELT, not just what was SAID.

Analyze the conversation using the following mindset:

1. Founder Context Awareness
   - Assume the founder is busy, risk-aware, and mentally filtering noise.
   - Identify what pressure, hesitation, or expectation the founder might be carrying at each moment.

2. Emotional State Mapping
   - Track how the founder’s emotional state shifts during the conversation
     (curious → guarded → disengaged / open → rushed → skeptical, etc.).
   - Explain WHY those shifts happened.

3. Control & Power Balance
   - Identify who had control of the conversation at different points.
   - Explain moments where control was lost or forcefully taken.

4. Trust & Risk Perception
   - Analyze how each statement either reduced or increased the founder’s perceived risk.
   - Focus on clarity, time respect, and relevance — not politeness.

5. Discomfort & Exit Signals
   - Identify subtle discomfort signals such as pauses, vague affirmations,
     topic changes, or suggestions to “email later.”
   - Explain what these signals actually mean in a real business context.

6. Pressure Response of the Caller
   - Identify how the caller behaved under pressure
     (over-explaining, justifying, selling, rushing, or grounding the conversation).
   - Explain what this reveals about the caller’s maturity.

7. How I Would Speak Differently
   - Do NOT write a full script.
   - Instead, explain what you would remove, reduce, or reframe to give
     the founder more control and mental comfort.

8. My Conversation Analysis Framework
   - Build a short, original framework that analyzes conversations based on:
     emotion, control, risk, energy exchange, and exit signals.
   - Focus on understanding human behavior, not communication theory.

Important:
- Avoid generic advice, soft language, or textbook communication tips.
- Write like a thoughtful human who understands business pressure.
- Prioritize empathy, clarity, and respect for mental space.
- The goal is insight, not perfection.

End the analysis with one reflective line about what this conversation teaches
about trust, maturity, or human interaction in real-world business settings.
"""

# Cached Whisper Function
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

def transcribe_audio(audio_path):
    model = load_whisper_model()
    result = model.transcribe(audio_path)
    return result["text"]

def analyze_with_llama(transcript, token, language="English"):
    client = InferenceClient(token=token)
    model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
    
    # Language specific instruction
    lang_instruction = ""
    if language == "Hinglish":
        lang_instruction = "5. OUTPUT LANGUAGE: Generate the ENTIRE analysis in HINGLISH (Natural mix of Hindi and English). Keep technical headers in English, but explain the insights in Hinglish (e.g., 'Founder kaafi guarded lag raha tha')."
    else:
        lang_instruction = "5. OUTPUT LANGUAGE: Generate the analysis in standard professional ENGLISH."

    user_message = f"""
Here is the raw transcript of a real call. 
Your task is to analyze it using the Design Thinking framework provided in the system prompt.

RULES:
1. Do NOT generate any new dialogue or conversation.
2. Do NOT repeat the transcript.
3. OUTPUT ONLY the analysis sections (1-8).
4. If the transcript is empty or unclear, say "Transcript is unclear".
{lang_instruction}

--- TRANSCRIPT BEGINS ---
{transcript}
--- TRANSCRIPT ENDS ---

Analyze the transcript now:
"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]
    
    response = client.chat_completion(
        model=model_id,
        messages=messages,
        max_tokens=2500,
        temperature=0.3
    )
    return response.choices[0].message.content

# Main UI
uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "m4a", "awb", "ogg", "aac", "flac", "amr", "wma", "mp4"])

# Language Selection
language = st.radio("Select Report Language:", ["English", "Hinglish"], horizontal=True)

if uploaded_file is not None:
    # Save temp file
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.audio(file_path, format="audio/wav")
    
    if st.button("Analyze Call"):
        token = get_api_key()
        if not token:
            st.error("Please provide a Hugging Face API Key in the sidebar or env variables.")
        else:
            try:
                with st.spinner(f"🎧 Transcribing & Analyzing in {language}..."):
                    transcript = transcribe_audio(file_path)
                
                with st.expander("View Transcript"):
                    st.text(transcript)
                
                with st.spinner("🧠 Generating Analysis..."):
                    analysis = analyze_with_llama(transcript, token, language)
                
                st.subheader("✨ Design Thinking Analysis Report")
                st.markdown(analysis)
                
                # Download Button
                st.download_button(
                    label="Download Report as Text",
                    data=analysis,
                    file_name=f"{uploaded_file.name}_analysis.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
