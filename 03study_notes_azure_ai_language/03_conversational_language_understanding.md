# Module: Build a Conversational Language Understanding Model
## Session: Prebuilt Capabilities, Resources, Intents/Utterances/Entities, Patterns, Prebuilt Entities, Train/Test/Publish

**Sources:**
- [Understand Prebuilt Capabilities of Azure Language Service](https://learn.microsoft.com/en-us/training/modules/build-language-understanding-model/2a-understand-prebuilt-capabilities)
- [Understand Resources for Building a CLU Model](https://learn.microsoft.com/en-us/training/modules/build-language-understanding-model/2-understand-resources-for-building)
- [Define Intents, Utterances, and Entities](https://learn.microsoft.com/en-us/training/modules/build-language-understanding-model/3-define-intents-utterances-entities)
- [Use Patterns to Differentiate Similar Utterances](https://learn.microsoft.com/en-us/training/modules/build-language-understanding-model/4-use-patterns-differentiate-similar-utterances)
- [Use Pre-built Entity Components](https://learn.microsoft.com/en-us/training/modules/build-language-understanding-model/5-use-pre-built-entity-components)
- [Train, Test, Publish, and Review a CLU Model](https://learn.microsoft.com/en-us/training/modules/build-language-understanding-model/6-train-test-publish-review)

---

## 1. Azure Language Service: Two Feature Categories

> Azure Language features fall into **two categories**: **Pre-configured** (no training needed) and **Learned** (require labeling + training).

### Pre-configured Features (No Training Required)

| Feature | What It Does | Example |
|---|---|---|
| **Summarization** | Summarizes documents or conversations into key sentences | Long support transcript → 3-sentence summary |
| **Named Entity Recognition (NER)** | Extracts people, places, organizations, etc. | "Seattle" → Location |
| **PII (personally identifiable information) Detection** | **Identifies and redacts** sensitive information | Email addresses, names, health info, IP addresses |
| **Key Phrase Extraction** | Pulls main concepts from text | "Text Analytics is a feature of Foundry Tools" → "Foundry Tools", "Text Analytics" |
| **Sentiment Analysis** | Identifies positive/negative/neutral tone | "Great hotel!" → Positive |
| **Language Detection** | Identifies which language text is written in | "Bonjour" → French |

### Learned Features (Require Label → Train → Deploy)

| Feature | What It Does |
|---|---|
| **Conversational Language Understanding (CLU)** | Custom model to predict **intent** and extract **entities** from **user utterances** |
| **Custom Named Entity Recognition** | Custom model to extract **specific entities from unstructured text** |
| **Custom Text Classification** | Custom model to classify text into user-defined categories |
| **Question Answering** | Mostly pre-configured; answers questions from FAQ/manual documents |

> **Quality of training data** is critical for learned feature, accuracy depends on precise, consistent, and complete labeling.

---

## 2. What Is CLU?

> **Conversational Language Understanding (CLU)** = a **learned** feature of Azure Language that lets you build a custom NLP model to **predict the overall intent** and **extract important information (entities)** from incoming user utterances.

**CLU requires:**
- Defining intents and example utterances
- Labeling entities in utterances
- Training the model
- Deploying to an endpoint

---

## 3. Azure Resources for CLU

> You need **one Azure Language resource**, used for both **authoring** (building the model) and **prediction** (querying from apps).

### Where to Create

1. Azure portal → search **Foundry Tools** → select **Language Service** → **Create**
2. Choose region closest to you (best performance), give it a unique name

### Two Ways to Build and Query

| Method | Description |
|---|---|
| **Language Studio** (`language.azure.com`) | Visual UI.  create project, label data, train, deploy, test interactively |
| **REST API** | Programmatic,  submit **JSON requests**; operations are **asynchronous** (submit job → poll for status) |

### Authentication Header (All API Calls)

```
Ocp-Apim-Subscription-Key: <your-resource-key>
```

### Two Key API Endpoints

| Purpose | Endpoint |
|---|---|
| **Pre-configured features** (NER, Sentiment, etc.) | `{ENDPOINT}/language/:analyze-text?api-version={VERSION}` |
| **CLU / Conversational** | `{ENDPOINT}/language/:analyze-conversations?api-version={VERSION}` |

### REST API: Deployment Flow (Asynchronous)

| Step | HTTP Method | Action |
|---|---|---|
| **Submit deployment** | POST | Send request to deploy a trained model |
| **Check status** | GET | Poll the `operation-location` URL from the POST response header |

Successful deployment response status: `"status": "succeeded"`

### CLU Query:  REST Request Body

```json
{
  "kind": "Conversation",
  "analysisInput": {
    "conversationItem": {
      "id": "1",
      "participantId": "1",
      "text": "Sample text"
    }
  },
  "parameters": {
    "projectName": "{PROJECT-NAME}",
    "deploymentName": "{DEPLOYMENT-NAME}",
    "stringIndexType": "TextElement_V8"
  }
}
```

### CLU Query: Response

```json
{
  "kind": "ConversationResult",
  "result": {
    "query": "String",
    "prediction": {
      "topIntent": "intent1",
      "projectKind": "Conversation",
      "intents": [
        { "category": "intent1", "confidenceScore": 1 },
        { "category": "intent2", "confidenceScore": 0 }
      ],
      "entities": [
        { "category": "entity1", "text": "text", "offset": 7, "length": 4, "confidenceScore": 1 }
      ]
    }
  }
}
```

---

## 4. Intents, Utterances, and Entities

### Core Definitions

| Term | Definition |
|---|---|
| **Utterance** | A phrase a user might enter when interacting with the application |
| **Intent** | The task or action the user wants to perform |
| **Entity** | Specific contextual information extracted from an utterance (who, what, when, where) |

> **None intent** = required in every model. Captures utterances that don't match any defined intent, use it explicitly for greetings and out-of-scope inputs.

### Example — Intents + Entities Together

| Utterance | Intent | Entities |
|---|---|---|
| "What time is it?" | GetTime | *(none)* |
| "What time is it in *London*?" | GetTime | Location: London |
| "What's the forecast for *Paris*?" | GetWeather | Location: Paris |
| "Will I need an umbrella *tonight*?" | GetWeather | Time: tonight |
| "What's the forecast for *Seattle tomorrow*?" | GetWeather | Location: Seattle, Time: tomorrow |
| "Turn the *light* on." | TurnOnDevice | Device: light |
| "Switch on the *fan*." | TurnOnDevice | Device: fan |

### 3 Types of Entities

| Entity Type | Description | Best Used For |
|---|---|---|
| **Learned** | Most flexible; defined by name and **learned from labeled utterances during training** | Most cases, when values are unpredictable |
| **List** | **Fixed set** of allowed values with optional synonyms | Days of week, product codes, categories (e.g., "Sun"/"Sunday") |
| **Prebuilt** | Auto-detects common types. **numbers, datetimes, names, organizations** | Standard types you don't want to label manually |

### Utterance Labeling Guidelines (3 Principles)

| Principle | Rule |
|---|---|
| **Label precisely** | Label each entity to its correct type. Only include what you want extracted |
| **Label consistently** | The same entity must have the same label across all utterances |
| **Label completely** | Label every instance of the entity in every utterance |

### Tips for Collecting Good Utterances

- Capture **multiple different phrasings** of the same intent
- Vary **length**: short, medium, and long
- Vary the **position** of the subject/noun (beginning, middle, end)
- Include both **correct and incorrect grammar** for realistic training data

---

## 5. Using Patterns to Differentiate Similar Utterances

> **Patterns** = template-style utterances using placeholders (e.g., `{DeviceName}`) that teach the model to handle **syntactically similar** utterances mapped to **different intents**.

### Problem: Similar Utterances, Different Intents

| Utterance | Intent |
|---|---|
| "Turn on the kitchen light" | TurnOnDevice |
| "Is the kitchen light on?" | GetDeviceStatus |
| "Turn off the kitchen light" | TurnOffDevice |

These look nearly identical but represent 3 different intents.

### Solution: Pattern Utterances with Entity Placeholders

```
TurnOnDevice:
  - "Turn on the {DeviceName}"
  - "Switch on the {DeviceName}"
  - "Turn the {DeviceName} on"

GetDeviceStatus:
  - "Is the {DeviceName} on[?]"

TurnOffDevice:
  - "Turn the {DeviceName} off"
  - "Switch off the {DeviceName}"
  - "Turn off the {DeviceName}"
```

> The model learns to distinguish intents by **format and word order**, not just vocabulary.
> `[?]` = **optional punctuation** in a pattern.

---

## 6. Prebuilt Entity Components

> **Prebuilt entity components** = predefined entity detectors for common types that require **no training examples**, the service automatically detects them.

### Common Prebuilt Entity Types

| Type | Examples Detected |
|---|---|
| Number | "6", "twenty", "3.5" |
| DateTime | Dates, times, durations |
| Email | Email addresses |
| URL | Web URLs |
| Organization | "Microsoft", "NHS" |
| Person name | Proper names |

### Key Facts

- Up to **5 prebuilt components per entity**
- No labeling needed
- Add in Language Studio: create entity → **"Add new prebuilt"**
- Significantly **reduces development time** for common entity types

---

## 7. Train, Test, Publish, and Review: Iterative Cycle

> Building a CLU model is an **iterative 4-step cycle** that repeats as the model improves.

### The 4-Step Cycle

| Step | Action | Where |
|---|---|---|
| **1. Train** | Model learns intents and entities from labeled sample utterances | Language Studio / REST API |
| **2. Test** | Evaluate the model interactively or with a labeled test dataset | Language Studio (interactive) or API |
| **3. Deploy (Publish)** | Push the trained model to a public endpoint for client apps | Language Studio / REST API (async) |
| **4. Review** | Analyze predictions from real usage; add/adjust utterances; retrain | Language Studio + production feedback |

```
Train → Test → Deploy → Review → (repeat)
```

> Each iteration improves the model based on real user input and observed failures.