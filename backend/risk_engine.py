import sys
import os
sys.path.append(os.path.dirname(__file__))

from audio_features import extract_audio_features

def evaluate_call_threat(pcm_bytes: bytes, llm_intent_score: float) -> dict:
    # 1. Get M2's acoustic score (40% weight)
    audio_analysis = extract_audio_features(pcm_bytes)
    acoustic_score = audio_analysis["acoustic_risk"]
    
    # 2. Compute weighted hybrid score (40% Acoustic + 60% Intent)
    composite_score = (acoustic_score * 0.40) + (llm_intent_score * 0.60)
    composite_score = round(float(composite_score), 2)
    
    # 3. Intercept threshold check (0.80+)
    should_intercept = composite_score >= 0.80
    
    return {
        "composite_risk": composite_score,
        "acoustic_score": acoustic_score,
        "intent_score": llm_intent_score,
        "pitch_anomaly": audio_analysis["is_anomaly"],
        "action": "INTERCEPT" if should_intercept else "MONITOR"
    }

if __name__ == "__main__":
    # Quick self-test
    dummy_bytes = bytes(16000 * 2)
    result = evaluate_call_threat(dummy_bytes, llm_intent_score=0.90)
    print("Risk Engine Test:", result)