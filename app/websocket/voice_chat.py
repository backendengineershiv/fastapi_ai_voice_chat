import asyncio
from uuid import uuid4
from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from app.services.ai_service import stream_ai_response
from app.services.text_to_speech import text_to_speech
from app.services.speech_stream import create_stream_recognizer
from app.services.conversation_service import save_message, get_messages

router = APIRouter()


@router.websocket("/voice-chat")
async def voice_chat(websocket: WebSocket):

    await websocket.accept()

    # unique session for this conversation
    session_id = str(uuid4())

    recognizer, stream = create_stream_recognizer()

    speech_finished = False

    # capture main FastAPI loop
    loop = asyncio.get_running_loop()

    async def handle_ai_response(user_text):

        print("User:", user_text)

        # save user message
        await save_message(session_id, "user", user_text)

        # fetch conversation history
        history = await get_messages(session_id)

        # system prompt
        messages = [
            {
                "role": "system",
                "content": "You are a helpful voice assistant."
            }
        ]

        messages.extend(history)

        full_response = ""

        for token in stream_ai_response(messages):

            full_response += token

            await websocket.send_text(token)

        print("AI:", full_response)

        await save_message(session_id, "assistant", full_response)

        text_to_speech(full_response)

    # Azure speech callback
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

            try:
                message = await websocket.receive()
            except RuntimeError:
                print("WebSocket closed")
                break

            # audio data from browser
            if "bytes" in message:

                audio_chunk = message["bytes"]

                stream.write(audio_chunk)

                speech_finished = False

            # control messages from browser
            elif "text" in message:

                if message["text"] == "END_OF_SPEECH" and not speech_finished:

                    speech_finished = True

                    print("User stopped speaking")

                    # close stream so Azure finalizes recognition
                    stream.close()

                    # restart recognizer for next speech segment
                    recognizer.stop_continuous_recognition()

                    recognizer, stream = create_stream_recognizer()

                    recognizer.recognized.connect(recognized)

                    recognizer.start_continuous_recognition()

    except WebSocketDisconnect:

        print("Client disconnected")

        recognizer.stop_continuous_recognition()