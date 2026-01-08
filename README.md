# 🎧 AI Call Analyzer (Design Thinking)

A Python-based tool that analyzes customer support and sales calls using **AI-powered pyschological profiling**. It goes beyond simple summarization to map the **emotional state, power dynamics, and risk perception** of the participants using the "Design Thinking" framework.

## 🚀 Key Features

*   **🗣️ Auto-Transcription**: Uses OpenAI's `Whisper` model for high-accuracy speech-to-text.
*   **🧠 Deep Psychological Analysis**: Uses **Meta-Llama-3-8B-Instruct** to analyze:
    *   Founder Context & Mental Space
    *   Emotional State Mapping (Curious → Guarded → Open)
    *   Control & Power Dynamics
    *   Trust & Risk Perception
*   **💻 Dual Interface**:
    *   **CLI Tool**: For quick local analysis.
    *   **Web App**: Streamlit-based interface for easy file uploads.
*   **📊 Model Comparison**: Proven superiority of Llama-3 over Mistral-7B/Zephyr for this specific task.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/paikshal/CALL-ANALYSIS-GUIDELINES-.git
    cd "dt intership"
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install FFmpeg**:
    *   **Windows**: [Download FFmpeg](https://ffmpeg.org/download.html) and add to PATH.
    *   **Linux/Mac**: `sudo apt install ffmpeg` or `brew install ffmpeg`.

4.  **Setup API Keys**:
    Create a `.env` file in the root directory:
    ```env
    HUGGINGFACE_API_KEY=hf_your_token_here
    ```

## 🎮 Usage

### Option 1: Web Interface (Recommended)
Run the Streamlit app to upload files via your browser:
```bash
streamlit run app.py
```

### Option 2: Command Line Interface (CLI)
Run the script directly on an audio file:
```bash
python analyze_call.py "path/to/audio/file.wav"
```

## 📂 Project Structure

*   `app.py`: Streamlit web application.
*   `analyze_call.py`: Core logic for transcription and Llama-3 analysis.
*   `model_comparison_insights.md`: Detailed report on why Llama-3 was chosen over Mistral.
*   `requirements.txt`: Python package dependencies.
*   `packages.txt`: System dependencies (for Cloud deployment).

## 💡 Model Insights
We conducted a rigorous comparison between **Meta-Llama-3-8B** and **Mistral-7B (Zephyr)**.
*   **Llama-3 (Winner)**: provided deep, nuanced psychological insights and strictly followed negative constraints (e.g., "Do not repeat transcript").
*   **Mistral**: frequently got stuck in repetition loops and provided surface-level analysis.

This project is locked to use **Llama-3** for maximum reliability.

## 📜 License
[MIT License](LICENSE)
