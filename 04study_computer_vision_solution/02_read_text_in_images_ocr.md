# Module: Read Text in Images (OCR)
## Session: Azure OCR Options, Image Analysis Read API, and Python SDK

**Sources:**
- [Explore Azure AI options for reading text](https://learn.microsoft.com/en-us/training/modules/read-text-images-documents-with-computer-vision-service/2-options-read-text)
- [Read text with Azure Vision Image Analysis (Python)](https://learn.microsoft.com/en-us/training/modules/read-text-images-documents-with-computer-vision-service/4-use-read-api?pivots=python)

---

## 1. Azure Services That Can Read Text

> Three Azure services can extract text from images/documents — choose based on your content type and use case.

| Service | Best For |
|---|---|
| **Azure Vision** | General images, photos, scanned documents: **OCR via image analysis** |
| **Azure Document Intelligence** | **Structured forms**, invoices, receipts, tables, key-value pairs |
| **Azure Content Understanding** | **Multimodal** content: documents, images, audio, and video |

---

## 2. Azure Vision (OCR)

> This module focuses on the **OCR feature inside Azure Vision Image Analysis**.

| Scenario | Why Azure Vision |
|---|---|
| **Scanned documents** | General, **unstructured** docs (labels, menus, business cards) |
| **Photographs with text** | Street signs, store names, handwritten notes in photos |
| **Digital asset management (DAM)** | Combines OCR + object detection + captions + **smart crop** in one call |

> Azure Vision is ideal when you need **text + other image analysis** (objects, captions, tags) in a single request.

---

## 3. Azure Document Intelligence

| Capability | Description |
|---|---|
| **Form processing** | Extracts data from forms, invoices, receipts, **structured** documents |
| **Prebuilt models** | **Ready-made** models for common document types (**no training** needed) |
| **Custom models** | Train models on your own document layouts |

---

## 4. Azure Content Understanding

| Capability | Description |
|---|---|
| **Multimodal extraction** | Documents, forms, images, audio streams, video |
| **Custom analyzers** |**Define fields/content to extract per business need** |

---

## 5. Resource Provisioning for Azure Vision OCR

> Same resources as image analysis, Azure Vision OCR uses the same endpoint.

| Resource Type | How Deployed |
|---|---|
| **Foundry Tools** | As part of a Microsoft Foundry hub/project, or standalone |
| **Azure Vision** | Standalone resource in Azure subscription |

**Endpoint format:**
```
https://<resource_name>.cognitiveservices.azure.com/
```

---

## 6. REST API for OCR

> Call the `imageanalysis:analyze` endpoint with `features=read`.

```
GET https://<endpoint>/computervision/imageanalysis:analyze?features=read&...
```

Pass the image as a URL or binary data, and optionally specify a `language` parameter (default: `en`).

---

## 7. Python SDK: Reading Text with Azure Vision

### Package to Install

```bash
pip install azure-ai-vision-imageanalysis
```

### Key Classes

| Class / Enum | Purpose |
|---|---|
| `ImageAnalysisClient` | Main client — connects to Azure Vision resource |
| `VisualFeatures.READ` | Enum value that enables OCR |
| `AzureKeyCredential` | Key-based authentication |

### Full Code Example

```python
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

# Connect to Azure Vision resource
client = ImageAnalysisClient(
    endpoint="<YOUR_RESOURCE_ENDPOINT>",
    credential=AzureKeyCredential("<YOUR_AUTHORIZATION_KEY>")
)

# Analyze image for text (OCR)
result = client.analyze(
    image_data=<IMAGE_DATA_BYTES>,       # Binary data from image file
    visual_features=[VisualFeatures.READ],
    language="en",                        # Optional — defaults to English
)
```

> For a **URL-based image** instead of binary data, use `client.analyze_from_url(...)`.

### Two Ways to Submit an Image

| Method | Code |
|---|---|
| **Binary file** | `client.analyze(image_data=<bytes>, ...)` |
| **URL** | `client.analyze_from_url(url="<url>", ...)` |

---

## 8. Understanding the OCR Response

> Results are returned **synchronously** as JSON (or equivalent SDK object). Structured as: **blocks → lines → words**.

### Response Hierarchy

```
readResult
  └── blocks[]            ← Currently always 1 block
        └── lines[]       ← Each line of detected text
              ├── text                ← Full line text string
              ├── boundingPolygon[]   ← 4 polygon points for the line
              └── words[]            ← Individual words in the line
                    ├── text          ← Word string
                    ├── boundingPolygon[]  ← 4 polygon points for the word
                    └── confidence    ← 0.0–1.0 confidence score
```

### Full Example JSON Response

```json
{
    "metadata": {
        "width": 500,
        "height": 430
    },
    "readResult": {
        "blocks": [
            {
                "lines": [
                    {
                        "text": "Hello World!",
                        "boundingPolygon": [
                            {"x": 251, "y": 265},
                            {"x": 673, "y": 260},
                            {"x": 674, "y": 308},
                            {"x": 252, "y": 318}
                        ],
                        "words": [
                            {
                                "text": "Hello",
                                "boundingPolygon": [
                                    {"x": 252, "y": 267},
                                    {"x": 307, "y": 265},
                                    {"x": 307, "y": 318},
                                    {"x": 253, "y": 318}
                                ],
                                "confidence": 0.996
                            },
                            {
                                "text": "World!",
                                "boundingPolygon": [
                                    {"x": 318, "y": 264},
                                    {"x": 386, "y": 263},
                                    {"x": 387, "y": 316},
                                    {"x": 319, "y": 318}
                                ],
                                "confidence": 0.99
                            }
                        ]
                    }
                ]
            }
        ]
    }
}
```

### Response Fields Explained

| Field | Description |
|---|---|
| `metadata.width` / `.height` | Dimensions of the analyzed image in pixels |
| `readResult.blocks[]` | Top-level grouping (currently always 1 block) |
| `lines[].text` | Full text of the line |
| `lines[].boundingPolygon` | 4 `{x, y}` points defining the line's position |
| `words[].text` | Individual word string |
| `words[].boundingPolygon` | 4 `{x, y}` points defining the word's position |
| `words[].confidence` | How confident the model is (0.0–1.0) |

### Text Available at Two Levels

| Level | Use Case |
|---|---|
| **Line** (`lines[].text`) | When you need full sentences/lines — simpler iteration |
| **Word** (`words[].text`) | When you need individual word positions or confidence |

> Text is available at **both** line and word level — use line-level for most scenarios to keep code simple.

---

## 9. Processing OCR Results in Python

```python
# Iterate over detected lines and words
if result.read is not None:
    for block in result.read.blocks:
        for line in block.lines:
            print(f"Line: {line.text}")
            for word in line.words:
                print(f"  Word: {word.text}  (confidence: {word.confidence:.3f})")
```

---

## 10. Comparison: Azure Vision OCR vs Document Intelligence vs Content Understanding

| Aspect | Azure Vision | Document Intelligence | Content Understanding |
|---|---|---|---|
| **Primary use** | OCR in images/photos | Structured forms & documents | Multimodal (image + audio + video) |
| **Input types** | Images (JPEG, PNG, GIF, BMP) | PDFs, images, forms | Documents, images, audio, video |
| **Output** | text, bounding polygons | Key-value pairs, tables, fields | Structured fields per analyzer |
| **Prebuilt models** | OCR only | Invoices, receipts, IDs, etc. | Custom analyzers |
| **Custom training** | No | Yes | Yes |
| **Combined with other vision** | Yes (tags, captions, objects) | No | No |

---

## Quick Reference — Exam Tips

| Key Fact | Detail |
|---|---|
| **3 Azure text-reading services** | Azure Vision (OCR), Document Intelligence (forms), Content Understanding (multimodal) |
| **Azure Vision OCR best for** | General images, photos, scanned docs — especially when combined with other vision features |
| **Document Intelligence best for** | Structured forms, invoices, receipts — key-value pairs + tables |
| **Python package** | `azure-ai-vision-imageanalysis` |
| **Client class** | `ImageAnalysisClient` |
| **OCR feature enum** | `VisualFeatures.READ` |
| **Response structure** | blocks → lines → words |
| **Text available at** | Both **line** level and **word** level |
| **Confidence score** | At the **word** level (0.0–1.0) |
| **Bounding polygon** | 4 `{x, y}` points — at both line and word level |
| **Default language** | `"en"` (English) |
| **Results are** | **Synchronous** (not async/polling like some older APIs) |
