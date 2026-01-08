# AI Model Comparison Report: Llama-3 vs. Mistral (Zephyr)

This report consolidates the analysis and comparison results from three different call recordings. We tested **Meta-Llama-3-8B-Instruct** against **Mistral-7B-Instruct** (via Zephyr-7B-Beta).

## 1. Call Recording: `ramandeep.wav`

| Feature | **Common / Strong Insights** (Both Models) | **Model Differences** |
| :--- | :--- | :--- |
| **Founder Context** | Both identified the founder as **"busy"**, **"risk-aware"**, and filtering noise. | **Llama-3**: Identified the founder as "thoughtful" and engaging when expansion was mentioned.<br>**Mistral**: Described answers as merely "short" without deep context. |
| **Key Challenges** | Both noted "Slow growth" and "Financial losses" as key issues. | **Llama-3**: Provided actionable analysis on why the founder was defensive about losses.<br>**Mistral**: repetitively suggested avoiding the topic of losses entirely. |
| **Verdict** | **Llama-3 Wins**. Mistral struggled with instruction following (repeated transcript). | |

---

## 2. Call Recording: `+919099500200...`

| Feature | **Common / Strong Insights** (Both Models) | **Model Differences** |
| :--- | :--- | :--- |
| **Emotional State** | Both tracked the shift from "Curious" to "Guarded". | **Llama-3**: Nuanced analysis of the "Gatekeeper" role and annoyance at the "rapid-fire" greeting.<br>**Mistral**: Missed the subtlety of the founder's time-guarding behavior. |
| **Caller Analysis** | Both noted the caller changed tone/control. | **Llama-3**: Correctly identified the caller's pressure led to *immaturity* (rushing).<br>**Mistral**: Incorrectly labeled the caller as "Mature" despite noting they struggled. |
| **Reliability** | | **Mistral**: Failed severely with **Infinite Loops** in the text generation. |

---

## 3. Call Recording: `...2511241950.awb`

| Feature | **Common / Strong Insights** (Both Models) | **Model Differences** |
| :--- | :--- | :--- |
| **Trust Dynamics** | Both saw the founder reduce risk when offered to share via WhatsApp/Text. | **Llama-3**: Accurately tracked: Curious -> Guarded -> Open (via specific channel).<br>**Mistral**: Got stuck in a text loop ("She seems mentally filtering noise, as she asks..."). |
| **Hallucinations** | | **Mistral**: Hallucinated a `[/USER]` prompt at the end of the report which didn't exist.<br>**Llama-3**: Clean, structured output. |

---

## 🚀 Final Verdict & Recommendation

### **Winner: Meta-Llama-3-8B-Instruct** 🏆

*   **Why?**
    1.  **Instruction Following**: Strictly followed the "Do not repeat transcript" rule.
    2.  **Depth**: Provided psychological insights (e.g., "Mental Space", "Power Dynamics") rather than just surface-level summary.
    3.  **Reliability**: Zero hallucinations or infinite loops across 3 complex tests.

### **Loser: Mistral-7B / Zephyr** ❌

*   **Why?**
    1.  **Repetition**: Prone to getting stuck in generation loops.
    2.  **Surface Level**: Missed subtleties in tone and context.
    3.  **Stability**: Failed to generate output in one instance (empty file).

**Action Taken**: The project `analyze_call.py` has been permanently configured to use **Llama-3**.
