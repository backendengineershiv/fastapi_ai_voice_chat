from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect
from app.services.ai_service import stream_ai_response
from app.services.text_to_speech import text_to_speech
from app.services.speech_to_text import speech_to_text_from_audio

router = APIRouter()

@router.websocket("/voice-chat")
async def voice_chat(websocket: WebSocket):

    await websocket.accept()

    try:

        while True:

            audio_bytes = await websocket.receive_bytes()

            # convert speech → text
            user_message = speech_to_text_from_audio(audio_bytes)

            print("User:", user_message)

            full_response = ""

            for token in stream_ai_response(user_message):

                full_response += token

                await websocket.send_text(token)

            text_to_speech(full_response)

    except WebSocketDisconnect:
        print("Client disconnected")