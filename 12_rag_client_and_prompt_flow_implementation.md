# Module: Build a Copilot with Microsoft Foundry
## Session: RAG Client Application + Implementing RAG in Prompt Flow
**Sources:**
- [Create a RAG-based client application](https://learn.microsoft.com/en-us/training/modules/build-copilot-ai-studio/3b-openai-client)
- [Implement RAG in a prompt flow](https://learn.microsoft.com/en-us/training/modules/build-copilot-ai-studio/4-build-copilot)

---

## 1. Two Ways to Implement RAG

> Once you have an Azure AI Search index (note 11), you can implement the RAG pattern in two different ways.

| Approach | How | When to Use |
|---|---|---|
| **RAG via SDK** (OpenAI client) | Extend a standard **chat completion** request with index connection details using `extra_body` | Code-first approach; direct SDK usage |
| **RAG via Prompt Flow** | Add an **Index Lookup tool node** to a prompt flow that retrieves context before generating a response | Visual / flow-based approach; multi-step orchestration |

---

## 2. RAG-Based Client Application (SDK Approach)

> You can implement RAG directly in code using the **Azure OpenAI SDK** by **attaching your Azure AI Search index** to the chat completion request.

### 2.1 How It Works

- Create an `AzureOpenAI` client as normal
- Build a prompt with system + user messages
- Define `rag_params`, a **dictionary** specifying the Azure AI Search index as a **data source**
- Pass `rag_params` via the `extra_body` parameter of `chat.completions.create()`
- The model automatically retrieves relevant context from the index and generates a grounded response

---

### 2.2 Keyword-Based RAG Query

> Default approach: the user prompt text is matched against the index as a **keyword search**.

```python
from openai import AzureOpenAI

# Connect to Azure OpenAI
chat_client = AzureOpenAI(
    api_version = "2024-12-01-preview",
    azure_endpoint = open_ai_endpoint,
    api_key = open_ai_key
)

# Build the prompt
prompt = [
    {"role": "system", "content": "You are a helpful AI assistant."}
]
input_text = input("Enter a question: ")
prompt.append({"role": "user", "content": input_text})

# Define RAG parameters — link to Azure AI Search index
rag_params = {
    "data_sources": [
        {
            "type": "azure_search",
            "parameters": {
                "endpoint": search_url,
                "index_name": "index_name",
                "authentication": {
                    "type": "api_key",
                    "key": search_key,
                }
            }
        }
    ],
}

# Submit prompt WITH index info attached via extra_body
response = chat_client.chat.completions.create(
    model="<model_deployment_name>",
    messages=prompt,
    extra_body=rag_params          # ← this is what enables RAG
)

# Print the grounded response
print(response.choices[0].message.content)
```

---

### 2.3 Vector-Based RAG Query

> Alternative: use **vector search** by specifying a `query_type` and an embedding model in `rag_params`. This enables **semantic similarity matching**, not just keyword matching.

```python
rag_params = {
    "data_sources": [
        {
            "type": "azure_search",
            "parameters": {
                "endpoint": search_url,
                "index_name": "index_name",
                "authentication": {
                    "type": "api_key",
                    "key": search_key,
                },
                # Additional params for vector-based query
                "query_type": "vector",
                "embedding_dependency": {
                    "type": "deployment_name",
                    "deployment_name": "<embedding_model_deployment_name>",
                },
            }
        }
    ],
}
```

### 2.4 Keyword vs. Vector Query Comparison

| | **Keyword Query** (default) | **Vector Query** |
|---|---|---|
| **How it searches** | Matches the **user's text against words** in the index | Converts text to vectors; matches by **semantic similarity** |
| **Configuration** | Just `endpoint`, `index_name`, `authentication` | Also needs `query_type: "vector"` + `embedding_dependency` |
| **Match type** | Exact or near-exact text matches | Semantic meaning, finds related content even with different words |
| **Requires** | A standard text index | A vector-enabled index + an embedding model deployment |

---

## 3. RAG in Prompt Flow

> **Prompt Flow** is a development framework for defining flows that **orchestrate interactions with an LLM**. It is the visual/flow-based way to implement RAG.

### 3.1 Prompt Flow Structure (Recap)

```
[Inputs]   ← user question + chat history
     ↓
[Tools]    ← series of connected nodes, each performing an operation
     ↓
[Outputs]  ← generated LLM response
```

**4 types of tools you can include in a prompt flow:**

| Tool Type | What It Does |
|---|---|
| **Python code** | Run custom Python scripts for data transformation or parsing |
| **Index Lookup** | Query a search index to retrieve relevant documents |
| **Prompt variants** | Define multiple versions of a prompt to compare and evaluate |
| **LLM submission** | Submit a prompt to a language model to generate a response |

---

### 3.2 The Key Tool for RAG: Index Lookup

> The **Index Lookup tool** is the core of RAG in a prompt flow. It **queries your Azure AI Search index and retrieves relevant context**, which is then passed to subsequent tools to augment the prompt.

```
[User question]
       ↓
[Index Lookup tool] → queries Azure AI Search → retrieves relevant documents
       ↓
[Retrieved context used to augment the prompt]
       ↓
[LLM node generates grounded response]
```

---

### 3.3 Sample: "Multi-round Q&A on Your Data"

> Prompt Flow provides a built-in sample you can clone: **"Multi-round Q&A on your data"**, a ready-to-use RAG chat flow.



---

### 3.4 Step-by-Step Details

#### Step 1 — Modify Query With History
- An **LLM node** **rewrites the user's question to include all relevant context** from prior conversation turns
- Produces a **more succinct, self-contained input** for the rest of the flow
- This is important for **multi-turn conversations** where the user's latest message may be ambiguous without context

#### Step 2 — Look Up Relevant Information
- The **Index Lookup tool** queries **the Azure AI Search index**
- Returns **the top-N most relevant documents** from your data source

#### Step 3 — Generate Prompt Context
- A **Python node** iterates over the retrieved documents
- Combines their **contents and sources** into **a single document string**
- This string is used as the grounding context in the next step

#### Step 4 — Define Prompt Variants
- **Prompt variants** allow you to test different system messages
- Goal: **find which system message** wording produces the most **grounded and factual** responses
- Example: one variant instructs the model to "use only the provided context" — another is more flexible

#### Step 5 — Chat With Context
- An **LLM node** receives the augmented prompt (question + retrieved context + system message)
- Generates a **natural language, grounded response**
- This response is also the **final output** of the entire flow

---

### 3.5 After Building the Flow

> Once the flow is **configured and tested**, you can **deploy it to an endpoint** and integrate it with any application to offer users an agentic chat experience.

---

## 4. Quick Reference

### Two RAG Implementation Approaches

| | **SDK approach** | **Prompt Flow approach** |
|---|---|---|
| **Tool** | `AzureOpenAI` client + `extra_body` | Index Lookup tool in a flow |
| **Style** | Code-first | Visual / orchestrated |
| **Key parameter** | `extra_body=rag_params` with `data_sources` | **Index Lookup tool** node |
| **Query types** | Keyword (default) or Vector | Configured in the Index Lookup tool |

### "Multi-round Q&A on Your Data" — 5-Step Flow

| Step | Tool | Purpose |
|---|---|---|
| 1 | LLM node | Rewrite question with chat history context |
| 2 | Index Lookup | Retrieve relevant docs from Azure AI Search |
| 3 | Python node | **Parse and combine retrieved docs into a string** |
| 4 | Prompt variants | Test different system messages for groundedness |
| 5 | LLM node | Generate final grounded response |

### Exam Tips

| Concept | Key Point |
|---|---|
| **RAG via SDK** | Use `extra_body=rag_params` with `data_sources` specifying the Azure AI Search index |
| **Keyword query** | Default in SDK RAG — text matched directly to index content |
| **Vector query** | Add `query_type: "vector"` + `embedding_dependency` with an embedding model deployment name |
| **Prompt Flow** | Development framework for orchestrating LLM interactions via connected tool nodes |
| **Index Lookup tool** | The key RAG tool in Prompt Flow — queries Azure AI Search to retrieve context |
| **Python node in RAG flow** | Parses top-N retrieved docs → combines into a single document string for the prompt |
| **Prompt variants in RAG** | Used to test different system messages → find which produces most grounded responses |
| **"Multi-round Q&A" sample** | 5-node RAG chat flow: history rewrite → index lookup → context generation → variants → LLM |
| **Step 1 purpose** | **Rewriting the question with history makes multi-turn conversations work correctly** |
| **Deploy flow** | After testing, deploy to an endpoint → integrate with any application |
