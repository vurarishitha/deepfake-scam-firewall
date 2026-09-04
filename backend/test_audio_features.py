"""
Quick standalone test for audio_features.py
Run this from inside your backend/ folder (or adjust the import path below).

Usage:
    python test_audio_features.py
"""

from audio_features import analyze_voice_authenticity

# Point these at your two sample clips in test_audio/
NORMAL_CLIP = "../test_audio/normal_sample.wav"
SYNTHETIC_CLIP = "../test_audio/synthetic_sample.wav"

def run_test(label, path):
    try:
        score = analyze_voice_authenticity(path)
        print(f"{label}: {path}")
        print(f"  -> synthetic_risk score: {score:.3f}")
    except Exception as e:
        print(f"{label}: FAILED to process {path}")
        print(f"  -> error: {e}")
    print()

if __name__ == "__main__":
    print("Testing analyze_voice_authenticity()\n" + "-" * 40)
    run_test("NORMAL VOICE", NORMAL_CLIP)
    run_test("SYNTHETIC/PITCH-SHIFTED VOICE", SYNTHETIC_CLIP)
    print("-" * 40)
    print("Expect: normal voice score LOW, synthetic voice score HIGH.")
    print("If both scores are similar, the logic isn't discriminating well yet.")