# Module: Create an Azure Content Understanding Client Application
## Session: Setup, Analyzer Creation (SDK + REST), and Content Analysis

**Sources:**
- [Prepare to use the AI Content Understanding API](https://learn.microsoft.com/en-us/training/modules/analyze-content-ai-api/02-prepare-content-understanding)
- [Create a Content Understanding analyzer](https://learn.microsoft.com/en-us/training/modules/analyze-content-ai-api/03-create-analyzer)
- [Analyze content](https://learn.microsoft.com/en-us/training/modules/analyze-content-ai-api/04-analyze)

---

## 1. Prerequisites and Setup

### Provisioning Options

| Option | Notes |
|---|---|
| **Microsoft Foundry resource** | Create directly in the Azure portal |
| **Microsoft Foundry project** | Includes a Foundry resource by default; also unlocks visual tools (Content Understanding Studio) |

### Required Connection Info

| Info | Where to Find It |
|---|---|
| **Endpoint** | Azure portal → Foundry resource → Keys and Endpoint |
| **API key** | Azure portal → Foundry resource → Keys and Endpoint |
| **Foundry project** | Also shown on the Foundry portal project home page |

> In a Foundry project you can also use the **Foundry SDK with Microsoft Entra ID** to retrieve connection details programmatically.

### Required Model Deployments

> Before using Content Understanding, you must configure these **default model deployments** on your Foundry resource.

| Model | Purpose |
|---|---|
| `GPT-4.1` | Completion (main AI model) |
| `GPT-4.1-mini` | Completion (lightweight) |
| `text-embedding-3-large` | **Embedding model** |

Configure in the **Azure portal** or via the API.

### Installing the Python SDK

```bash
pip install azure-ai-contentunderstanding
```

> Requires **Python 3.9+**. You can also use the **REST API directly from any HTTP-capable** language.

---

## 2. Analyzer Schema (JSON Definition)

> An **analyzer** is defined by a **JSON schema** that specifies what fields to extract from content.

### Schema Structure

```json
{
    "description": "Simple business card",
    "baseAnalyzerId": "prebuilt-document",
    "config": {
        "returnDetails": true
    },
    "fieldSchema": {
        "fields": {
            "ContactName": {
                "type": "string",
                "method": "extract",
                "description": "Name on business card"
            },
            "EmailAddress": {
                "type": "string",
                "method": "extract",
                "description": "Email address on business card"
            }
        }
    },
    "models": {
        "completion": "gpt-4.1",
        "embedding": "text-embedding-3-large"
    }
}
```

### Schema Fields Explained

| Field | Description |
|---|---|
| `description` | Human-readable description of the analyzer |
| `baseAnalyzerId` | Pre-built base to extend (e.g., `"prebuilt-document"`, `"prebuilt-image"`) |
| `config.returnDetails` | Return detailed OCR/layout information alongside field values |
| `fieldSchema.fields` | Dictionary of fields to extract or generate |
| `field.type` | Data type of the field (e.g., `"string"`) |
| `field.method` | `"extract"` = read value from content; `"generate"` = infer/create value |
| `field.description` | Helps the AI understand what to look for |
| `models.completion` | Generative model for processing (e.g., `"gpt-4.1"`) |
| `models.embedding` | Embedding model (e.g., `"text-embedding-3-large"`) |

### `extract` vs `generate`

| Method | Meaning |
|---|---|
| `"extract"` | Value physically exists in the content, read it out (e.g., printed name on a card) |
| `"generate"` | Value is inferred by the AI, not literally present (e.g., sentiment, summary) |

---

## 3. Creating an Analyzer: Python SDK

```python
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.core.credentials import AzureKeyCredential

# Authenticate
endpoint = "<YOUR_ENDPOINT>"
credential = AzureKeyCredential("<YOUR_API_KEY>")
client = ContentUnderstandingClient(endpoint=endpoint, credential=credential)

# Define the analyzer
analyzer_name = "business_card_analyser"
analyzer_definition = {
    "description": "Simple business card",
    "baseAnalyzerId": "prebuilt-document",
    "config": {"returnDetails": True},
    "fieldSchema": {
        "fields": {
            "ContactName": {"type": "string", "method": "extract", "description": "Name on business card"},
            "EmailAddress": {"type": "string", "method": "extract", "description": "Email address on business card"}
        }
    },
    "models": {
        "completion": "gpt-4.1",
        "embedding": "text-embedding-3-large"
    }
}

# Create the analyzer (asynchronous — poller handles waiting)
poller = client.begin_create_analyzer(analyzer_name, body=analyzer_definition)
result = poller.result()
print(f"Analyzer created: {result.analyzer_id}")
```

| SDK Method | Description |
|---|---|
| `ContentUnderstandingClient(endpoint, credential)` | Creates the authenticated client |
| `client.begin_create_analyzer(name, body=definition)` | Starts **async analyzer** creation; returns a poller |
| `poller.result()` | Blocks until creation is complete; returns the result |

---

## 4. Creating an Analyzer: REST API

> HTTP method: **PUT** submits the schema **JSON** to **create the analyzer**.

```python
import json, requests

# Load schema JSON from file
with open("card.json", "r") as file:
    schema_json = json.load(file)

analyzer_name = "business_card_analyser"
headers = {
    "Ocp-Apim-Subscription-Key": "<YOUR_API_KEY>",
    "Content-Type": "application/json"
}

# PUT request to create the analyzer
url = f"<YOUR_ENDPOINT>/contentunderstanding/analyzers/{analyzer_name}?api-version=2025-11-01"
response = requests.put(url, headers=headers, data=json.dumps(schema_json))

# Extract the callback URL from the response header
callback_url = response.headers["Operation-Location"]

# Poll until complete
result_response = requests.get(callback_url, headers=headers)
status = result_response.json().get("status")
while status == "Running":
    result_response = requests.get(callback_url, headers=headers)
    status = result_response.json().get("status")

print("Done!")
```

| REST Step | HTTP Method | Endpoint |
|---|---|---|
| Create analyzer | PUT | `/contentunderstanding/analyzers/{name}?api-version=2025-11-01` |
| Check status | GET | Value of `Operation-Location` response header |

---

## 5. Analyzing Content: Python SDK

```python
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalysisInput
from azure.core.credentials import AzureKeyCredential

client = ContentUnderstandingClient(
    endpoint="<YOUR_ENDPOINT>",
    credential=AzureKeyCredential("<YOUR_API_KEY>")
)

# Submit content for analysis
analyzer_name = "business_card_analyser"
poller = client.begin_analyze(
    analyzer_id=analyzer_name,
    inputs=[AnalysisInput(url="https://host.com/business-card.png")]
)

# Wait for completion (SDK handles polling automatically)
result = poller.result()

# Extract field values from results
content = result.contents[0]
if content.fields:
    for field_name, field_data in content.fields.items():
        if field_data.type == "string":
            print(f"{field_name}: {field_data.value}")
```

| SDK Method | Description |
|---|---|
| `client.begin_analyze(analyzer_id, inputs)` | Submits content; returns a poller |
| `AnalysisInput(url=...)` | Wraps the content URL as input |
| `poller.result()` | **Blocks and polls automatically** until complete |
| `result.contents[0].fields` | Dictionary of extracted field results |
| `field_data.type` | Field type (e.g., `"string"`) |
| `field_data.value` | Extracted value |

---

## 6. Analyzing Content: REST API

> HTTP method: **POST** submits content to the analyzer.

```python
import json, requests

analyzer_name = "business_card_analyser"
headers = {
    "Ocp-Apim-Subscription-Key": "<YOUR_API_KEY>",
    "Content-Type": "application/json"
}

# POST: submit the content URL
url = f"<YOUR_ENDPOINT>/contentunderstanding/analyzers/{analyzer_name}:analyze?api-version=2025-11-01"
request_body = {"inputs": [{"url": "https://host.com/business-card.png"}]}
response = requests.post(url, headers=headers, json=request_body)

# Extract the operation ID
id_value = response.json().get("id")

# Poll until complete
result_url = f"<YOUR_ENDPOINT>/contentunderstanding/analyzerResults/{id_value}?api-version=2025-11-01"
result_response = requests.get(result_url, headers=headers)
status = result_response.json().get("status")
while status == "Running":
    result_response = requests.get(result_url, headers=headers)
    status = result_response.json().get("status")

# Process results
if status == "Succeeded":
    result_json = result_response.json()
```

| REST Step | HTTP Method | Endpoint |
|---|---|---|
| Submit content | POST | `/analyzers/{name}:analyze?api-version=2025-11-01` |
| Submit binary | POST | `/analyzers/{name}:analyzeBinary?api-version=2025-11-01` |
| Check status / get results | GET | `/analyzerResults/{operation-id}?api-version=2025-11-01` |

---

## 7. JSON Response Structure (REST API)

```json
{
    "id": "00000000-0000-0000-0000-a00000000000",
    "status": "Succeeded",
    "result": {
        "analyzerId": "business_card_analyser",
        "apiVersion": "2025-11-01",
        "createdAt": "2025-05-16T03:51:46Z",
        "contents": [
            {
                "markdown": "John Smith\nEmail: john@contoso.com\n",
                "fields": {
                    "ContactName": {
                        "type": "string",
                        "valueString": "John Smith",
                        "confidence": 0.994
                    },
                    "EmailAddress": {
                        "type": "string",
                        "valueString": "john@contoso.com",
                        "confidence": 0.998
                    }
                },
                "kind": "document",
                "pages": [ ... ]
            }
        ]
    }
}
```

### Response Field Reference

| JSON Path | Description |
|---|---|
| `status` | `"NotStarted"` → `"Running"` → `"Succeeded"` / `"Failed"` |
| `result.contents[]` | Array of content results (one per input) |
| `contents[].markdown` | Raw text of the document in Markdown format |
| `contents[].fields` | Dictionary of extracted fields |
| `fields.{Name}.type` | Field data type (e.g., `"string"`) |
| `fields.{Name}.valueString` | Extracted string value (REST API) |
| `fields.{Name}.confidence` | Confidence score (0–1) |
| `fields.{Name}.spans` | Character offset + length in the markdown |
| `fields.{Name}.source` | Bounding box coordinates in the document |
| `contents[].pages[]` | OCR layout: words, lines per page |
| `contents[].paragraphs[]` | Paragraph-level content |

### Parsing Results (REST API)

```python
contents = result_json["result"]["contents"]
for content in contents:
    if "fields" in content:
        for field_name, field_data in content["fields"].items():
            if field_data["type"] == "string":
                print(f"{field_name}: {field_data['valueString']}")
# Output:
# ContactName: John Smith
# EmailAddress: john@contoso.com
```

---

## 8. SDK vs REST API Comparison

| Aspect | Python SDK | REST API |
|---|---|---|
| **Package** | `azure-ai-contentunderstanding` | Any HTTP library (e.g., `requests`) |
| **Auth** | `AzureKeyCredential` | `Ocp-Apim-Subscription-Key` header |
| **Create analyzer** | `begin_create_analyzer()` + `poller.result()` | PUT + poll `Operation-Location` |
| **Analyze content** | `begin_analyze()` + `poller.result()` | POST + poll `analyzerResults/{id}` |
| **Polling** | **Automatic** (SDK handles it) | **Manual** (`while status == "Running"`) |
| **Results access** | Typed objects (`field_data.value`) | Parse JSON (`field_data['valueString']`) |
| **Binary upload** | `AnalysisInput(data=...)` | `:analyzeBinary` endpoint |

---

## Quick Reference — Exam Tips

| Key Fact | Detail |
|---|---|
| **Required model deployments** | `GPT-4.1`, `GPT-4.1-mini`, `text-embedding-3-large` — must be configured first |
| **Python SDK package** | `azure-ai-contentunderstanding` |
| **Python version** | 3.9+ required |
| **Client class** | `ContentUnderstandingClient` |
| **Create analyzer HTTP method** | **PUT** (REST) / `begin_create_analyzer()` (SDK) |
| **Analyze content HTTP method** | **POST** (REST) / `begin_analyze()` (SDK) |
| **`extract` vs `generate`** | Extract = read from content; Generate = AI infers |
| **Polling (SDK)** | Automatic via `poller.result()` — no manual loop needed |
| **Polling (REST)** | Manual: loop `GET analyzerResults/{id}` until `"Succeeded"` |
| **URL vs binary** | `:analyze` + `url` field OR `:analyzeBinary` for raw file bytes |
| **Field value key (REST)** | `valueString` (not `value`) for string fields |
| **`baseAnalyzerId`** | Pre-built base analyzer to extend (e.g., `"prebuilt-document"`) |
| **API version** | `2025-11-01` |
