# Module: Develop a Vision-Enabled Generative AI Application
## Session: Multimodal Model Deployment and Vision-Based Chat App Development

**Sources:**
- [Deploy a multimodal model](https://learn.microsoft.com/en-us/training/modules/develop-generative-ai-vision-apps/2-deploy-multimodal-model)
- [Develop a vision-based chat app](https://learn.microsoft.com/en-us/training/modules/develop-generative-ai-vision-apps/3-develop-visual-chat-app)

---

## 1. What Is a Multimodal Model?

> **Multimodal model** = a generative AI model that accepts not just text, but also **image** (and sometimes **audio**) as input, enabling **vision-based chat applications**.

Standard chat models only accept text. To handle prompts that include images, you must deploy a multimodal model.

---

## 2. Available Multimodal Models in Microsoft Foundry

| Model | Provider | Supports |
|---|---|---|
| **Phi-4-multimodal-instruct** | Microsoft | Text + Image (+ Audio) |
| **gpt-4o** | OpenAI | Text + Image + Audio |
| **gpt-4o-mini** | OpenAI | Text + Image |

> the full list is in the [Model catalog in Microsoft Foundry portal](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/model-catalog-overview).

---

## 3. Testing Multimodal Models

> After deploying a multimodal model, test it in the **chat playground** in the Microsoft Foundry portal.

- Upload a local image file directly in the chat playground
- Add a text message alongside the image
- The model responds based on both text and image content

---

## 4. How Vision-Based Chat Differs from Text-Based Chat

| Aspect | Text Chat | Vision Chat |
|---|---|---|
| **User message content** | Single string | **Multi-part array** (text item + image item) |
| **Image input** | Not supported | URL or **base64** binary data |
| **Connection/endpoint** | Same | Same, just different message structure |
| **API compatibility** | Azure AI Model Inference or OpenAI | Same, both support vision |

> The connection and endpoint setup is identical, only the **prompt structure** changes.

---

## 5. Vision Prompt Structure (JSON)

> The key difference is a **multi-part `content` array** in the user message — one text item and one image item.

### Full Prompt Structure

```json
{
    "messages": [
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": [
            {
                "type": "text",
                "text": "Describe this picture:"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://....."
                }
            }
        ]}
    ]
}
```

### Message Structure Breakdown

| Field | Value | Description |
|---|---|---|
| `role` | `"system"` | System prompt — sets assistant behavior |
| `role` | `"user"` | User turn — contains multi-part content |
| `content` (user) | Array `[...]` | Multi-part: text item **and** image item |
| `type` | `"text"` | Text portion of the user message |
| `type` | `"image_url"` | Image portion of the user message |
| `image_url.url` | URL string or data URL | The actual image — web URL or base64 |

---

## 6. Two Ways to Provide Image Data

### Option A: Image URL (web-hosted image)

```json
{
    "type": "image_url",
    "image_url": {
        "url": "https://example.com/image.jpg"
    }
}
```

> Use when the image is publicly accessible online.

### Option B: Base64 Binary Data (local image file)

```json
{
    "type": "image_url",
    "image_url": {
        "url": "data:image/jpeg;base64,<binary_image_data>"
    }
}
```

> Use when submitting a **local file**, encode it as base64, wrap in a data URL.

### Comparison

| Method | When to Use | Format |
|---|---|---|
| **Image URL** | Image is hosted online | `"url": "https://..."` |
| **Base64 data URL** | Local image file | `"url": "data:image/jpeg;base64,..."` |

---

## 7. API and SDK Options

> Two API families can submit vision-based prompts, choose based on your model and deployment.

| API | SDK Languages | Best For |
|---|---|---|
| **Azure AI Model Inference API** | Python, .NET | Models deployed in Microsoft Foundry (including non-OpenAI models like Phi-4) |
| **OpenAI API** | Python, .NET | OpenAI models (gpt-4o, gpt-4o-mini) |

> Both APIs use the same multi-part message structure shown above.

---

## 8. End-to-End Pattern

```
1. Deploy multimodal model in Microsoft Foundry
        ↓
2. Connect client app to the model endpoint
        ↓
3. Build multi-part user message:
   - text content item (the question/instruction)
   - image_url content item (URL or base64 data URL)
        ↓
4. Submit prompt via Azure AI Model Inference or OpenAI SDK
        ↓
5. Process and display the model's response
```

---

## Quick Reference — Exam Tips

| Key Fact | Detail |
|---|---|
| **Multimodal = image input support** | Standard models are text-only; multimodal handles text + image (+ sometimes audio) |
| **3 key multimodal models** | Phi-4-multimodal-instruct (Microsoft), gpt-4o, gpt-4o-mini (OpenAI) |
| **Test in** | Chat playground in Microsoft Foundry portal |
| **Vision prompt difference** | User `content` is an **array** (multi-part), not a simple string |
| **Two content item types** | `"type": "text"` + `"type": "image_url"` |
| **Two image data formats** | Web URL (`https://...`) or base64 data URL (`data:image/jpeg;base64,...`) |
| **Local image** | Must be base64 encoded and wrapped in a data URL |
| **Two compatible APIs** | Azure AI Model Inference API + OpenAI API — both support vision |
| **Phi-4 preferred API** | Azure AI Model Inference (non-OpenAI model) |
| **gpt-4o preferred API** | OpenAI API (or Azure AI Model Inference) |
