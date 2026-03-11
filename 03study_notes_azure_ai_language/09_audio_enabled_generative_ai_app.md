# Module: Develop an Audio-Enabled Generative AI Application
## Session: Deploying Multimodal Models, Audio Prompt Structure, Binary Audio, SDK Options

**Sources:**
- [Deploy a Multimodal Model](https://learn.microsoft.com/en-us/training/modules/develop-generative-ai-audio-apps/2-deploy-multimodal-model)
- [Develop an Audio-Based Chat App](https://learn.microsoft.com/en-us/training/modules/develop-generative-ai-audio-apps/3-develop-audio-chat-app)

---

## 1. Multimodal Model?

> **Multimodal model** = a generative AI model that accepts **more than one type of input**  in a single prompt.

### Why You Need a Multimodal Model for Audio

- Standard LLMs only accept **text input**
- To send audio in a prompt, you need a model that understands **audio-based input**
- The model processes the audio content and responds in text (or audio, depending on configuration)

---

## 2. Multimodal Models Available in Microsoft Foundry

| Model | Provider | Notes |
|---|---|---|
| **Phi-4-multimodal-instruct** | Microsoft | Lightweight, multimodal SLM |
| **gpt-4o** | OpenAI | Full multimodal support (text, image, audio) |
| **gpt-4o-mini** | OpenAI | Smaller, faster version of gpt-4o |

> Check the **Model Catalog** in Microsoft Foundry portal for the full current list.

---

## 3. Testing in the Foundry Playground

> After deploying a multimodal model, you can test audio prompts directly in the **chat playground** in Microsoft Foundry portal

| Option | Description |
|---|---|
| **Upload a file** | Upload a local audio file as an attachment |
| **Record a message** | Record audio directly in the browser |
| **Add text** | Combine text instructions with the audio (e.g., "Transcribe this audio:") |

---

## 4. Audio-Based Chat App

> The core difference between a **text chat app** and an **audio chat app** is the **structure of the user message**.

| Chat Type | User Message Structure |
|---|---|
| Text chat | Single string: `"content": "Hello"` |
| Audio chat | Multi-part array: `"content": [ {text item}, {audio item} ]` |

> Everything else (connection to endpoint, system message, processing responses) works the same as a text-based chat app.

---

## 5. Audio Prompt JSON Structure

> A prompt with audio uses a **multi-part `content` array** for the user message, containing both a `text` item and an `audio_url` item.

### Full Prompt JSON

```json
{
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Transcribe this audio:"
                },
                {
                    "type": "audio_url",
                    "audio_url": {
                        "url": "https://....."
                    }
                }
            ]
        }
    ]
}
```

### Message Structure Breakdown

| Field | Value / Description |
|---|---|
| `role: "system"` | System instruction: plain string as usual |
| `role: "user"` | User message : an **array** instead of a string |
| `type: "text"` | Text portion of the user message (e.g., instruction to the model) |
| `type: "audio_url"` | Audio portion of the user message |
| `audio_url.url` | Either a **web URL** to an audio file, or **base64-encoded binary data** |

---

## 6. Two Ways to Provide Audio Content

### Option 1: URL to a Web-Hosted Audio File

```json
{
    "type": "audio_url",
    "audio_url": {
        "url": "https://example.com/audio/sample.mp3"
    }
}
```

> Use when the audio file is **publicly accessible on the web**.

---

### Option 2: Base64-Encoded Local Audio File

```json
{
    "type": "audio_url",
    "audio_url": {
        "url": "data:audio/mp3;base64,<binary_audio_data>"
    }
}
```

> Use when the audio file is **stored locally** — encode the binary file as base64 and embed it in a **data URL**.

### Data URL Format

```
data:{mime-type};base64,{base64-encoded-data}
```

| Part | Example |
|---|---|
| `mime-type` | `audio/mp3`, `audio/wav`, `audio/ogg` |
| `base64,...` | Base64-encoded string of the raw audio file bytes |

### Web URL vs Base64 Comparison

| Aspect | Web URL | Base64 (Local File) |
|---|---|---|
| **Where audio lives** | Publicly hosted on a web server | Local file on your machine |
| **URL format** | `https://...` | `data:audio/mp3;base64,...` |
| **Requires internet access** | Yes (to fetch the file) | No (data embedded in request) |
| **Payload size** | Small (just the URL) | Larger (full audio bytes encoded) |

---

## 7. API and SDK Options

> You can submit audio-based prompts using either of two APIs, both of which have Python and .NET SDKs:

| API | Use Case |
|---|---|
| **Azure AI Model Inference API** | Works with models deployed in Microsoft Foundry (including non-OpenAI models) |
| **OpenAI API** | Works specifically with OpenAI models (gpt-4o, gpt-4o-mini) |

> Both **APIs abstract the underlying REST calls through language-specific SDKs**. Choose based on which model you deployed and where.

---

## 8. Text Chat vs Audio Chat

| Aspect | Text Chat App | Audio Chat App |
|---|---|---|
| **Model type** | Standard LLM | **Multimodal model** |
| **Connection/endpoint** | Same | Same |
| **System message** | Plain string | Plain string |
| **User message `content`** | Single string | **Array** of content items |
| **Content item types** | N/A | `text` + `audio_url` |
| **Audio source** | N/A | Web URL or base64-encoded local file |
| **API** | Azure AI Model Inference or OpenAI | Azure AI Model Inference or OpenAI |

