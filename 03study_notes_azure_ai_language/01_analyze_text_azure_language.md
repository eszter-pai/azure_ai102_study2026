# Module: Analyze Text with Azure Language
## Session: Language Detection, Key Phrases, Sentiment, NER, Entity Linking

**Sources:**
- [Provision an Azure Language Resource](https://learn.microsoft.com/en-us/training/modules/analyze-text-ai-language/2-provision-resource)
- [Detect Language](https://learn.microsoft.com/en-us/training/modules/analyze-text-ai-language/3-detect-language)
- [Extract Key Phrases](https://learn.microsoft.com/en-us/training/modules/analyze-text-ai-language/4-extract-key-phrases)
- [Analyze Sentiment](https://learn.microsoft.com/en-us/training/modules/analyze-text-ai-language/5-analyze-sentiment)
- [Extract Entities (NER)](https://learn.microsoft.com/en-us/training/modules/analyze-text-ai-language/6-extract-entities)
- [Extract Linked Entities](https://learn.microsoft.com/en-us/training/modules/analyze-text-ai-language/7-extract-linked-entities)

---

## 1. What Is Azure Language?

> **Azure Language** = an Azure AI service designed to **extract information and insights from text**. It provides multiple **pre-built NLP capabilitie**s via API.

### 5 Core Capabilities

| Capability | What It Does |
|---|---|
| **Language Detection** | Determines the language in which text is written |
| **Key Phrase Extraction** | Identifies important words and phrases that indicate the main points |
| **Sentiment Analysis** | Quantifies how positive or negative the text is |
| **Named Entity Recognition (NER)** | Detects references to entities: locations, time periods, organizations, etc. |
| **Entity Linking** | Identifies specific entities and **provides reference links to Wikipedia articles** |

---

## 2. Provisioning an Azure Language Resource

> To use Azure Language, you must **provision a resource** in your Azure subscription (via the Azure portal or Microsoft Foundry portal).

### Authentication

| Value | Purpose |
|---|---|
| **Endpoint** | The URL of your Azure Language resource |
| **Key** | One of the resource's API keys for authentication |

### 2 Ways to Call the API

| Method | Description |
|---|---|
| **REST interface** | Submit requests as **JSON** and receive JSON responses |
| **SDK** | Use language-specific SDKs (Python, C#, etc.). JSON is abstracted by objects and methods |

> Both methods exchange the same underlying data values.

---

## 3. Language Detection

> **Language Detection** = evaluates text input and returns a **language identifier + confidence score** for each document submitted.

### Use Cases
- Content stores **where language is unknown**
- Chat bots that need to respond in the user's language

### Request Format (`kind`: `"LanguageDetection"`)

```json
{
    "kind": "LanguageDetection",
    "parameters": { "modelVersion": "latest" },
    "analysisInput": {
        "documents": [
            { "id": "1", "text": "Hello world", "countryHint": "US" },
            { "id": "2", "text": "Bonjour tout le monde" }
        ]
    }
}
```

> Optional: `countryHint` improves prediction performance by providing a country context.

### Response Format

```json
{
    "kind": "LanguageDetectionResults",
    "results": {
        "documents": [
            {
                "detectedLanguage": {
                    "confidenceScore": 1,
                    "iso6391Name": "en",
                    "name": "English"
                },
                "id": "1",
                "warnings": []
            }
        ]
    }
}
```

### Response Fields

| Field | Description |
|---|---|
| `name` | Full language name (e.g., "English", "French") |
| `iso6391Name` | ISO 639-1 language code (e.g., `"en"`, `"fr"`) |
| `confidenceScore` | 0 to 1 If closer to 1 = higher confidence |

### 3 Special Cases

| Scenario | Behavior |
|---|---|
| **Single language** | Returns that language with high confidence (close to 1.0) |
| **Mixed language** | Returns the **predominant language** with a **lower confidence score** |
| **Ambiguous / unparseable** | Returns `"(Unknown)"` for name and ISO code; `confidenceScore: 0.0` |

### Limits
- Max document size: **5,120 characters**
- Max collection size: **1,000 items (IDs)**

---

## 4. Key Phrase Extraction

> **Key Phrase Extraction** = evaluates a document and identifies the **main points / most important words and phrases** based on context.

### Use Cases
- Summarizing the topics of a document
- Tagging content for search indexing
- Routing documents by subject matter

### Key Detail
- Works **best for larger documents** (short text gives less context)
- Max document size: **5,120 characters**

### Request Format (`kind`: `"KeyPhraseExtraction"`)

```json
{
    "kind": "KeyPhraseExtraction",
    "parameters": { "modelVersion": "latest" },
    "analysisInput": {
        "documents": [
            { "id": "1", "language": "en", "text": "You must be the change you wish to see in the world." },
            { "id": "2", "language": "en", "text": "The journey of a thousand miles begins with a single step." }
        ]
    }
}
```

> Note: **`language` field is required** for key phrase extraction.

### Response Format

```json
{
    "kind": "KeyPhraseExtractionResults",
    "results": {
        "documents": [
            { "id": "1", "keyPhrases": ["change", "world"], "warnings": [] },
            { "id": "2", "keyPhrases": ["miles", "single step", "journey"], "warnings": [] }
        ]
    }
}
```

> Response contains a **list of key phrases** per document. no scores.

---

## 5. Sentiment Analysis

> **Sentiment Analysis** = evaluates how **positive or negative** a text document is. Returns sentiment labels and confidence scores at both **document level** and **sentence level**.

### Use Cases
- Evaluating movie, book, or product reviews
- Prioritizing customer service responses (email, social media)
- Brand monitoring

### Request Format (`kind`: `"SentimentAnalysis"`)

```json
{
    "kind": "SentimentAnalysis",
    "parameters": { "modelVersion": "latest" },
    "analysisInput": {
        "documents": [
            { "id": "1", "language": "en", "text": "Good morning!" }
        ]
    }
}
```

### Response Format

```json
{
    "kind": "SentimentAnalysisResults",
    "results": {
        "documents": [
            {
                "id": "1",
                "sentiment": "positive",
                "confidenceScores": { "positive": 0.89, "neutral": 0.1, "negative": 0.01 },
                "sentences": [
                    {
                        "sentiment": "positive",
                        "confidenceScores": { "positive": 0.89, "neutral": 0.1, "negative": 0.01 },
                        "offset": 0,
                        "length": 13,
                        "text": "Good morning!"
                    }
                ],
                "warnings": []
            }
        ]
    }
}
```

### Sentiment Labels

| Label | Description |
|---|---|
| `positive` | Text conveys positive sentiment |
| `neutral` | Text is neither positive nor negative |
| `negative` | Text conveys negative sentiment |
| `mixed` | Document contains both positive and negative sentences |

### Confidence Scores
- Three scores per result: `positive`, `neutral`, `negative`
- Each is a value **0 to 1**; all three together reflect the model's certainty

### Document-Level Sentiment Rules

| Sentence Sentiments | Overall Document Sentiment |
|---|---|
| All neutral | **Neutral** |
| Only positive + neutral | **Positive** |
| Only negative + neutral | **Negative** |
| Both positive and negative | **Mixed** |

> Both **document-level** and **sentence-level** sentiment are returned in every response.

---

## 6. Named Entity Recognition (NER)

> **NER** = identifies **entities mentioned in text** and groups them into **categories and subcategories**.

### Entity Categories

| Category | Example |
|---|---|
| **Person** | "Joe", "Marie Curie" |
| **Location** | "London", "Paris" (subcategory: GPE = Geopolitical Entity) |
| **DateTime** | "Saturday", "2024-01-15" (subcategory: Date, Time) |
| **Organization** | "Microsoft", "United Nations" |
| **Address** | Street addresses |
| **Email** | Email addresses |
| **URL** | Web URLs |

> For the full category list, see the Azure AI Language documentation.

### Request Format (`kind`: `"EntityRecognition"`)

```json
{
    "kind": "EntityRecognition",
    "parameters": { "modelVersion": "latest" },
    "analysisInput": {
        "documents": [
            { "id": "1", "language": "en", "text": "Joe went to London on Saturday" }
        ]
    }
}
```

### Response Format

```json
{
    "kind": "EntityRecognitionResults",
    "results": {
        "documents": [
            {
                "entities": [
                    { "text": "Joe", "category": "Person", "offset": 0, "length": 3, "confidenceScore": 0.62 },
                    { "text": "London", "category": "Location", "subcategory": "GPE", "offset": 12, "length": 6, "confidenceScore": 0.88 },
                    { "text": "Saturday", "category": "DateTime", "subcategory": "Date", "offset": 22, "length": 8, "confidenceScore": 0.8 }
                ],
                "id": "1",
                "warnings": []
            }
        ]
    }
}
```

### Response Fields per Entity

| Field | Description |
|---|---|
| `text` | The exact text of the entity as it appeared |
| `category` | Top-level category (e.g., Person, Location) |
| `subcategory` | More specific classification (e.g., GPE, Date) — not always present |
| `offset` | Character position where the entity starts in the text |
| `length` | Number of characters in the entity |
| `confidenceScore` | 0 to 1

---

## 7. Entity Linking

> **Entity Linking** = **disambiguates** entities of the same name by linking them to **Wikipedia articles**. Used when the same word could refer to different things.

### How It Differs from NER

| Feature | NER | Entity Linking |
|---|---|---|
| **Purpose** | Identify and categorize entities | Identify + **disambiguate** by linking to knowledge base |
| **Output** | Category + confidence score | Wikipedia URL + Bing ID + match confidence |
| **Knowledge base** | None | **Wikipedia** (via Bing) |
| **Use case** | "London" → Location | "Venus" → planet or goddess? → links to correct article |

### Disambiguation Example

| Text | Linked To |
|---|---|
| "I saw Venus shining in the sky" | `https://en.wikipedia.org/wiki/Venus` (planet) |
| "Venus, the goddess of beauty" | `https://en.wikipedia.org/wiki/Venus_(mythology)` |

### Request Format (`kind`: `"EntityLinking"`)

```json
{
    "kind": "EntityLinking",
    "parameters": { "modelVersion": "latest" },
    "analysisInput": {
        "documents": [
            { "id": "1", "language": "en", "text": "I saw Venus shining in the sky" }
        ]
    }
}
```

### Response Format

```json
{
    "kind": "EntityLinkingResults",
    "results": {
        "documents": [
            {
                "id": "1",
                "entities": [
                    {
                        "bingId": "89253af3-5b63-e620-9227-f839138139f6",
                        "name": "Venus",
                        "matches": [
                            { "text": "Venus", "offset": 6, "length": 5, "confidenceScore": 0.01 }
                        ],
                        "language": "en",
                        "id": "Venus",
                        "url": "https://en.wikipedia.org/wiki/Venus",
                        "dataSource": "Wikipedia"
                    }
                ],
                "warnings": []
            }
        ]
    }
}
```

### Response Fields per Linked Entity

| Field | Description |
|---|---|
| `name` | Canonical name of the entity (e.g., "Venus") |
| `bingId` | Bing knowledge base identifier |
| `url` | Link to the **Wikipedia article** for this specific entity |
| `dataSource` | Always `"Wikipedia"` for entity linking |
| `matches` | List of text spans in the document that matched this entity |
| `confidenceScore` (in matches) | Confidence that this text span refers to the linked entity |

---

## 8. All 5 Capabilities — Side-by-Side Comparison

| Capability | `kind` Value | Input Required | Key Output | Returns Score? |
|---|---|---|---|---|
| **Language Detection** | `LanguageDetection` | `text` (+ optional `countryHint`) | `name`, `iso6391Name`, `confidenceScore` | Yes (0–1) |
| **Key Phrase Extraction** | `KeyPhraseExtraction` | `text`, `language` | List of `keyPhrases` | No |
| **Sentiment Analysis** | `SentimentAnalysis` | `text`, `language` | `sentiment` label + `confidenceScores` (pos/neu/neg) | Yes (0–1 per label) |
| **NER** | `EntityRecognition` | `text`, `language` | `category`, `subcategory`, `offset`, `length`, `confidenceScore` | Yes (0–1) |
| **Entity Linking** | `EntityLinking` | `text`, `language` | `name`, `url`, `bingId`, `dataSource`, `matches` | Yes (in matches) |

---

## 9. Common Request Structure

All Azure Language API calls share the same pattern:

```json
{
    "kind": "<CapabilityKind>",
    "parameters": { "modelVersion": "latest" },
    "analysisInput": {
        "documents": [
            { "id": "<unique_id>", "language": "<lang_code>", "text": "<your_text>" }
        ]
    }
}
```

> **`language`** field is optional for language detection (it's detecting the language) but **required** for all other capabilities.
