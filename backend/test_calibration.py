from scam_detector import score

test_cases = [
    ("Normal - lunch plan", "Hey, are we still on for lunch tomorrow at noon?"),
    ("Normal - work update", "Just finished the report, sending it over now."),
    ("Ambiguous - urgent help ask", "I'm having a problem right now and I need you to help me quickly. I'm at the hospital and I've run out of cash. Can you please transfer some money to me?"),
    ("High risk - bank OTP", "This is your bank's security department. Your account has been compromised, read us the one-time password sent to your phone right now or your account will be frozen."),
    ("High risk - tech support scam", "This is Microsoft support. We've detected a virus on your computer. Please install this remote access software immediately so we can fix it."),
    ("High risk - kidnapping scam", "Your daughter has been in an accident, we need you to wire two thousand dollars to this account right now or she won't get treatment."),
    ("Borderline - gift card", "Hey it's your boss, I'm in a meeting and need you to buy some gift cards for a client, send me the codes."),
]

for label, transcript in test_cases:
    result = score(transcript)
    print(f"[{label}]")
    print(f"  Transcript: {transcript}")
    print(f"  Result: {result}")
    print()