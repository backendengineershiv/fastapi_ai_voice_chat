import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import tempfile
import subprocess

load_dotenv()

speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")


def speech_to_text_from_audio(audio_bytes):

    # save incoming audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
        f.write(audio_bytes)
        webm_file = f.name

    wav_file = webm_file.replace(".webm", ".wav")

    # convert webm → wav using ffmpeg
    subprocess.run([
        "ffmpeg",
        "-i", webm_file,
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        wav_file
    ])

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=speech_region
    )

    audio_config = speechsdk.audio.AudioConfig(filename=wav_file)

    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text

    print("Speech recognition failed:", result.reason)

    return ""