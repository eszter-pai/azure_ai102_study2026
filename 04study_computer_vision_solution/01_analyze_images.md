# Module: Analyze Images with Azure Vision
## Session: Provisioning, Connecting, and Analyzing Images

**Sources:**
- [Provision an Azure Vision resource](https://learn.microsoft.com/en-us/training/modules/analyze-images/2-provision-computer-vision-resource)
- [Analyze an image](https://learn.microsoft.com/en-us/training/modules/analyze-images/3-analyze-image?pivots=csharp)

---

## 1. What Is Azure Vision?

> **Azure Vision** = an Azure AI service for analyzing images using **pre-built AI models**; accessible **via REST API or SDKs** (Python, .NET, etc.).

Part of the broader **Foundry Tools** suite, also accessible through Microsoft Foundry projects.

---

## 2. Provisioning Options

> Three ways to get access to Azure Vision, depending on your needs.

| Option | Resource Type | Best For |
|---|---|---|
| **1. Microsoft Foundry hub + project** | Foundry hub with Foundry Tools included | Teams combining **GenAI + agents + Vision in one solution** |
| **2. Foundry Tools resource** | Standalone Foundry Tools | **Access to multiple AI services** via **a single endpoint/key** |
| **3. Azure Vision standalone** | Azure Vision resource | Azure Vision only; includes a **free tier** for experimentation |

> The standalone Azure Vision resource is the simplest option and offers a **free tier**.

---

## 3. Connecting to Your Resource

> Every Azure Vision resource exposes an **endpoint URL** for client apps to connect to.

### Endpoint Format

```
https://<resource_name>.cognitiveservices.azure.com/
```

Find the endpoint in the **Azure portal** or, if using a Foundry project, in the **Microsoft Foundry portal**.

---

## 4. Authentication Methods

| Method | How It Works | When to Use |
|---|---|---|
| **Key-based** | Pass an authorization key in the request | Development / testing |
| **Microsoft Entra ID** | Use an Entra ID token tied to a role with **resource access** | **Production** (recommended) |
| **Managed identity** | Entra ID auth via Azure-managed identity | Production apps hosted in Azure |
| **Azure Key Vault** | Store and retrieve keys securely | Production apps requiring key rotation |

> In a **Foundry project**: use the Foundry SDK to connect via Entra ID, then retrieve the Foundry Tools key from the project connection.

---

## 5. Image Requirements for Analysis

> Before submitting an image, ensure it meets these constraints.

| Requirement | Value |
|---|---|
| **Supported formats** | JPEG, PNG, GIF, BMP |
| **Max file size** | 4 MB |
| **Minimum dimensions** | **50 × 50 pixels** |

---

## 6. Submitting an Image for Analysis (C#)

> Use the `ImageAnalysisClient` and specify which **visual features** you want.

```csharp
using Azure.AI.Vision.ImageAnalysis;

// Create client with key-based auth
ImageAnalysisClient client = new ImageAnalysisClient(
    "<YOUR_RESOURCE_ENDPOINT>",
    new AzureKeyCredential("<YOUR_AUTHORIZATION_KEY>"));

// Analyze image — binary bytes + requested features
ImageAnalysisResult result = client.Analyze(
    <IMAGE_DATA_BYTES>,                          // Binary data from image file
    VisualFeatures.Caption | VisualFeatures.Tags,  // Pipe-combine features
    new ImageAnalysisOptions { GenderNeutralCaption = true });
```

> To use **Microsoft Entra ID authentication**, replace `AzureKeyCredential` with a **`TokenCredential`**.

### Two Ways to Submit an Image

| Method | Description |
|---|---|
| **Binary data** | Read image file → pass bytes (`IMAGE_DATA_BYTES`) |
| **URL** | Pass a publicly accessible image URL |

---

## 7. Visual Features (VisualFeatures Enumeration)

> Specify which features to analyze using `VisualFeatures.*`. Combine with `|` (bitwise OR).

| Feature | What It Returns |
|---|---|
| `VisualFeatures.Tags` | Tags for **objects, scenery, settings, actions**, with **confidence scores** |
| `VisualFeatures.Objects` | **Bounding box** for each detected **object** |
| `VisualFeatures.Caption` | A single natural-language caption of the whole image |
| `VisualFeatures.DenseCaptions` | **Detailed captions for individual detected** objects/regions |
| `VisualFeatures.People` | Bounding box for detected people |
| `VisualFeatures.SmartCrops` | Bounding box for the best-fit crop at a given aspect ratio |
| `VisualFeatures.Read` | Extracts **readable text (OCR) from the image** |

> Most results include a **bounding box** (for spatial features) or a **confidence score** (for tags/captions).

---

## 8. Understanding the JSON Response

> The API returns a JSON document containing results for all requested features.

### Example Response (DenseCaptions)

```json
{
  "apim-request-id": "abcde-1234-5678-9012-f1g2h3i4j5k6",
  "modelVersion": "<version>",
  "denseCaptionsResult": {
    "values": [
      {
        "text": "a house in the woods",
        "confidence": 0.7055229544639587,
        "boundingBox": { "x": 0, "y": 0, "w": 640, "h": 640 }
      },
      {
        "text": "a trailer with a door and windows",
        "confidence": 0.6675070524215698,
        "boundingBox": { "x": 214, "y": 434, "w": 154, "h": 108 }
      }
    ]
  },
  "metadata": {
    "width": 640,
    "height": 640
  }
}
```

### Response Structure

| JSON Field | Description |
|---|---|
| `apim-request-id` | Unique request ID for **debugging/tracing** |
| `modelVersion` | Version of the Azure Vision model used |
| `denseCaptionsResult.values[]` | Array of captions with `text`, `confidence`, `boundingBox` |
| `metadata.width` / `metadata.height` | **Dimensions** of the analyzed image |
| `boundingBox.x`, `.y` | Top-left corner of the region (pixels) |
| `boundingBox.w`, `.h` | Width and height of the region (pixels) |

---

## 9. Key Concepts Summary

| Concept | Detail |
|---|---|
| **Client class** | `ImageAnalysisClient` (Azure.AI.Vision.ImageAnalysis) |
| **Analysis method** | `client.Analyze(imageData, features, options)` |
| **Feature selector** | `VisualFeatures` enum, pipe-combine multiple features |
| **Auth (dev)** | `AzureKeyCredential("key")` |
| **Auth (prod)** | `TokenCredential` (Microsoft Entra ID) |
| **Response format** | JSON with per-feature result blocks |

