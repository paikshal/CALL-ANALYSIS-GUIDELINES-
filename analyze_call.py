import os
import whisper
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Add FFmpeg to PATH (Hardcoded for this environment fix)
ffmpeg_path = r"C:\Users\paiks\AppData\Local\Microsoft\Winget\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_path

# Load environment variables
load_dotenv()

# Configure Hugging Face
api_key = os.getenv("HUGGINGFACE_API_KEY")
if not api_key:
    print("HUGGINGFACE_API_KEY not found in environment variables.")
    # Fallback/Exit or ask user

# Initialize Client
client = InferenceClient(token=api_key)

# The User's specific "Design Thinking Fellow" persona prompt
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

def transcribe_audio(audio_path):
    """
    Transcribes audio using OpenAI's Whisper model (local).
    """
    print(f"\n🎧 Loading Whisper model (this may take a moment first time)...")
    model = whisper.load_model("base") 
    
    print(f"🎧 Transcribing '{audio_path}'...")
    result = model.transcribe(audio_path)
    
    return result["text"]

def analyze_with_huggingface(transcript):
    """
    Sends the transcript to Hugging Face (Mistral-7B/Zephyr) for analysis.
    """
    print(f"\n🧠 Sending transcript ({len(transcript)} chars) to Hugging Face for Design Thinking Analysis...")
    
    # Model: Meta-Llama-3-8B-Instruct (High quality, requires access)
    model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
    
    # Improved prompt to prevent hallucination
    user_message = f"""
Here is the raw transcript of a real call. 
Your task is to analyze it using the Design Thinking framework provided in the system prompt.

RULES:
1. Do NOT generate any new dialogue or conversation.
2. Do NOT repeat the transcript.
3. OUTPUT ONLY the analysis sections (1-8).
4. If the transcript is empty or unclear, say "Transcript is unclear".

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
        temperature=0.3  # Lower temperature for more focused analysis
    )
    
    return response.choices[0].message.content

def main():
    print("=== AI Customer Support Analyzer (Whisper + Hugging Face) ===")
    
    import sys
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
    else:
        audio_path = input("Enter the path to the audio file (e.g., call.mp3): ").strip()
    
    # Remove quotes if user added them
    if audio_path.startswith('"') and audio_path.endswith('"'):
        audio_path = audio_path[1:-1]
        
    if not os.path.exists(audio_path):
        print(f"❌ Error: File not found at {audio_path}")
        return

    try:
        # Step 1: Transcribe
        transcript = transcribe_audio(audio_path)
        print("\n📝 Transcript generated successfully.")
        # print(f"Preview: {transcript[:200]}...")

        # Step 2: Analyze
        analysis = analyze_with_huggingface(transcript)
        
        print("\n" + "="*40)
        print("✨ DESIGN THINKING ANALYSIS REPORT ✨")
        print("="*40 + "\n")
        print(analysis)
        
        print(f"DEBUG: Response length: {len(analysis)}")
        
        # Save to file
        base_name = os.path.basename(audio_path)
        file_root, _ = os.path.splitext(base_name)
        output_file = f"{file_root}_report.txt"
        
        abs_path = os.path.abspath(output_file)
        print(f"DEBUG: Saving to absolute path: {abs_path}")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(analysis)
        print(f"\n✅ Analysis saved to '{output_file}'")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
