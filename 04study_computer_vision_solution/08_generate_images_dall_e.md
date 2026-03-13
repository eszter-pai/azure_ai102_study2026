# Module: Generate Images with AI
## Session: Image Generation Models, Foundry Playground, and REST API / SDK

**Sources:**
- [What are image-generation models?](https://learn.microsoft.com/en-us/training/modules/generate-images-azure-openai/2-what-is-dall-e)
- [Explore image-generation models in Microsoft Foundry portal](https://learn.microsoft.com/en-us/training/modules/generate-images-azure-openai/3-dall-e-in-openai-studio)
- [Create a client application that uses an image generation model](https://learn.microsoft.com/en-us/training/modules/generate-images-azure-openai/4-dall-e-rest-api)

---

## 1. What Are Image Generation Models?

> **Image generation model** = a generative AI model that creates **original graphical images** from natural language descriptions (prompts).

- Input: a text prompt (e.g., `"A squirrel on a motorcycle"`)
- Output: a newly generated image — **not retrieved from a catalog**
- The model *generates* new images based on its training data — it is **not a search engine**

### Supported Models in Microsoft Foundry

| Model | Provider |
|---|---|
| **DALL-E 3** | OpenAI |
| **GPT-Image 1** | OpenAI |

> See the [Model catalog in Microsoft Foundry portal](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/model-catalog-overview) for the full current list.

---

## 2. Testing in the Foundry Portal (Images Playground)

> Use the **Images playground** in Microsoft Foundry portal to experiment with image generation interactively, no code required.

### Steps

1. Create a Microsoft Foundry project
2. Open the **Images playground**
3. Submit a natural language prompt
4. View the generated image
5. Adjust settings and regenerate

### Configurable Settings (DALL-E)

| Setting | Options | Default |
|---|---|---|
| **Resolution (size)** | `1024x1024`, `1792x1024`, `1024x1792` | `1024x1024` |
| **Style** | `vivid`, `natural` | `vivid` |
| **Quality** | `standard`, `hd` | `standard` |

---

## 3. Using the REST API

> Submit a POST request to the model endpoint with your prompt and parameters.

### Authentication

Pass your authorization key in the **request header**.

### Request Parameters (DALL-E 3)

| Parameter | Required | Description |
|---|---|---|
| `prompt` | Yes | Natural language description of the image |
| `n` | Yes | Number of images: **DALL-E 3 only supports `n=1`** |
| `size` | Yes | Resolution: `"1024x1024"`, `"1792x1024"`, or `"1024x1792"` |
| `quality` | Optional | `"standard"` (default) or `"hd"` |
| `style` | Optional | `"vivid"` (default) or `"natural"` |

### Example Request (JSON)

```json
{
    "prompt": "A badger wearing a tuxedo",
    "n": 1,
    "size": "1024x1024",
    "quality": "hd",
    "style": "vivid"
}
```

### Example Response (JSON)

```json
{
    "created": 1686780744,
    "data": [
        {
            "url": "<URL of generated image>",
            "revised_prompt": "<prompt that was used>"
        }
    ]
}
```

### Response Fields

| Field | Description |
|---|---|
| `created` | Unix timestamp of when the image was generated |
| `data[].url` | URL to the generated PNG image (view or download) |
| `data[].revised_prompt` | The prompt the system actually used (may differ from what you sent) |

> The system may **revise your prompt** automatically to achieve better results — the actual prompt used is returned in `revised_prompt`.

---

## 4. Synchronous Processing

> DALL-E 3 processes requests **synchronously** — the response is returned directly with the image URL (no polling required).

| Aspect | Detail |
|---|---|
| **Processing mode** | Synchronous |
| **Result** | Image URL returned immediately in the response |
| **Image format** | PNG |
| **Max images per request** | 1 (DALL-E 3 only supports `n=1`) |

---

## 5. SDK Options

> Instead of calling the REST API directly, use a language-specific SDK that wraps the REST calls.

| SDK | Language |
|---|---|
| **OpenAI Python SDK** | Python |
| **Azure OpenAI .NET SDK** | C# / .NET |

---

## 6. Image Generation vs Image Analysis

| Aspect | Image Generation (DALL-E) | Image Analysis (Azure Vision) |
|---|---|---|
| **Direction** | Text → Image | Image → Text/Data |
| **Input** | Natural language prompt | Image file or URL |
| **Output** | Generated PNG image | Tags, captions, bounding boxes, OCR |
| **Model type** | Generative | Analytical |
| **Result format** | URL to generated image | JSON with features |
| **Images are...** | Newly generated (original) | Analyzed (not modified) |

---

## Quick Reference — Exam Tips

| Key Fact | Detail |
|---|---|
| **Two image gen models in Foundry** | DALL-E 3, GPT-Image 1 |
| **Images are generated, not retrieved** | The model creates new images — it is not a search engine |
| **Test in** | Images playground in Microsoft Foundry portal |
| **3 size options (DALL-E 3)** | `1024x1024`, `1792x1024`, `1024x1792` |
| **Style options** | `vivid` (default) or `natural` |
| **Quality options** | `standard` (default) or `hd` |
| **DALL-E 3 n limit** | Only `n=1` supported — one image per request |
| **Processing** | Synchronous — URL returned immediately in response |
| **Response key fields** | `data[].url` (image URL) + `data[].revised_prompt` |
| **revised_prompt** | System may auto-edit your prompt for better results |
| **SDK options** | OpenAI Python SDK, Azure OpenAI .NET SDK |
