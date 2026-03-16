from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect
from app.services.ai_service import stream_ai_response
from app.services.text_to_speech import text_to_speech
from app.services.speech_stream import create_stream_recognizer

router = APIRouter()


@router.websocket("/voice-chat")
async def voice_chat(websocket: WebSocket):

    await websocket.accept()

    recognizer, stream = create_stream_recognizer()

    try:

        def recognized(evt):
            if evt.result.text:

                print("User:", evt.result.text)

                full_response = ""

                for token in stream_ai_response(evt.result.text):

                    full_response += token

                text_to_speech(full_response)

        recognizer.recognized.connect(recognized)

        recognizer.start_continuous_recognition()

        while True:

            audio_chunk = await websocket.receive_bytes()

            stream.write(audio_chunk)

    except WebSocketDisconnect:

        print("Client disconnected")

        recognizer.stop_continuous_recognition()