# Deepfake & Scam Defense Firewall

**Track:** Build the Unexpected · **Event:** HackWave 3.0 · **Team Size:** 3 · **Team Name:** name not found

A live, mic-based dashboard that streams audio, detects synthetic-voice signatures and scam intent in real time, and executes a simulated protective interception when combined risk crosses a threshold.


---

## Problem

AI voice cloning has made phone scams dramatically more convincing. Attackers can now clone a real bank's tone, a relative's voice, or an authority figure's cadence, and combine that with high-pressure scripts ("your account is compromised, read me your OTP now") to manipulate victims in real time. Humans are bad at detecting synthetic voices under stress, and keyword-based scam filters are too easy to fool or too prone to false alarms.

## Solution

We built a system that judges a live call using **two independent signals**, fused into one risk score:

1. **How the voice sounds** — acoustic analysis (pitch variance, spectral centroid, zero-crossing rate) flags voices that sound unnaturally flat or synthetic, a common signature of cloned/AI-generated speech.
2. **What the words mean** — a live transcript is sent to **Featherless.ai** (Llama 3.1 8B Instruct), which returns a structured JSON scam-risk score flagging urgency, OTP/PIN requests, and impersonation of authority.

Neither signal alone is reliable — a real telemarketer might sound flat over bad audio, and a real bank might legitimately ask for verification. But **a synthetic-sounding voice combined with scam-shaped language** is a strong, hard-to-fake signal. When the fused score crosses a threshold, the system automatically triggers a visual alert, an audio warning, and a simulated call-termination — no human needs to click a button.

### Architecture

```
Mic (Browser/WebRTC) → FastAPI/WebSocket Backend → Fused Risk Score → Live Dashboard
                              │
                    ┌─────────┴─────────┐
                    │                   │
              Speech-to-Text      Librosa Audio
              → Transcript        Feature Extraction
                    │                   │
              LLM Intent Score    Acoustic Score
                    │                   │
                    └────────┬──────────┘
                    Risk = 0.40 × Acoustic + 0.60 × LLM Intent
```

### Core scoring logic

```python
def analyze_voice_authenticity(audio_chunk):
    y, sr = librosa.load(audio_chunk, sr=None)
    pitch, _ = librosa.piptrack(y=y, sr=sr)
    pitch_std = np.std(pitch[pitch > 0]) if np.any(pitch > 0) else 0
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    synthetic_risk = 1.0 if pitch_std < 15.0 else max(0.0, (40.0 - pitch_std) / 40.0)
    return synthetic_risk
```

```
Final Risk = 0.40 × Acoustic Score + 0.60 × LLM Intent Score
```

If `Final Risk > 0.80`, the system auto-triggers a visual alert, an audio warning overlay, and a "call terminated" UI state.

---

## Tech Stack

**Backend:** Python, FastAPI, Uvicorn, WebSockets, Pydantic, librosa, NumPy, SciPy, SoundFile
**Speech-to-Text:** Whisper
**LLM scoring:** Featherless.ai (Llama 3.1 8B Instruct)
**Frontend:** React + Vite, Recharts, Lucide React, WaveSurfer.js
**Deployment:** Backend on Render/Railway, Frontend on Vercel/Netlify

> **Mandatory tool usage:** *[Fill in here exactly which event-mandated open-source AI tool was used, and where in the pipeline.]*

---

## Setup

### Prerequisites
- Python 3.11 or 3.12
- Node.js LTS
- Git
- FFmpeg (required by librosa/soundfile for audio decoding)

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/deepfake-scam-firewall.git
cd deepfake-scam-firewall
```

### 2. Backend setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\Activate.ps1
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in `backend/`:
```
FEATHERLESS_API_KEY=your_key_here
# or ANTHROPIC_API_KEY / OPENAI_API_KEY depending on your LLM provider
```

Run the backend:
```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend setup
```bash
cd frontend
npm install
npm run dev
```
Open the local URL printed in the terminal (typically `http://localhost:5173`).

---

## Usage

1. Open the dashboard in your browser and grant microphone access when prompted.
2. Speak normally — the transcript streams live, and the threat gauge should stay green.
3. To simulate an attack, play a synthetic/cloned voice clip or a scam script (e.g. "This is bank security, read me your OTP immediately") near the mic.
4. Watch the acoustic score and LLM intent score both spike, pushing the fused risk gauge into the red.
5. If the fused score crosses **0.80**, the system automatically locks into an **INTERCEPTED** state with a visual and audio alert — no manual action required.

### Offline/local demo mode
If live mic input or network conditions are unreliable, a fallback mode runs pre-recorded audio samples (`test_audio/`) through the same detection pipeline without requiring a live mic or stable deployment link.

---

## Project Structure

```
deepfake-scam-firewall/
├── backend/
│   ├── main.py                    # FastAPI app, WebSocket endpoint
│   ├── websocket.py                # streaming handlers
│   ├── stt.py                      # Whisper speech-to-text integration
│   ├── audio_features.py           # librosa acoustic scoring
│   ├── scam_detector.py            # Featherless.ai scam-intent scoring
│   ├── risk_engine.py              # fusion formula
│   ├── batch_test_clips.py         # batch testing helper
│   ├── debug_audio_features.py     # acoustic scoring debug script
│   ├── test_audio_features.py
│   ├── test_calibration.py
│   ├── test_featherless.py
│   ├── test_pipeline.py
│   ├── test_scam_detector.py
│   ├── test_stt.py
│   ├── test_ws_client.py
│   ├── requirements.txt
│   ├── .env                        # API keys (not committed)
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Waveform.tsx
│   │   │   ├── Transcript.tsx
│   │   │   ├── ThreatGauge.tsx
│   │   │   └── InterceptOverlay.tsx
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── dashboard.css
│   ├── mic.js                      # WebRTC mic capture
│   ├── mic_test.html
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── test_audio/                     # sample clips for offline demo mode
│   ├── normal_sample.wav
│   ├── normal_2.wav
│   ├── normal_3.wav
│   ├── synthetic_sample.wav
│   ├── synth_2.wav
│   └── synth_3.wav
├── .gitignore
└── README.md
```

---

## Limitations

Built in 24 hours as a proof of concept — not a production system. Detection thresholds (pitch variance cutoff, 40/60 fusion weighting) are demo heuristics, not validated against real spoofed-voice datasets. It's a mic-based simulation, not real telephony.

---

## Real-World Impact

Voice-cloning scams are a fast-growing threat, and existing defenses (caller ID, keyword filters) are increasingly easy to bypass. A system that fuses acoustic authenticity with intent analysis — rather than relying on either alone — points toward a more robust direction for real-time scam defense, particularly for vulnerable populations who are common targets of these attacks.