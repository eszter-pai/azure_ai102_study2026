# Module: Build a Copilot with Microsoft Foundry
## Session: Groundedness + RAG (Retrieval Augmented Generation)
**Sources:**
- [Introduction](https://learn.microsoft.com/en-us/training/modules/build-copilot-ai-studio/1-introduction)
- [Understand how to ground your language model](https://learn.microsoft.com/en-us/training/modules/build-copilot-ai-studio/2-ground-language-model)

---

## 1. What Is Groundedness?

> **Groundedness** refers to whether a language model's response is **rooted in factual, relevant information** (not just text it learned during training.)

- A language model trained on general internet text can produce **grammatically correct but factually wrong** answers
- These inaccurate responses are sometimes called **"hallucinations"** (invented information presented as fact)
- To prevent this, you must **ground** the model in a specific, relevant data source

---

## 2. Ungrounded vs. Grounded Responses

| | **Ungrounded** | **Grounded** |
|---|---|---|
| **Information source** | Model's training data only (general internet text) | A specific, relevant data source you provide |
| **Response quality** | Grammatically coherent but **may be inaccurate** | Contextualized, **factually accurate** |
| **Risk** | May include **invented details** (e.g., fictional products) | Based on real data from your data source |
| **Example** | "Which product should I use for X?" → model invents a product | "Which product should I use for X?" → model answers from your actual product catalog |

---

### 2.1 Ungrounded Flow

```
[User prompt]
      ↓
[Language model uses only training data]
      ↓
[Response: coherent but uncontextualized — may be wrong]
```

### 2.2 Grounded Flow

```
[User prompt]
      ↓
[Retrieve relevant data from a data source]
      ↓
[Prompt + grounding data sent to language model]
      ↓
[Response: contextualized, accurate, based on real data]
```

---

## 3. RAG (Retrieval Augmented Generation)

> **RAG** is the standard technique used to ground a language model. It retrieves relevant information from a data source and adds it to the prompt **before** the model generates a response.

### 3.1 The 3-Step RAG Pattern

| Step | Name | What Happens |
|---|---|---|
| **1** | **Retrieve** | Fetch grounding data from the data source that is relevant to the user's prompt |
| **2** | **Augment** | Add the retrieved grounding data **to the prompt** |
| **3** | **Generate** | Send the augmented prompt to the language model → model produces a grounded response |

```
[User prompt]
      ↓
[1. RETRIEVE: search data source for relevant context]
      ↓
[2. AUGMENT: combine user prompt + retrieved context]
      ↓
[3. GENERATE: language model creates a grounded response]
      ↓
[Accurate, contextualized answer returned to user]
```

---

### 3.2 Why RAG?

- Allows the model to access knowledge it was **not trained on**:
  - Your company's **internal** documents
  - **Up-to-date** product catalogs
  - **Domain-specific** knowledge bases
  - Data more **recent** than the model's training cutoff

---

## 4. Adding Grounding Data in Microsoft Foundry

> Microsoft Foundry supports several **data connections** you can use to bring your own data into a project for grounding.

### 4.1 Supported Data Sources

| Data Source | Description |
|---|---|
| **Azure Blob Storage** | Store and access **unstructured** data (**files, documents**) in Azure |
| **Azure Data Lake Storage Gen2** | Scalable storage for **large-scale analytics data** |
| **Microsoft OneLake** | **Unified data lake** across Microsoft Fabric |
| **Upload files/folders** | Directly upload files to the project's storage in the Foundry portal |

> You connect these data sources to your AI Foundry project using the **Add Data** feature in the portal.

---

### 4.2 What You Build With This

> The goal is to build a **custom agent** (a chat-based AI application) that uses your own data to ground its responses.

- The agent gives users an **intuitive chat interface** to interact with
- Behind the scenes, RAG retrieves relevant data from your connected source before each response
- Result: users get **accurate, domain-specific answers**





