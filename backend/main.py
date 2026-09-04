import os
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from risk_engine import evaluate_call_threat
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
    print("Client connected to real-time analysis pipeline.")
    
    try:
        while True:
            message = await websocket.receive()
            
            if "bytes" in message:
                pcm_bytes = message["bytes"]
                # Evaluate intent against fallback or transcript stream
                intent_score = analyze_scam_intent("Urgent bank transfer required")
                
                threat_data = evaluate_call_threat(pcm_bytes, intent_score)
                await websocket.send_text(json.dumps(threat_data))
                
            elif "text" in message:
                data = json.loads(message["text"])
                transcript = data.get("transcript", "")
                intent_score = analyze_scam_intent(transcript)
                
                threat_data = evaluate_call_threat(b"", intent_score)
                await websocket.send_text(json.dumps(threat_data))

    except WebSocketDisconnect:
        print("Client disconnected.")