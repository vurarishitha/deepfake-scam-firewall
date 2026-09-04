"""
Debug script — imports the REAL analyze_voice_authenticity from audio_features.py
and also prints the raw pitch_std so we can see what's happening.

Run from inside backend/:
    python debug_audio_features.py
"""

import librosa
import numpy as np
from audio_features import analyze_voice_authenticity


def debug_analyze(path, label):
    print(f"\n{label}: {path}")
    try:
        y, sr = librosa.load(path, sr=None)
        print(f"  duration: {len(y)/sr:.2f}s, sample rate: {sr}")

        f0, voiced_flag, voiced_probs = librosa.pyin(
            y,
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7'),
            sr=sr
        )
        voiced_f0 = f0[~np.isnan(f0)]

        if len(voiced_f0) == 0:
            print("  WARNING: no voiced pitch detected")
            pitch_std = 0
        else:
            pitch_std = np.std(voiced_f0)
            print(f"  voiced frames: {len(voiced_f0)}")
            print(f"  pitch mean: {np.mean(voiced_f0):.2f}")
            print(f"  pitch_std: {pitch_std:.2f}")

        # Now call the REAL function from audio_features.py
        real_score = analyze_voice_authenticity(path)
        print(f"  REAL synthetic_risk (from audio_features.py): {real_score:.3f}")

    except Exception as e:
        print(f"  FAILED: {e}")


if __name__ == "__main__":
    debug_analyze("../test_audio/normal_sample.wav", "NORMAL VOICE")
    debug_analyze("../test_audio/synthetic_sample.wav", "SYNTHETIC VOICE")