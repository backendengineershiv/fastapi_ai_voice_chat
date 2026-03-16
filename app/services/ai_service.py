import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


def stream_ai_response(messages):

    stream = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=messages,
        stream=True
    )

    for chunk in stream:

        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta

        if delta and delta.content:
            yield delta.content