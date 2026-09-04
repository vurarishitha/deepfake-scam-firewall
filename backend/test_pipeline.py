from stt import transcribe
from scam_detector import score

transcript = transcribe("WhatsApp Audio 2026-09-04 at 16.44.51.wav")
print("Transcript:", transcript)

result = score(transcript)
print("Scam Risk:", result)