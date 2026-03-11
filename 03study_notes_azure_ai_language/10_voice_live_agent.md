# Module: Develop an Azure AI Voice Live Agent
## Session: Voice Live API Architecture, Events, Configuration, and Python SDK

**Sources:**
- [Explore the Azure Voice Live API](https://learn.microsoft.com/en-us/training/modules/develop-voice-live-agent/2-voice-live-api)
- [Explore the AI Voice Live Client Library for Python](https://learn.microsoft.com/en-us/training/modules/develop-voice-live-agent/3-voice-live-sdk)

---

## 1. What Is the Voice Live API?

> **Voice Live API** = an Azure AI API that enables real-time, bidirectional voice communication using **WebSocket connections** and **JSON-formatted events**.

### Key Features

| Feature | Description |
|---|---|
| **Real-time audio processing** | **PCM16 and G.711** audio formats supported |
| **Advanced voice options** | OpenAI voices + Azure custom voices |
| **Avatar integration** | **WebRTC-based video** and animation streaming |
| **Built-in audio enhancement** | Noise reduction + echo cancellation |
| **Event-driven architecture** | Client events → server; Server events → client |

> Optimized for **Microsoft Foundry** resources: recommended for full feature availability.

---

## 2. Authentication Methods

| Method | Description |
|---|---|
| **Microsoft Entra (keyless)** | **Token-based**; recommended for production; requires **Cognitive Services User** role |
| **API Key** | Via `api-key` connection header (not available in browser) or `api-key` query string parameter |

### Microsoft Entra Token Details

| Detail | Value |
|---|---|
| **Required role** | Cognitive Services User |
| **Token scope** | `https://ai.azure.com/.default` (or legacy `https://cognitiveservices.azure.com/.default`) |
| **Header format** | `Authorization: Bearer <token>` |
| **Generated via** | Azure CLI or Azure SDKs |

> The `api-key` header option is **not available in browser environments**ㄝ use the query string parameter instead.

---

## 3. WebSocket Endpoint

> The endpoint varies depending on whether you connect through a **Foundry project (Agent)** or directly to a **model**.

| Connection Type | Endpoint Pattern |
|---|---|
| **Project (Agent) connection** | `wss://<resource>.services.ai.azure.com/voice-live/realtime?api-version=2025-10-01` |
| **Model connection** | `wss://<resource>.cognitiveservices.azure.com/voice-live/realtime?api-version=2025-10-01` |

| Connection Type | Required Query Parameters |
|---|---|
| **Model connection** | `model` |
| **Agent connection** | `agent_id` + `project_id` |

> The endpoint URL is the same for all models: only the **query parameters** differ.

---

## 4. Voice Live API Events

> Events are **JSON-formatted** and split into **client events** (sent to server) and **server events** (received from server).

### Client Events (sent from client → server)

| Event | Purpose |
|---|---|
| `session.update` | Modify session configurations (voice, modalities, turn detection, etc.) |
| `input_audio_buffer.append` | Add audio bytes to the input buffer |
| `input_audio_buffer.commit` | Process the buffer for transcription or response generation |
| `input_audio_buffer.clear` | Remove audio data from the buffer |
| `response.create` | Trigger model inference to generate a response |
| `session.avatar.connect` | Provide client SDP offer for WebRTC avatar streaming |

### Server Events (sent from server → client)

| Event | Purpose |
|---|---|
| `session.updated` | Confirms session configuration changes |
| `response.done` | Indicates response generation is complete |
| `conversation.item.created` | Notifies when a new conversation item is added |
| `input_audio_buffer.speech_started` | User started speaking (use to stop playback) |
| `response.audio_delta` | Audio chunk of the response (stream to speaker) |
| `error` | Error occurred in the session |

---

## 5. Session Configuration (`session.update`)

> The **first event** sent after connecting is typically `session.update`, it configures all session behavior.

### Full Example

```json
{
  "type": "session.update",
  "session": {
    "modalities": ["text", "audio"],
    "voice": {
      "type": "openai",
      "name": "alloy"
    },
    "instructions": "You are a helpful assistant. Be concise and friendly.",
    "input_audio_format": "pcm16",
    "output_audio_format": "pcm16",
    "input_audio_sampling_rate": 24000,
    "turn_detection": {
      "type": "azure_semantic_vad",
      "threshold": 0.5,
      "prefix_padding_ms": 300,
      "silence_duration_ms": 500
    },
    "temperature": 0.8,
    "max_response_output_tokens": "inf"
  }
}
```

### Session Configuration Fields

| Field | Description |
|---|---|
| `modalities` | Input/output types: `"text"`, `"audio"` |
| `voice.type` | `"openai"` or Azure custom voice |
| `voice.name` | Voice name (e.g., `"alloy"`) |
| `instructions` | System prompt for the agent |
| `input_audio_format` | Audio format for incoming audio (e.g., `"pcm16"`) |
| `output_audio_format` | Audio format for outgoing audio (e.g., `"pcm16"`) |
| `input_audio_sampling_rate` | Sampling rate in Hz (e.g., `24000`) |
| `turn_detection` | VAD settings (how end-of-speech is detected) |
| `temperature` | Response randomness (0–1) |
| `max_response_output_tokens` | Max tokens per response (`"inf"` = unlimited) |

### Turn Detection (VAD) Fields

| Field | Description |
|---|---|
| `type` | `"azure_semantic_vad"` — uses semantic understanding to detect turns |
| `threshold` | Sensitivity (0–1); higher = less sensitive |
| `prefix_padding_ms` | Audio captured before speech detected (ms) |
| `silence_duration_ms` | Silence required before turn ends (ms) |

> Use `azure_semantic_vad` for **intelligent turn detection**: it understands meaning, not just silence.

---

## 6. Audio Processing Configuration

> Noise reduction and echo cancellation can be enabled via `session.update`.

```json
{
  "type": "session.update",
  "session": {
    "input_audio_noise_reduction": {
      "type": "azure_deep_noise_suppression"
    },
    "input_audio_echo_cancellation": {
      "type": "server_echo_cancellation"
    }
  }
}
```

| Feature | Type Value | Benefit |
|---|---|---|
| **Noise reduction** | `azure_deep_noise_suppression` | Filters background noise; improves VAD accuracy |
| **Echo cancellation** | `server_echo_cancellation` | Prevents model hearing its own speaker output |

---

## 7. Avatar Streaming (WebRTC)

> Avatars are integrated via **WebRTC** for video and animation output alongside voice responses.

### `session.avatar.connect` Event

```json
{
  "type": "session.avatar.connect",
  "client_sdp": "<client_sdp>"
}
```

| Configurable | Options |
|---|---|
| Video | Resolution, bitrate, codec settings |
| Animation | Blendshapes, visemes |

---

## 8. Python SDK `azure-ai-voicelive`

> The Python SDK is **async-only** (as of v1.0.0). All patterns use `async/await`.

### SDK Overview

| Aspect | Detail |
|---|---|
| **Package** | `azure-ai-voicelive` |
| **API style** | Async-only (synchronous API deprecated in v1.0.0) |
| **Core function** | `connect()` — opens WebSocket session |
| **Namespace** | `azure.ai.voicelive.aio` (async) |

---

## 9. Authentication with the SDK

### API Key Authentication

```python
import asyncio
from azure.core.credentials import AzureKeyCredential
from azure.ai.voicelive import connect

async def main():
    async with connect(
        endpoint="your-endpoint",
        credential=AzureKeyCredential("your-api-key"),
        model="gpt-4o"
    ) as connection:
        pass

asyncio.run(main())
```

### Microsoft Entra Authentication (Recommended for Production)

```python
import asyncio
from azure.identity.aio import DefaultAzureCredential
from azure.ai.voicelive import connect

async def main():
    credential = DefaultAzureCredential()
    async with connect(
        endpoint="your-endpoint",
        credential=credential,
        model="gpt-4o"
    ) as connection:
        pass

asyncio.run(main())
```

| Auth Method | Credential Class | Production Ready |
|---|---|---|
| API Key | `AzureKeyCredential("key")` | No (keys exposed) |
| Microsoft Entra | `DefaultAzureCredential()` (async) | **Yes** (recommended) |

---

## 10. Handling Server Events with the SDK

> Iterate over `connection` with `async for` to receive server events.

```python
async for event in connection:
    if event.type == ServerEventType.SESSION_UPDATED:
        print(f"Session ready: {event.session.id}")
        # Start audio capture

    elif event.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
        print("User started speaking")
        # Stop playback immediately — prevent agent from "talking over" user

    elif event.type == ServerEventType.RESPONSE_AUDIO_DELTA:
        audio_bytes = event.delta
        # Stream audio_bytes to speaker

    elif event.type == ServerEventType.ERROR:
        print(f"Error: {event.error.message}")
```

### Key `ServerEventType` Values

| Event Type | When It Fires | Action |
|---|---|---|
| `SESSION_UPDATED` | Session config confirmed | Begin audio capture |
| `INPUT_AUDIO_BUFFER_SPEECH_STARTED` | User starts speaking | **Cancel playback immediately** |
| `RESPONSE_AUDIO_DELTA` | Audio chunk from model | Stream chunk to speaker |
| `RESPONSE_DONE` | Response complete | End of turn |
| `ERROR` | Something went wrong | Handle/log error |

> **Important:** On `SPEECH_STARTED`, cancel agent audio playback immediately — otherwise the agent will keep playing while the user speaks ("talking over" the user).

---

## 11. Minimal Full Example

```python
import asyncio
from azure.core.credentials import AzureKeyCredential
from azure.ai.voicelive.aio import connect
from azure.ai.voicelive.models import (
    RequestSession, Modality, InputAudioFormat, OutputAudioFormat,
    ServerVad, ServerEventType
)

API_KEY = "your-api-key"
ENDPOINT = "your-endpoint"
MODEL = "gpt-4o"

async def main():
    async with connect(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(API_KEY),
        model=MODEL,
    ) as conn:
        # Configure session
        session = RequestSession(
            modalities=[Modality.TEXT, Modality.AUDIO],
            instructions="You are a helpful assistant.",
            input_audio_format=InputAudioFormat.PCM16,
            output_audio_format=OutputAudioFormat.PCM16,
            turn_detection=ServerVad(
                threshold=0.5,
                prefix_padding_ms=300,
                silence_duration_ms=500
            ),
        )
        await conn.session.update(session=session)

        # Process events
        async for evt in conn:
            print(f"Event: {evt.type}")
            if evt.type == ServerEventType.RESPONSE_DONE:
                break

asyncio.run(main())
```

### Key SDK Classes

| Class | Purpose |
|---|---|
| `connect()` | Opens async WebSocket session |
| `RequestSession` | Session configuration object |
| `Modality` | Enum: `TEXT`, `AUDIO` |
| `InputAudioFormat` | Enum: `PCM16`, etc. |
| `OutputAudioFormat` | Enum: `PCM16`, etc. |
| `ServerVad` | VAD turn detection config |
| `ServerEventType` | Enum of all server event types |

---

## 12. Voice Live API vs Standard Chat API

| Aspect | Standard Chat API | Voice Live API |
|---|---|---|
| **Transport** | HTTPS (request/response) | **WebSocket** (persistent, bidirectional) |
| **Communication** | One-shot request/response | **Real-time streaming** |
| **Input** | Text | **Audio (microphone stream)** |
| **Output** | Text | **Audio (speaker stream)** |
| **Events** | None | Client events + Server events |
| **Turn detection** | N/A | **VAD (silence or semantic)** |
| **Avatar** | No | WebRTC avatar streaming |
| **SDK pattern** | Sync or async | **Async-only** |

---

## Quick Reference — Exam Tips

| Key Fact | Detail |
|---|---|
| **Transport protocol** | WebSocket (`wss://`) — not HTTP |
| **Authentication (production)** | Microsoft Entra with `Bearer` token; requires **Cognitive Services User** role |
| **First event to send** | `session.update` — configures voice, modalities, VAD, audio formats |
| **Audio buffer events** | `append` → `commit` → (optional) `clear` |
| **Turn detection type** | `azure_semantic_vad` — uses semantic understanding |
| **Interrupt handling** | Cancel playback on `INPUT_AUDIO_BUFFER_SPEECH_STARTED` |
| **Audio response event** | `RESPONSE_AUDIO_DELTA` — each chunk of audio output |
| **SDK style** | Async-only (`async/await`); use `async for event in connection` |
| **Avatar protocol** | WebRTC (via `session.avatar.connect` with SDP offer) |
| **Noise reduction** | `azure_deep_noise_suppression`; echo cancellation: `server_echo_cancellation` |
