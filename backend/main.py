import os
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from scam_detector import analyze_scam_intent

load_dotenv()

app = FastAPI(title="Deepfake Scam Firewall API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "system": "Deepfake Scam Firewall"}

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    print("[WS] Client connected to real-time analysis pipeline.")
    
    # Track the highest score achieved in this session so it never drops backward
    highest_score_seen = 0.0
    
    try:
        while True:
            data_str = await websocket.receive_text()
            payload = json.loads(data_str)
            transcript_text = payload.get("transcript", "").strip()
            
            if not transcript_text:
                continue

            print(f"[Backend Processing]: '{transcript_text}'")

            # Get intent score from Scam Detector
            intent_score = await asyncio.to_thread(analyze_scam_intent, transcript_text)
            
            # Ensure the score never drops below what we've already detected in this session
            if intent_score > highest_score_seen:
                highest_score_seen = intent_score
            else:
                intent_score = highest_score_seen

            final_score_int = int(intent_score * 100)

            # Build response payload
            response_payload = {
                "score": final_score_int,
                "composite_risk": final_score_int,
                "status": "INTERCEPT" if final_score_int >= 80 else "SAFE",
                "pitch_std": 0.05,
                "timbre_std": 0.02,
                "transcript": transcript_text
            }

            print(f"[Backend Sending Locked Score]: {final_score_int}%")
            await websocket.send_text(json.dumps(response_payload))

    except WebSocketDisconnect:
        print("[WS] Client disconnected.")