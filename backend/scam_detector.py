import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")

def analyze_scam_intent(transcript_text: str) -> float:
    """
    Sends transcript text to Featherless LLM and returns 
    a scam intent probability score between 0.0 and 1.0.
    """
    if not transcript_text or len(transcript_text.strip()) == 0:
        return 0.0

    # Basic fallback heuristic if API key is missing
    if not FEATHERLESS_API_KEY:
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
                "content": "You are a fraud detection agent. Analyze the text for scam patterns (e.g., sense of urgency, requesting OTPs, gift cards, bank transfers, impersonating officials). Output ONLY a valid JSON object with key 'scam_score' between 0.0 and 1.0."
            },
            {
                "role": "user",
                "content": f"Analyze this transcript: '{transcript_text}'"
            }
        ],
        "temperature": 0.1
    }

    try:
        response = requests.post(
            "https://api.featherless.ai/v1/chat/completions", 
            headers=headers, 
            json=payload, 
            timeout=5
        )
        if response.status_code == 200:
            res_json = response.json()
            content = res_json['choices'][0]['message']['content']
            parsed = json.loads(content)
            return float(parsed.get("scam_score", 0.5))
        return 0.5
    except Exception:
        return 0.5

if __name__ == "__main__":
    score = analyze_scam_intent("Please send me your bank OTP immediately or your account will be blocked.")
    print("Test Intent Score:", score)