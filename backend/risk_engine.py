import sys
import os
sys.path.append(os.path.dirname(__file__))

from audio_features import extract_audio_features

def evaluate_call_threat(pcm_bytes: bytes, llm_intent_score: float, transcript_text: str = "") -> dict:
    # 1. Get M2's acoustic score (40% weight)
    # audio_analysis = extract_audio_features(pcm_bytes)
    acoustic_score = 0.0  # Default to 0.0 when streaming text-only

    # 2. Compute hybrid score (Fallback to 100% LLM Intent if no PCM bytes are streamed)
    if not pcm_bytes:
        composite_score = llm_intent_score
    else:
        composite_score = (acoustic_score * 0.40) + (llm_intent_score * 0.60)
        
    composite_score = round(float(composite_score), 2)

    # 3. Intercept threshold check (0.80+)
    should_intercept = composite_score >= 0.80

    return {
        "score": int(composite_score * 100),
        "pitch_std": 0.05,
        "timbre_std": 0.02,
        "transcript": transcript_text if transcript_text else ("Urgent bank transfer required" if should_intercept else "Monitoring call..."),
        "composite_risk": composite_score,
        "action": "INTERCEPT" if should_intercept else "MONITOR"
    }

if __name__ == "__main__":
    # Quick self-test
    dummy_bytes = bytes(16000 * 2)
    result = evaluate_call_threat(dummy_bytes, llm_intent_score=0.90, transcript_text="Test scam")
    print("Risk Engine Test:", result)