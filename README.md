# Real-Time AI Voice Assistant Backend

A **real-time conversational AI voice assistant backend** built using **FastAPI, WebSockets, Azure OpenAI, Azure Speech Services, and MongoDB**.
The system captures microphone audio from the browser, streams it to the backend, converts speech to text, generates an AI response, and returns the answer with synthesized speech.

This project demonstrates how to build **low-latency voice AI systems** similar to modern AI assistants.

---

# 🚀 Features

* 🎤 **Real-time microphone streaming**
* 🔁 **WebSocket bidirectional communication**
* 🧠 **LLM responses using Azure OpenAI**
* 🗣 **Speech-to-Text using Azure Speech**
* 🔊 **Text-to-Speech responses**
* 💾 **Conversation memory stored in MongoDB**
* ⚡ **Streaming AI responses for lower latency**
* 🧵 **Async backend architecture with FastAPI**

---

# 🏗 System Architecture

Browser Microphone
↓
WebSocket Audio Streaming
↓
FastAPI Backend
↓
Azure Speech Service (Speech-to-Text)
↓
MongoDB (Conversation Memory)
↓
Azure OpenAI (LLM Response Generation)
↓
Azure Speech Service (Text-to-Speech)
↓
Audio Response

---

# 🧰 Tech Stack

Backend

* FastAPI
* WebSockets
* Async Python

AI Services

* Azure OpenAI
* Azure Speech-to-Text
* Azure Text-to-Speech

Database

* MongoDB
* Motor (Async MongoDB driver)

Frontend

* HTML + JavaScript
* Web Audio API
* MediaRecorder / AudioContext

---

# 📂 Project Structure

```
fastapi-ai-voice-chat
│
├── app
│   ├── main.py
│   │
│   ├── websocket
│   │   └── voice_chat.py
│   │
│   ├── services
│   │   ├── ai_service.py
│   │   ├── speech_stream.py
│   │   ├── text_to_speech.py
│   │   └── conversation_service.py
│   │
│   ├── database
│   │   └── mongodb.py
│   │
│   ├── models
│   └── schemas
│
├── test_ws.html
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```
git clone https://github.com/yourusername/fastapi-ai-voice-chat.git
cd fastapi-ai-voice-chat
```

---

## 2. Create Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-02-15-preview

AZURE_SPEECH_KEY=your_speech_key
AZURE_SPEECH_REGION=your_region

MONGO_URI=mongodb://localhost:27017
MONGO_DB=voice_ai
```

---

# 🗄 MongoDB Setup

Start MongoDB locally.

```
brew services start mongodb-community
```

Verify:

```
mongosh
```

Database used:

```
voice_ai
```

Collection:

```
conversations
```

Example document:

```
{
  "session_id": "abc123",
  "messages": [
    { "role": "user", "content": "Hello AI" },
    { "role": "assistant", "content": "Hello! How can I help?" }
  ]
}
```

---

# ▶️ Running the Server

```
uvicorn app.main:app --reload --port 8003
```

Server starts at:

```
http://localhost:8003
```

---

# 🎤 Testing Voice Chat

Open the provided test client:

```
test_ws.html
```

Steps:

1. Open the HTML file in a browser
2. Click **Start Talking**
3. Speak into the microphone
4. The AI assistant responds with voice

---

# 🔄 Real-Time Voice Pipeline

1️⃣ Browser records microphone audio
2️⃣ Audio chunks streamed via WebSocket
3️⃣ FastAPI backend receives audio
4️⃣ Azure Speech converts speech → text
5️⃣ Conversation history retrieved from MongoDB
6️⃣ Azure OpenAI generates response
7️⃣ Response converted to speech
8️⃣ AI voice reply played

---

# 🧠 Conversation Memory

Messages are stored in MongoDB so the AI maintains context.

Example conversation:

User: My name is Shiv
AI: Nice to meet you Shiv

User: What is my name?
AI: Your name is Shiv

---

# ⚡ Performance Optimizations

* Streaming LLM responses
* Persistent WebSocket connection
* Async FastAPI architecture
* Audio chunk processing
* Minimal API overhead

---

# 🧪 Future Improvements

Potential improvements:

* Stream TTS audio back to browser
* WebRTC audio streaming
* Voice activity detection improvements
* Interrupt AI while speaking
* Redis session cache
* Horizontal scaling with Kubernetes
* RAG knowledge base integration

---

# 📚 What This Project Demonstrates

This project demonstrates how to build **production-style AI systems** combining:

* real-time audio streaming
* speech recognition
* LLM orchestration
* conversation memory
* asynchronous backend design

These patterns are commonly used in **AI voice assistants and conversational AI systems**.

---

# 👨‍💻 Author

Shiv Pratap Raj
Software Engineer | Backend & AI Systems

---
