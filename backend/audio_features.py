import librosa
import numpy as np

def extract_audio_features(audio_bytes: bytes, sample_rate: int = 16000) -> dict:
    """
    Parses raw PCM16 audio bytes and computes acoustic features 
    to calculate a synthetic voice risk score based on pitch fluctuation.
    """
    # 1. Fallback for empty or micro-chunks
    if not audio_bytes or len(audio_bytes) < sample_rate * 0.5:
        return {
            "pitch_std": 0.0,
            "spectral_centroid": 0.0,
            "acoustic_risk": 0.0,
            "is_anomaly": False
        }

    # 2. Convert PCM16 byte stream into a float32 array (-1.0 to 1.0)
    audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

    # 3. Track pitch (F0) using Librosa piptrack
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sample_rate)
    
    # Filter out silent and low-energy frames
    voiced_pitches = pitches[magnitudes > np.median(magnitudes)]
    
    # Calculate micro-pitch variance (standard deviation)
    pitch_std = float(np.std(voiced_pitches)) if len(voiced_pitches) > 0 else 0.0

    # 4. Measure timbre brightness (Spectral Centroid)
    centroid = librosa.feature.spectral_centroid(y=audio, sr=sample_rate)
    spectral_centroid_mean = float(np.mean(centroid)) if centroid.size > 0 else 0.0

    # 5. Compute Synthetic Risk Score
    # Synthetic TTS models lack dynamic human pitch variation (flat pitch_std < 15.0)
    if pitch_std == 0.0:
        acoustic_risk = 0.0
    elif pitch_std < 15.0:
        acoustic_risk = 1.0
    else:
        acoustic_risk = max(0.0, (40.0 - pitch_std) / 40.0)

    return {
        "pitch_std": round(pitch_std, 2),
        "spectral_centroid": round(spectral_centroid_mean, 2),
        "acoustic_risk": round(float(acoustic_risk), 2),
        "is_anomaly": acoustic_risk > 0.65
    }

if __name__ == "__main__":
    # Self-test block: Verify execution with dummy silence buffer
    dummy_pcm = bytes(16000 * 2)  # 1 second of zero-pcm bytes
    output = extract_audio_features(dummy_pcm)
    print("Self-Test Success! Output structure:", output)