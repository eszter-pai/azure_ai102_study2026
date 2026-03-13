# Module: Analyze Video with Azure Video Indexer
## Session: Capabilities, Custom Insights, Widgets, and REST API

**Sources:**
- [Understand Azure Video Indexer capabilities](https://learn.microsoft.com/en-us/training/modules/analyze-video/2-understand-video-indexer-capabilities)
- [Extract custom insights](https://learn.microsoft.com/en-us/training/modules/analyze-video/3-extract-custom-insights)
- [Use Video Indexer widgets and APIs](https://learn.microsoft.com/en-us/training/modules/analyze-video/4-use-video-indexer-widgets-apis)

---

## 1. What Is Azure Video Indexer?

> **Azure Video Indexer** = an Azure AI service that extracts insights from videos using **pre-built** and **custom** AI models; **accessible via portal, embeddable widgets, and REST API.**

---

## 2. Built-In Capabilities

> Video Indexer provides 8 types of insights out-of-the-box — no training required.

| Capability | What It Does |
|---|---|
| **Facial recognition** | Detects individual people in the video: requires **Limited Access** approval |
| **OCR (Optical Character Recognition)** | Reads text visible in the video frames |
| **Speech transcription** | Converts spoken dialogue into a text transcript |
| **Topics** | **Identifies key topics** discussed throughout the video |
| **Sentiment** | Analyzes how positive or negative segments of the video are |
| **Labels** | **Tags key objects or themes** throughout the video |
| **Content moderation** | Detects adult or violent themes |
| **Scene segmentation** | Breaks the video down into its constituent scenes |

> The Video Indexer portal allows you to **upload, view, and analyze videos interactively**, no code needed.

---

## 3. Custom Models (Extending Recognition)

> Extend Video Indexer's capabilities by training **custom models** for domain-specific recognition.

| Custom Model | What You Train It On | What It Does |
|---|---|---|
| **People** | Images of specific people's faces | Recognizes those people in all your videos: requires **Limited Access** approval |
| **Language** | Organization-specific terminology | Detects and transcribes custom terms not in common usage |
| **Brands** | **Specific names** (products, projects, companies) | Recognizes those names as brands in transcripts and visuals |

> **Limited Access** approval (Microsoft Responsible AI policy) is required for **facial recognition** features. Both built-in (celebrities) and custom people models.

---

## 4. Using Video Indexer in Custom Applications

> Two ways to integrate **Video Indexer** into your own apps.

| Method | Description | Best For |
|---|---|---|
| **Widgets** | Embed the portal's player/insights/editor UI into custom HTML | Sharing specific video insights **without full portal access** |
| **REST API** | Programmatically automate all indexing tasks | Custom apps, automation, pipelines |

---

## 5. Video Indexer Widgets

> The same **player, analysis, and editing widgets** from the Video Indexer portal can be **embedded in custom HTML pages**.

- Embed the player, insights panel, or editor widget
- Share insights from specific videos with others
- No full portal account access required for viewers

---

## 6. Video Indexer REST API

> The REST API requires an **access token** obtained first, then used in subsequent calls.

### Step 1: Get an Access Token

```http
GET https://api.videoindexer.ai/Auth/<location>/Accounts/<accountId>/AccessToken
```

| URL Placeholder | Description |
|---|---|
| `<location>` | Azure region (e.g., `trial`, `westeurope`) |
| `<accountId>` | Your **Video Indexer account ID** |

### Step 2: Use the Token in API Calls

> Pass `<accessToken>` as a query string parameter in subsequent requests.

### Common API Operations

| Operation | HTTP Method | Endpoint Pattern |
|---|---|---|
| **List videos** | GET | `/<location>/Accounts/<accountId>/Videos?<accessToken>` |
| **Get custom logo** | GET | `/<location>/Accounts/<accountId>/Customization/CustomLogos/Logos/<logoId>?<accessToken>` |
| **Create project** | POST | Various endpoints |
| **Retrieve insights** | GET | Various endpoints |
| **Create/delete custom models** | POST/DELETE | Various endpoints |

### Example: List Videos Response (JSON)

```json
{
    "accountId": "SampleAccountId",
    "id": "30e66ec1b1",
    "name": "test3",
    "description": null,
    "created": "2018-04-25T16:50:00.967+00:00",
    "lastModified": "2018-04-25T16:58:13.409+00:00",
    "lastIndexed": "2018-04-25T16:50:12.991+00:00",
    "privacyMode": "Private",
    "userName": "SampleUserName",
    "isOwned": true,
    "state": "Processing",
    "durationInSeconds": 13,
    "thumbnailVideoId": "30e66ec1b1",
    "social": {
        "likedByUser": false,
        "likes": 0,
        "views": 0
    },
    "indexingPreset": "Default",
    "streamingPreset": "Default",
    "sourceLanguage": "en-US"
}
```

### Key Response Fields

| Field | Description |
|---|---|
| `id` | Unique video ID |
| `state` | Processing state (e.g., `"Processing"`, `"Processed"`) |
| `durationInSeconds` | Video length |
| `privacyMode` | `"Private"` or `"Public"` |
| `sourceLanguage` | Detected or specified language (e.g., `"en-US"`) |
| `indexingPreset` | Indexing mode used (e.g., `"Default"`) |
| `thumbnailVideoId` | ID of the video used for thumbnail |

---

## 7. Deployment

> Video Indexer resources can be provisioned via **ARM templates** (Azure Resource Manager) for automated/repeatable deployments.

- Full API reference: [Video Indexer Developer Portal](https://api-portal.videoindexer.ai/)

---

## 8. Video Indexer vs Azure Vision

| Aspect | Azure Vision | Azure Video Indexer |
|---|---|---|
| **Input** | Static images | Videos |
| **Temporal analysis** | No | Yes (timeline, scenes, segments) |
| **Speech/audio** | No | Yes (transcription, topics) |
| **Sentiment** | No | Yes (per-segment) |
| **Custom models** | No | Yes (people, language, brands) |
| **Integration** | SDK / REST API | Portal, widgets, REST API |
| **Limited Access** | Face detection | Facial recognition |

---

## Quick Reference — Exam Tips

| Key Fact | Detail |
|---|---|
| **8 built-in capabilities** | Facial recognition, OCR, Speech transcription, Topics, Sentiment, Labels, Content moderation, Scene segmentation |
| **Limited Access required** | Facial recognition (built-in celebrities + custom people models) |
| **3 custom model types** | People, Language, Brands |
| **2 integration methods** | Widgets (embed in HTML) + REST API |
| **API auth pattern** | Get access token first → pass as query string in all subsequent calls |
| **Access token endpoint** | `https://api.videoindexer.ai/Auth/<location>/Accounts/<accountId>/AccessToken` |
| **Scene segmentation** | Breaks video into scenes — unique to Video Indexer, not in Azure Vision |
| **Content moderation** | Detects adult or violent content in video |
| **ARM template** | Used for automated provisioning of Video Indexer resource |
| **Developer portal** | `api-portal.videoindexer.ai` — full API reference |
