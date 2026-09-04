"""
Batch-tests every .wav file in test_audio/ and prints a sorted table of scores.
Use this to pick your best "normal" and "synthetic" demo clips.

Setup:
    Put as many candidate clips as you want into test_audio/, named anything
    you like (e.g. normal_1.wav, normal_2.wav, synth_tts1.wav, synth_tts2.wav)

Run from inside backend/:
    python batch_test_clips.py
"""

import os
import glob
from audio_features import analyze_voice_authenticity

TEST_AUDIO_DIR = "../test_audio"

def main():
    wav_files = glob.glob(os.path.join(TEST_AUDIO_DIR, "*.wav"))

    if not wav_files:
        print(f"No .wav files found in {TEST_AUDIO_DIR}")
        return

    results = []
    for path in wav_files:
        try:
            score = analyze_voice_authenticity(path)
            results.append((os.path.basename(path), score))
        except Exception as e:
            results.append((os.path.basename(path), f"FAILED: {e}"))

    # Sort by score descending (highest risk first)
    results.sort(key=lambda x: x[1] if isinstance(x[1], float) else -1, reverse=True)

    print("\n" + "=" * 50)
    print(f"{'FILE':<30} {'SYNTHETIC_RISK':>15}")
    print("=" * 50)
    for name, score in results:
        if isinstance(score, float):
            print(f"{name:<30} {score:>15.3f}")
        else:
            print(f"{name:<30} {score:>15}")
    print("=" * 50)
    print("\nPick your HIGHEST-scoring clip as synthetic_sample.wav")
    print("Pick your LOWEST-scoring clip as normal_sample.wav")
    print("(rename/copy the winning files to those exact filenames)")

if __name__ == "__main__":
    main()