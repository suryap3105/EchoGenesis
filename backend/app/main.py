from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.state_manager import StateManager
from app.quantum_bridge import QuantumBridge
import asyncio
import json

app = FastAPI(title="EchoGenesis Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
quantum_bridge = QuantumBridge()
state_manager = StateManager(quantum_bridge)

@app.on_event("startup")
async def startup_event():
    print("EchoGenesis is waking up...")
    # Initialize state if needed

@app.get("/")
async def root():
    return {"message": "EchoGenesis Alive", "status": state_manager.get_status()}

@app.post("/chat")
async def chat(message: dict):
    user_text = message.get("message", "")
    reply = await state_manager.process_interaction(user_text)
    return {"reply": reply, "state": state_manager.get_public_state()}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Push state updates every 100ms or on change
            # For now, just echo or push periodic updates
            await asyncio.sleep(0.1)
            state = state_manager.get_public_state()
            await websocket.send_text(json.dumps(state))
    except WebSocketDisconnect:
        print("Client disconnected")
