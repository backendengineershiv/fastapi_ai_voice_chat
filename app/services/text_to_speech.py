import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")


def text_to_speech(text):

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=speech_region
    )

    # voice (you can change later)
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config
    )

    print("🔊 AI speaking...")

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis complete")

    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print("Speech synthesis canceled:", cancellation.reason)