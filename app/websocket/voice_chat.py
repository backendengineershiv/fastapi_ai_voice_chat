from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect
from app.services.ai_service import stream_ai_response
from app.services.text_to_speech import text_to_speech

router = APIRouter()


@router.websocket("/voice-chat")
async def voice_chat(websocket: WebSocket):

    await websocket.accept()

    try:

        while True:

            user_message = await websocket.receive_text()

            print("User:", user_message)

            # store full response for TTS
            full_response = ""

            for token in stream_ai_response(user_message):

                full_response += token

                # stream token to browser
                await websocket.send_text(token)

            print("AI:", full_response)

            # convert AI response to speech
            text_to_speech(full_response)

    except WebSocketDisconnect:
        print("Client disconnected")