# Module: Build a Copilot with Microsoft Foundry
## Session: Make Your Data Searchable — Azure AI Search, Indexes & Vector Search
**Source:**
- [Make your data searchable](https://learn.microsoft.com/en-us/training/modules/build-copilot-ai-studio/3-search-data)

---

## 1. Why Search Matters for RAG

> To build a grounded agent (from note 10), you need to **efficiently search your data** to retrieve the relevant context. Azure AI Search is the tool that does this retrieval step in the RAG pattern.

- **Azure AI Search** acts as the **retriever** in a prompt flow application
- It allows you to: **bring your own data → index it → query the index** to retrieve relevant context
- The retrieved context is then passed to the language model (the Augment step in RAG)

```
[User prompt]
      ↓
[Azure AI Search queries the index → retrieves relevant context]    ← "Retrieve" step of RAG
      ↓
[Context + prompt sent to language model]
      ↓
[Grounded response returned to user]
```

---

## 2. What Is a Search Index?

> A **search index** describes **how your content is organized** to make it **searchable**.

**Analogy:** Think of a **library catalog**:
- The catalog contains metadata about each book: makes any book easy to find
- A search index does the same for your data documents

| Concept | Library Analogy | Search Index Equivalent |
|---|---|---|
| Data | Books in the library | Your documents/files |
| Index | Library catalog | Search index in Azure AI Search |
| Query | "Find books about X" | User prompt / search query |
| Result | Retrieved book | Relevant document/passage |

> The **index asset** is stored in **Azure AI Search** and **queried by Microsoft Foundry** when used in a chat flow.

---

## 3. Text Index vs. Vector Index



| | **Text-based Index** | **Vector-based Index** |
|---|---|---|
| **How it stores data** | Raw text | Mathematical vectors (embeddings) |
| **What it matches** | Exact or near-exact keywords | **Semantic meaning** — even with different words |
| **Search quality** | Good | **Better** — understands meaning, not just words |
| **Requires** | Just the text | An **embedding model** to generate embeddings |
| **Best for** | Simple keyword lookups | Language model applications (RAG) |

---

## 4. Embeddings

> An **embedding** is a format for representing data, a **vector of floating-point numbers** that allows a search engine to find semantically related information.

### 4.1 Why Embeddings Work

- Words and sentences that are **semantically related** will have **vectors that are close to each other** in multidimensional space
- Even if **different words** are used, embeddings capture the **meaning**

**Example:**
- Document A: *"The children played joyfully in the park."*
- Document B: *"Kids happily ran around the playground."*

These sentences use **different words** but have **similar meaning**. Embeddings represent both as vectors that are mathematically close to each other, so a search for "children playing outside" would retrieve both.

---

### 4.2 Cosine Similarity

> **Cosine similarity** is the mathematical method used to measure how semantically similar two pieces of text are.

- It measures the **cosine of the angle** between two vectors in multidimensional space
- **Small angle → vectors are close → high similarity**
- **Large angle → vectors are far apart → low similarity**

---

### 4.3 How to Create Embeddings for a Search Index

- Use an **Azure OpenAI embedding model** available in Microsoft Foundry
- When creating your index in the Foundry portal, you are guided to configure it with an embedding model
- The index then contains vector representations of your data, ready for vector search

---

## 5. The 4 Search Types

> Once you have **a search index, you can query it** using different search techniques.

| Search Type | How It Works | Strengths |
|---|---|---|
| **Keyword search** | Finds documents that contain the **exact keywords** from the query | Precise, great **when exact wording matters** |
| **Semantic search** | Understands the **meaning** of the query; matches semantically related content (not just exact words) | Better than keyword for natural language queries |
| **Vector search** | Uses **mathematical vector representations** (embeddings) to find documents with similar semantic meaning or context | Most advanced, captures meaning across different words/languages/formats |
| **Hybrid search** | **Combines keyword + vector search** (+ optional semantic ranking); queries run in parallel and results are merged | **Most accurate for generative AI apps**, precise when exact match available, still relevant when only conceptual match exists |

> **For generative AI applications: use Hybrid search** — it gives the most accurate results.

---

### 5.1 Search Type Decision Guide

```
Need exact keyword matches only?
    → Keyword search

Need to match meaning, not just exact words?
    → Semantic search

Need to search across different languages or formats using meaning?
    → Vector search

Building a generative AI / RAG application? (recommended)
    → Hybrid search (keyword + vector + optional semantic ranking)
```

---

## 6. Creating an Index in Microsoft Foundry

**The workflow:**

```
1. Add your data to Microsoft Foundry (Blob Storage, Data Lake, OneLake, or file upload)
         ↓
2. Use Azure AI Search integration in the Foundry portal
         ↓
3. Select an embedding model (Azure OpenAI embedding model)
         ↓
4. Index is created and stored in Azure AI Search
         ↓
5. Index is queried by Foundry during chat flow execution
```

> Microsoft Foundry guides you through configuring an index that is **most suitable for use with a language model**, you don't need to configure it manually from scratch.

---

## 7. Quick Reference

### Exam Tips

| Concept | Key Point |
|---|---|
| **Azure AI Search role** | The **retriever** in a RAG/prompt flow application |
| **Search index** | Organizes data so it can be queried — stored in Azure AI Search |
| **Embedding** | Vector of floating-point numbers representing semantic meaning |
| **Cosine similarity** | Measures semantic similarity between two vectors (embeddings) |
| **Embedding model** | Required to create a vector index — use Azure OpenAI embedding model in Foundry |
| **Vector index** | Better than text index for language model applications — captures meaning, not just keywords |
| **Hybrid search** | **Best for generative AI apps** — combines keyword + vector; precise + semantically relevant |
| **Where index is stored** | In **Azure AI Search**; queried by Foundry during the chat flow |
| **Creating an index** | Done in the Foundry portal; guided wizard selects the right settings for LLMs |
| **Supported data sources** | Azure Blob Storage, Azure Data Lake Gen2, OneLake, file upload (see note 10) |
