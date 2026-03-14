# Module: Create a Multimodal Analysis Solution with Azure Content Understanding
## Session: Service Overview, Analyzer Creation, and Content Understanding API

**Sources:**
- [What is Azure Content Understanding?](https://learn.microsoft.com/en-us/training/modules/analyze-content-ai/02-content-understanding)
- [Create a Content Understanding analyzer](https://learn.microsoft.com/en-us/training/modules/analyze-content-ai/03-create-analyzer)
- [Use the Content Understanding API](https://learn.microsoft.com/en-us/training/modules/analyze-content-ai/04-use-api)

---

## 1. What Is Azure Content Understanding?

> **Azure Content Understanding** = a generative AI service that extracts insights and structured data from **multiple content types** (documents, images, audio, video) using a single, consistent API.

- Available through **Microsoft Foundry**
- Build applications that **analyze complex data** and generate outputs to **automate and optimize processes**

### Three Ways to Use It

| Method | Description |
|---|---|
| **Microsoft Foundry portal** | Manage and develop via the portal UI |
| **Content Understanding Studio** | Visual interface for creating, testing, and refining analyzers (`ai.azure.com/contentunderstanding`) |
| **Content Understanding API** | Programmatic access via REST API or language SDKs |

---

## 2. Supported Content Types (Multimodal)

> Content Understanding supports **four content types**, enabling a single service for multimodal analysis.

| Content Type | Example Use Cases |
|---|---|
| **Documents and forms** | Extract field values from invoices to automate payment processing |
| **Images** | Analyze charts, detect **product defects**, identify objects or people |
| **Audio** | Summarize conference calls, determine sentiment of customer calls, extract data from voicemail |
| **Video** | Extract key points from recordings, summarize presentations, detect activity in security footage |

---

## 3. Core Concept: Analyzer + Schema

> A **Content Understanding solution** is built around an **analyzer**, trained to extract specific fields from a content type based on a **schema** you define.

| Concept | Description |
|---|---|
| **Analyzer** | The trained component that extracts data from content |
| **Schema** | Defines what fields to extract; based on a content sample + template |
| **Analyzer template** | Pre-built starting point for common scenarios, speeds up schema definition |
| **Named version** | After building, you can refine and save new schema versions |

> Because of generative AI capabilities, you need **minimal training data**, the service often maps schema fields to content values automatically from a single sample.

---

## 4. 4-Step Process to Build a Solution

| Step | Action |
|---|---|
| **1** | Create a **Foundry resource** |
| **2** | Define a **Content Understanding schema** (based on a sample file + analyzer template) |
| **3** | **Build** the analyzer (makes it accessible via endpoint) |
| **4** | **Use** the analyzer to extract/generate fields from new content |

---

## 5. Creating an Analyzer in Content Understanding Studio

> **Content Understanding Studio** (`ai.azure.com/contentunderstanding`) is the visual tool for custom analyzer creation, not all features are available in the standard Foundry portal.

### Steps in Content Understanding Studio

| Step | Detail |
|---|---|
| **1. Create a project** | Associate with a Foundry resource; provisions storage + Key Vault automatically |
| **2. Define a schema** | Upload a sample file (doc/image/audio/video) → apply template → define fields |
| **3. Test** | Run analysis on sample or new files; view extracted values + JSON output |
| **4. Build** | Publishes the analyzer to the Foundry endpoint for client apps to call |
| **5. Refine** | Edit schema → create new named versions |

### Schema Notes

| Note | Detail |
|---|---|
| **Templates depend on content type** | Different fields and options available per type |
| **Optional extras (documents)** | Barcodes, formulae extraction |
| **Explicit labeling** | You can manually label fields in documents to improve accuracy |
| **Region support** | Schemas can only be created in regions where Content Understanding is supported |

---

## 6. Using the Content Understanding API

> The API uses a **2-step asynchronous pattern**: submit content → poll for results.

### Authentication

| Method | Details |
|---|---|
| **Key-based** | Pass authorization key in the request header |
| **Microsoft Entra ID** | Use Foundry API with Entra ID credentials |

Obtain the endpoint and keys from the **Azure portal** or **Microsoft Foundry portal**.

---

### Step 1: Submit Content for Analysis (POST)

```http
POST {endpoint}/contentunderstanding/analyzers/{analyzer}:analyze?api-version=2025-11-01
```

**Request body (URL input):**

```json
{
  "inputs": [
    {
      "url": "https://host.com/doc.pdf"
    }
  ]
}
```

> To submit **binary file data** directly instead of a URL, use the `analyzeBinary` operation.

**Response:**

```http
Operation-Id: 1234abcd-1234-abcd-1234-abcd1234abcd
Operation-Location: {endpoint}/contentunderstanding/analyzerResults/1234abcd-1234-abcd-1234-abcd1234abcd?api-version=2025-11-01
{
  "id": "1234abcd-1234-abcd-1234-abcd1234abcd",
  "status": "NotStarted"
}
```

| Response Field | Description |
|---|---|
| `id` | The **Operation ID** — used in the poll request |
| `status` | Initial status: `"NotStarted"` |
| `Operation-Location` | Full URL to poll for results |

---

### Step 2: Poll for Results (GET)

```http
GET {endpoint}/contentunderstanding/analyzerResults/{operation-id}?api-version=2025-11-01
```

- Poll repeatedly until `status` is `"Succeeded"` (or `"Failed"`)
- When complete: response body contains the **JSON payload** with extracted field values

---

## 7. Asynchronous Pattern Summary

```
Client                              Content Understanding API
  |                                          |
  |-- POST :analyze (content URL/binary) --> |
  |<-- 202 Accepted + Operation ID --------- |
  |                                          |
  |-- GET analyzerResults/{id} -----------> |  (poll)
  |<-- status: "Running" ------------------- |
  |                                          |
  |-- GET analyzerResults/{id} -----------> |  (poll again)
  |<-- status: "Succeeded" + JSON results -- |
```

| Operation | HTTP Method | Endpoint suffix |
|---|---|---|
| Submit content | POST | `/analyzers/{name}:analyze` |
| Submit binary | POST | `/analyzers/{name}:analyzeBinary` |
| Check status / get results | GET | `/analyzerResults/{operation-id}` |

---

## 8. Content Understanding vs Azure Vision vs Document Intelligence

| Aspect | Azure Vision | Document Intelligence | Azure Content Understanding |
|---|---|---|---|
| **Content types** | Images | Documents/forms | Documents, images, audio, **video** |
| **Output** | Tags, captions, bounding boxes | Structured form fields | Custom schema-defined fields |
| **Training needed** | None (pre-built) | Pre-built + custom models | Schema-based (minimal samples) |
| **Custom schema** | No | Yes (custom models) | **Yes — core concept** |
| **Multimodal** | No | No | **Yes** |
| **Studio** | Foundry portal | Document Intelligence Studio | Content Understanding Studio |

---

## Quick Reference — Exam Tips

| Key Fact | Detail |
|---|---|
| **4 supported content types** | Documents/forms, Images, Audio, Video |
| **Core building block** | **Analyzer** + **Schema** (not a pre-built model) |
| **Minimal training data** | Generative AI infers field mappings from a single sample |
| **Custom analyzer creation** | Use **Content Understanding Studio** (`ai.azure.com/contentunderstanding`) — not the standard Foundry portal |
| **Project provisioning** | Automatically creates storage + Key Vault |
| **API pattern** | Asynchronous: POST → get Operation ID → GET poll until `"Succeeded"` |
| **URL vs binary** | `:analyze` for URL input; `:analyzeBinary` for direct binary upload |
| **API version** | `2025-11-01` |
| **Auth options** | Key in header OR Microsoft Entra ID via Foundry API |
| **Named versions** | After building, refine schema → save as new named version |
