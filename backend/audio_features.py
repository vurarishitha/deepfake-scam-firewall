import librosa
import numpy as np


def analyze_voice_authenticity(audio_chunk):
    """
    Analyzes an audio file/chunk and returns a synthetic-risk score from 0.0 to 1.0.
    Higher score = more likely synthetic/AI-generated voice.

    NOTE: this is a demo heuristic, not validated on real spoofed-voice datasets.
    Uses pyin (more stable than piptrack) to estimate pitch variance across the clip.
    Very low pitch variance often indicates a flatter, more "synthetic" delivery,
    though this is a rough proxy, not a robust deepfake detector.
    """
    y, sr = librosa.load(audio_chunk, sr=None)

    # pyin gives a much more stable/accurate pitch track than piptrack
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=librosa.note_to_hz('C2'),   # ~65 Hz, covers low voices
        fmax=librosa.note_to_hz('C7'),   # ~2093 Hz, covers high voices
        sr=sr
    )

    voiced_f0 = f0[~np.isnan(f0)]

    if len(voiced_f0) == 0:
        pitch_std = 0
    else:
        pitch_std = np.std(voiced_f0)

    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))

    # Rescaled threshold: pyin's pitch_std for natural speech tends to sit
    # roughly in the 10-60 Hz range, unlike piptrack's noisy larger values.
    synthetic_risk = 1.0 if pitch_std < 8.0 else max(0.0, (60.0 - pitch_std) / 60.0)

    return synthetic_risk