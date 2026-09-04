import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("FEATHERLESS_API_KEY"),
    base_url="https://api.featherless.ai/v1"
)

SYSTEM_PROMPT = """You are a real-time scam-call detection assistant.
Analyze the transcript of an ongoing phone call and assess scam risk.

Look for: urgency or pressure to act immediately, requests for OTP/PIN/card
numbers/passwords, impersonation of a bank/government agency/tech support/
employer, requests to transfer money via wire transfer, gift cards, prepaid
cards, or cryptocurrency (these are common because they are difficult to
trace or reverse), requests to install remote-access software, and threats
of account suspension, legal action, or harm to a family member.

Gift card and prepaid card payment requests should be treated as HIGH RISK,
similar to wire transfer requests, since they are a hallmark of scam tactics.

Return ONLY valid JSON in this exact shape, with no extra text, no markdown:
{"scam_risk": <float between 0.0 and 1.0>, "reason": "<short explanation>"}
"""

def score(transcript: str) -> dict:
    if not transcript or not transcript.strip():
        return {"scam_risk": 0.0, "reason": "No transcript yet"}
    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": transcript},
            ],
            temperature=0.2,
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"scam_risk": 0.0, "reason": "Failed to parse LLM output"}
    except Exception as e:
        return {"scam_risk": 0.0, "reason": f"LLM error: {str(e)}"}