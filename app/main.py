from fastapi import FastAPI
from app.websocket.voice_chat import router as voice_router

app = FastAPI()

app.include_router(voice_router)

@app.get("/")
def home():
    return {"message": "AI Voice Chat Backend Running"}