import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")

def analyze_scam_intent(transcript_text: str) -> float:
    """
    Uses Featherless AI open-weights infrastructure to calculate 
    a scam intent score (0.0 - 1.0) on streaming transcripts.
    """
    if not transcript_text or not transcript_text.strip():
        return 0.0

    if not FEATHERLESS_API_KEY:
        # Fallback heuristic if API key is not present
        keywords = ["bank", "otp", "wire", "urgent", "transfer", "police", "arrest", "account"]
        matches = sum(1 for word in keywords if word in transcript_text.lower())
        return min(1.0, matches * 0.25)

    headers = {
        "Authorization": f"Bearer {FEATHERLESS_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a real-time scam detection firewall. Analyze the speech transcript "
                    "for malicious intent (e.g., impersonation, social engineering, demanding money/OTPs). "
                    "Respond ONLY with a JSON object: {\"scam_score\": float} where float is between 0.0 and 1.0."
                )
            },
            {
                "role": "user",
                "content": f"Transcript: \"{transcript_text}\""
            }
        ],
        "temperature": 0.1
    }

    try:
        response = requests.post(
            "https://api.featherless.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=3
        )
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            return float(parsed.get("scam_score", 0.5))
        return 0.5
    except Exception:
        return 0.5