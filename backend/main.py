import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from websocket import manager, save_chunk_to_tempfile
from scam_detector import score
from stt import transcribe
from risk_engine import fuse_risk

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten before final submission
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    transcript_so_far = ""
    try:
        while True:
            audio_bytes = await websocket.receive_bytes()

            tmp_path = save_chunk_to_tempfile(audio_bytes)
            try:
                chunk_text = transcribe(tmp_path)
            finally:
                os.remove(tmp_path)

            if chunk_text:
                transcript_so_far += " " + chunk_text

            llm_result = score(transcript_so_far)

            acoustic_score = 0.0  # TODO: replace with M2's real score once merged
            fused = fuse_risk(acoustic_score, llm_result["scam_risk"])

            await manager.send_json(websocket, {
                "transcript": transcript_so_far.strip(),
                "llm_score": llm_result["scam_risk"],
                "reason": llm_result["reason"],
                "acoustic_score": acoustic_score,
                "fused_risk": fused,
                "intercept": fused >= 0.80,
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)