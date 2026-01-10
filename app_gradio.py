import gradio as gr
import os
import whisper
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import tempfile
import shutil

# Load Environment Variables
load_dotenv()

# System Prompt
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

# Helper/Logic Functions (Reused from app.py)
def get_api_key(user_input_key):
    # Priority: 1. User Input, 2. Local Env
    if user_input_key and user_input_key.strip():
        return user_input_key.strip()
    return os.getenv("HUGGINGFACE_API_KEY")

def load_whisper_model():
    # In Gradio, we can load this globally or cache it if we want custom caching,
    # but for simplicity we rely on whisper's own caching or just load it.
    # To avoid reloading every time, we can load it once globally if memory permits,
    # or just call it inside the function.
    return whisper.load_model("base")

def transcribe_audio(audio_path):
    if not audio_path:
        return ""
    model = load_whisper_model()
    result = model.transcribe(audio_path)
    return result["text"]

def analyze_with_llama(transcript, token, language="English"):
    if not token:
        raise ValueError("No API Key provided.")
        
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

def process_call(audio_file, language, api_key_input):
    try:
        if audio_file is None:
            return "Please upload an audio file.", "", None
        
        token = get_api_key(api_key_input)
        if not token:
            return "Error: Please provide a Hugging Face API Key.", "", None
        
        # 1. Transcribe
        transcript = transcribe_audio(audio_file)
        
        # 2. Analyze
        analysis = analyze_with_llama(transcript, token, language)
        
        # 3. Create a downloadable file
        output_file = "analysis_report.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(analysis)
            
        return transcript, analysis, output_file

    except Exception as e:
        return f"Error: {str(e)}", "", None

# Gradio UI
with gr.Blocks(title="AI Call Analyzer", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎧 AI Call Analyzer (Design Thinking)")
    gr.Markdown("""
    Upload a call recording (Audio) to analyze it using **Whisper** (Transcription) and **Llama-3** (Analysis).
    This tool provides deep insights into Founder Context, Emotional State, and more.
    """)
    
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(type="filepath", label="Upload Audio File")
            language_input = gr.Radio(choices=["English", "Hinglish"], value="English", label="Select Report Language")
            api_key_input = gr.Textbox(
                label="Hugging Face API Key", 
                type="password", 
                placeholder="Enter HF Token if not in env",
                info="Required if HUGGINGFACE_API_KEY is not set in environment."
            )
            analyze_btn = gr.Button("Analyze Call", variant="primary")
        
        with gr.Column():
            transcript_output = gr.Textbox(label="Transcript", lines=10, interactive=False)
            analysis_output = gr.Markdown(label="Analysis Report")
            download_output = gr.File(label="Download Report")

    analyze_btn.click(
        fn=process_call,
        inputs=[audio_input, language_input, api_key_input],
        outputs=[transcript_output, analysis_output, download_output]
    )

if __name__ == "__main__":
    # share=True creates a public link which is great for mobile testing
    demo.launch(share=True)
