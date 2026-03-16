import asyncio
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

    speech_finished = False

    # capture main event loop
    loop = asyncio.get_running_loop()

    async def handle_ai_response(user_text):

        print("User:", user_text)

        full_response = ""

        for token in stream_ai_response(user_text):

            full_response += token

            await websocket.send_text(token)

        print("AI:", full_response)

        if full_response.strip():
            text_to_speech(full_response)

    # Azure callback (runs in separate thread)
    def recognized(evt):

        if evt.result.text:

            user_text = evt.result.text

            print("Recognized:", user_text)

            asyncio.run_coroutine_threadsafe(
                handle_ai_response(user_text),
                loop
            )

    recognizer.recognized.connect(recognized)

    recognizer.start_continuous_recognition()

    try:

        while True:

            message = await websocket.receive()

            if "bytes" in message:

                audio_chunk = message["bytes"]

                stream.write(audio_chunk)

                speech_finished = False

            elif "text" in message:

                if message["text"] == "END_OF_SPEECH" and not speech_finished:

                    speech_finished = True

                    print("User stopped speaking")

    except WebSocketDisconnect:

        print("Client disconnected")

        recognizer.stop_continuous_recognition()