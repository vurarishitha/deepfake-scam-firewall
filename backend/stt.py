from faster_whisper import WhisperModel

_model = WhisperModel("small", device="cpu", compute_type="int8")

def transcribe(audio_path: str) -> str:
    segments, _ = _model.transcribe(audio_path, beam_size=5)
    return " ".join(segment.text for segment in segments).strip()