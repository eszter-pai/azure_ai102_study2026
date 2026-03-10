# Module: Create Question Answering Solutions with Azure Language
## Session: Knowledge Base, Multi-Turn, Publishing, Client API, Active Learning

**Sources:**
- [Understand Question Answering](https://learn.microsoft.com/en-us/training/modules/create-question-answer-solution-ai-language/2-understand-question-answer-capability)
- [Compare to Language Understanding](https://learn.microsoft.com/en-us/training/modules/create-question-answer-solution-ai-language/3-compare-to-language-understanding)
- [Create a Knowledge Base](https://learn.microsoft.com/en-us/training/modules/create-question-answer-solution-ai-language/4-create-knowledge-base)
- [Implement Multi-Turn Conversation](https://learn.microsoft.com/en-us/training/modules/create-question-answer-solution-ai-language/5-implement-multi-turn-conversation)
- [Test and Publish a Knowledge Base](https://learn.microsoft.com/en-us/training/modules/create-question-answer-solution-ai-language/6-test-publish-knowledge-base)
- [Use a Knowledge Base (Client API)](https://learn.microsoft.com/en-us/training/modules/create-question-answer-solution-ai-language/7-consume-client-interfaces)
- [Improve Performance — Active Learning & Synonyms](https://learn.microsoft.com/en-us/training/modules/create-question-answer-solution-ai-language/8-implement-active-learning)

---

## 1. What Is Question Answering in Azure Language?

> **Question Answering** = a capability of Azure Language that lets you define a **knowledge base** of **question-and-answer pairs** which can be queried using **natural language input**.

- The knowledge base is published to a **REST endpoint**
- Consumed by **client applications**, commonly **bots**
- Successor to the older **QnA Maker** service (QnA Maker still exists as standalone)

### 3 Sources for Building a Knowledge Base

| Source Type | Description |
|---|---|
| **FAQ web pages** | URLs for **web pages containing frequently asked questions** |
| **Structured text files** | Files such as **brochures or user guides** containing Q&A-like content |
| **Chit-chat datasets** | Built-in predefined conversational exchanges (e.g., greetings, jokes) in a specified style |

---

## 2. Question Answering vs. Language Understanding

> Both are natural language capabilities in Azure Language — but they solve **different problems**.

| Aspect | Question Answering | Language Understanding |
|---|---|---|
| **Usage pattern** | User submits a **question**, expects an **answer** | User submits an **utterance**, expects a **response or action** |
| **Query processing** | Matches question to a **static answer** in the knowledge base | Interprets utterance, identifies **intent** and **entities** |
| **Response** | A **static answer** to a known question | The most likely **intent** + referenced **entities** |
| **Client logic** | Client **presents the answer** to the user | Client is responsible for **performing the appropriate action** |

> They are **complementary**, you can combine both in one solution (e.g., language understanding routes to the right knowledge base).

### Decision Guide

| Scenario | Use |
|---|---|
| "What are your opening hours?" | **Question Answering** |
| "Book me a flight to Paris tomorrow" | **Language Understanding** |
| FAQ bot / customer support bot | **Question Answering** |
| App that takes actions based on commands | **Language Understanding** |

---

## 3. Creating a Knowledge Base

> The main tool for creating and managing a knowledge base is **Language Studio** (`language.azure.com`).

### 7-Step Setup Process

| Step | Action |
|---|---|
| **1** | Sign in to Azure portal |
| **2** | Search for **Foundry Tools** → select **Language Service** resource |
| **3** | Create a resource with **question answering feature enabled** |
| **4** | Create or select an **Azure AI Search** resource to host the knowledge base index |
| **5** | In **Language Studio**, select your Azure Language resource and create a **Custom question answering** project |
| **6** | Add data sources: FAQ URLs, structured text files, and/or chit-chat datasets |
| **7** | Edit and refine question-and-answer pairs in the portal |

### Key Components

| Component | Description |
|---|---|
| **Azure Language resource** | The service that powers question answering |
| **Azure AI Search** | **Backend index that stores and retrieves the knowledge base **content |
| **Language Studio** | **Web UI** for building, managing, and testing the knowledge base |
| **Chit-chat** | Built-in small-talk Q&A sets (e.g., "How are you?" → "I'm doing great!") in a selectable style |

> You can also use the **REST API or SDK** to define, train, and publish programmatically, but Language Studio is the most common approach.

---

## 4. Multi-Turn Conversation

> **Multi-turn conversation** = when a single question isn't enough to provide a definitive answer, the knowledge base asks **follow-up questions** to clarify before responding.

### When to Use Multi-Turn

- When the answer depends on **additional context** the user hasn't provided
- When one question could refer to multiple scenarios (e.g., "cancel a reservation" → hotel or flight?)

### How It Works

```
User: "How can I cancel a reservation?"
           ↓
Bot: "Cancellation policies depend on the type of reservation."
     → [Cancel a flight]  → [Cancel a hotel]
           ↓ (user selects)
Bot: Provides specific cancellation answer for chosen type
```

### How to Set Up Multi-Turn

| Method | Description |
|---|---|
| **Import from web page/document** | Multi-turn is enabled automatically based on the **structure** of the source (e.g., nested FAQ headings) |
| **Manually define** | Add **follow-up prompts and responses** to existing Q&A pairs in Language Studio |

### Follow-Up Prompt Options

| Option | Description |
|---|---|
| **Link to existing answer** | Reuse an already-defined Q&A pair as the follow-up answer |
| **Define a new answer** | Write a new answer specifically for this follow-up context |
| **Restrict answer context** | Limit the linked answer so it **only appears within this multi-turn flow** (not accessible as a standalone answer) |

---

## 5. Testing and Publishing a Knowledge Base

### Testing

- Done interactively in **Language Studio**
- Submit test questions and review returned answers
- Inspect **confidence scores** and **alternative answers**
- Refine Q&A pairs based on test results before publishing

### Publishing / Deploying

- When satisfied with performance, **deploy** directly from Language Studio
- Deployment creates a **REST endpoint** that client applications use
- After deployment, clients can submit questions and receive answers via the REST API

---

## 6. Using the Knowledge Base: Client API

### Request Format

```json
{
  "question": "What do I need to do to cancel a reservation?",
  "top": 2,
  "scoreThreshold": 20,
  "strictFilters": [
    {
      "name": "category",
      "value": "api"
    }
  ]
}
```

### Request Properties

| Property | Description |
|---|---|
| `question` | The natural language question to send to the knowledge base |
| `top` | **Maximum number of answers** to return |
| `scoreThreshold` | **Minimum confidence score**, answers below this are excluded |
| `strictFilters` | Limits results to answers that match specified **metadata** (name/value pairs) |

### Response Format

```json
{
  "answers": [
    {
      "score": 27.74823341616769,
      "id": 20,
      "answer": "Call us on 555 123 4567 to cancel a reservation.",
      "questions": [
        "How can I cancel a reservation?"
      ],
      "metadata": [
        {
          "name": "category",
          "value": "api"
        }
      ]
    }
  ]
}
```

### Response Fields

| Field | Description |
|---|---|
| `score` | Confidence score for this answer match |
| `id` | Unique ID of the Q&A pair in the knowledge base |
| `answer` | The answer text returned to the user |
| `questions` | The question(s) in the knowledge base that matched |
| `metadata` | Metadata tags associated with the Q&A pair |

---

## 7. Improving Performance: Active Learning & Synonyms

### 7.1 Active Learning

> **Active learning** = automatically suggests **alternate phrasings** for existing questions based on real user queries, helping the knowledge base handle more varied input over time.

- **Enabled by default**
- Goal: handle cases where users phrase the same question differently

#### How Active Learning Works (3 Steps)

| Step | Action |
|---|---|
| **1. Create Q&A pairs** | Add questions and answers in Language Studio (manually or by importing a file in bulk) |
| **2. Review suggestions** | Active learning suggests alternate phrasings for each question in the **Review suggestions pane** |
| **3. Accept or reject** | Select the checkmark to accept or delete icon to reject each suggestion; can bulk accept/reject all |

#### Manual Alternative: Add Alternate Questions
- In the **Edit knowledge base pane**, use **"Add alternate question"** to manually add additional phrasings for any Q&A pair

### 7.2 Synonyms

> **Synonyms** = let you define words that mean the same thing so the service finds the correct answer regardless of which term the user uses.

**Example:** A travel agency user might say "reservation" or "booking", define them as synonyms so both return the same answer.

#### Synonyms are defined via the REST API (JSON format):

```json
{
    "synonyms": [
        {
            "alterations": [
                "reservation",
                "booking"
            ]
        }
    ]
}
```

> Each `alterations` array = one synonym group. All words in the group are treated as equivalent.

---

## 8. Full Workflow

```
1. Provision Azure Language resource (with question answering enabled)
   + provision Azure AI Search resource
        ↓
2. In Language Studio: create Custom Question Answering project
        ↓
3. Add data sources (FAQ URLs / files / chit-chat)
        ↓
4. Edit & refine Q&A pairs
   → Add multi-turn follow-up prompts where needed
        ↓
5. Test interactively in Language Studio
   → Check confidence scores, review alternate answers
        ↓
6. Deploy → REST endpoint created
        ↓
7. Client application calls REST endpoint
   → Sends { "question": "..." }
   → Receives { "answers": [...] }
        ↓
8. Improve over time
   → Active learning: accept/reject suggested alternate questions
   → Synonyms: define equivalent terms via REST API
```

---

## 9. Component Reference Summary

| Component | What It Is | Key Role |
|---|---|---|
| **Question answering** | Azure Language capability | Matches user questions to static answers in a knowledge base |
| **Knowledge base** | Collection of Q&A pairs | The data store that answers are drawn from |
| **Language Studio** | Web UI (`language.azure.com`) | Create, manage, test, and deploy knowledge bases |
| **Azure AI Search** | Backend search index | Stores and retrieves knowledge base content |
| **Chit-chat** | Built-in conversational dataset | Adds small-talk capability to a knowledge base |
| **Multi-turn** | Follow-up prompt chains | Clarifies ambiguous questions before giving an answer |
| **REST endpoint** | Published deployment URL | How client apps query the knowledge base |
| **Active learning** | Automatic suggestion engine | Proposes alternate question phrasings based on real usage |
| **Synonyms** | Equivalent term definitions | Ensures consistent answers regardless of word choice |
| **QnA Maker** | Predecessor service | Older standalone version; migration guide available |
