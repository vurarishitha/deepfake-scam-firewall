import asyncio
import websockets

async def test():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as ws:
        with open("WhatsApp Audio 2026-09-04 at 16.44.51.wav", "rb") as f:
            audio_bytes = f.read()
        await ws.send(audio_bytes)
        response = await ws.recv()
        print("Server response:")
        print(response)

asyncio.run(test())