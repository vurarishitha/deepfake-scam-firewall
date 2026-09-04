from scam_detector import score

normal_transcript = "Hey, are we still on for lunch tomorrow at noon? I was thinking that new pizza place."
scam_transcript = "This is your bank's security department. Your account has been compromised, we need you to read us the one-time password sent to your phone right now or your account will be frozen."

print("--- Normal call ---")
print(score(normal_transcript))

print("--- Scam call ---")
print(score(scam_transcript))