import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")

def analyze_scam_intent(transcript_text: str) -> float:
    if not transcript_text:
        return 0.0

    text = transcript_text.lower()
    print(f"[ScamDetector Analyzing]: '{text}'")

    words = text.split()
    word_count = len(words)
    
    if word_count == 0:
        return 0.0

    # Weighted keywords
    low_risk = ["bank", "account", "department", "customer", "service"]
    med_risk = ["urgent", "verify", "update", "suspended", "security"]
    high_risk = ["otp", "odp", "fraud", "blocked", "pin", "wire", "password"]

    # Calculate base threat weight
    threat_weight = 0.0
    for w in words:
        if w in low_risk:
            threat_weight += 0.10
        elif w in med_risk:
            threat_weight += 0.25
        elif w in high_risk:
            threat_weight += 0.45

    if threat_weight == 0.0:
        return 0.05  # Minimal baseline for active speech

    # Blend threat weight with word progression (smooth curve scaling)
    # This prevents short phrases from blowing past limits too fast
    progression_factor = min(word_count / 12.0, 1.0)
    score = (threat_weight * 0.7) + (progression_factor * 0.3)

    # Hard cap early sentences to guarantee smooth ramp-up
    if word_count < 6 and score > 0.6:
        score = 0.55

    score = min(max(score, 0.05), 1.0)
    
    print(f"[ScamDetector Smooth Score]: {int(score * 100)}%")
    return float(score)