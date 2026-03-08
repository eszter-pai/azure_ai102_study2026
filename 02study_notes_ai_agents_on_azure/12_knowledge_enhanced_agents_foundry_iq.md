# Module: Build Knowledge-Enhanced AI Agents with Foundry IQ
## Session: RAG Fundamentals + Foundry IQ + Data Sources + Retrieval Configuration

**Sources:**
- [Understanding RAG for Agents](https://learn.microsoft.com/en-us/training/modules/introduction-foundry-iq/2-understand-rag)
- [Explore Foundry IQ](https://learn.microsoft.com/en-us/training/modules/introduction-foundry-iq/3-foundry-iq)
- [Configure Data Sources for Knowledge Bases](https://learn.microsoft.com/en-us/training/modules/introduction-foundry-iq/4-data-requirements)
- [Configure Retrieval with Foundry IQ](https://learn.microsoft.com/en-us/training/modules/introduction-foundry-iq/5-configure-retrieval)

---

## 1. Why Simple Agents Fail in Enterprise Environments

> Simple AI agents face **5 fundamental limitations** that make them unreliable for enterprise use.

| Limitation | Impact | Example |
|---|---|---|
| **Knowledge cutoff dates** | No access to recent information | Can't help with newly released features or updated policies |
| **No private data access** | Generic responses only | Missing company procedures, support knowledge, product specs |
| **Lack of context** | Irrelevant advice | Ignores specific security requirements or approval workflows |
| **Fabricated responses** | **Compliance and security risks** | Confident-sounding but incorrect information (**hallucination**) |
| **Scalability issues** | Duplicated engineering effort | Every team rebuilds the same RAG infrastructure |

---

## 2. Retrieval Augmented Generation

> **RAG** = an architectural approach that transforms agents by **connecting them to organizational knowledge sources in real-time**, moving from static training data to dynamic knowledge retrieval.

### Critical Advantages of RAG for Enterprise

| Advantage | Description |
|---|---|
| **Real-time updates** | Keeps agents current with policies and procedures **without requiring retraining** |
| **Source transparency** | Shows users **exactly which documents** informed each response: builds trust, enables verification |
| **Factual grounding** | Anchors responses in actual organizational content, **eliminates fabricated information** and ensures compliance |

---

## 3. What Is Foundry IQ?

> **Foundry IQ** = a **managed knowledge platform for AI agents**, built on **Azure AI Search**. It provides RAG capabilities as a **shared service** that multiple agents can use, eliminating the need to build custom RAG infrastructure for each agent.

**Key shift:** From building infrastructure → to designing agent experiences.

### The Traditional RAG Problem (Without Foundry IQ)

```
3 agents needed → 3 separate RAG systems to build and maintain
```

### The Foundry IQ Solution

```
3 agents needed → Create knowledge bases ONCE → Connect any agent to them
```

### How Foundry IQ Organizes Information

> Knowledge bases organize information by **business domain**, not by technical storage location.

- Instead of searching "SharePoint Site A" or "Blob Container B"...
- Agents search **"Product Documentation"** or **"HR Policies"**
- Related data from multiple storage locations appears as **one unified knowledge source**

**Example: Product Documentation knowledge base might contain:**
- Technical specifications from SharePoint
- **API documentation** from Azure Blob Storage
- Usage analytics from OneLake
- Support tickets from an existing search index

### What Happens When You Add a Data Source (4 Steps)

| Step | Action |
|---|---|
| **1. Discovery** | Foundry IQ scans your storage location for documents |
| **2. Processing** | Documents are **chunked and embedded** for semantic search |
| **3. Indexing** | Content becomes searchable through the knowledge base |
| **4. Monitoring** | Changes to documents **trigger automatic reindexing** |

### Built-in Retrieval Intelligence (Automatic)

When an agent queries a knowledge base, Foundry IQ automatically:
- **Analyzes the question** to understand what information is needed
- **Selects retrieval strategies** based on the query type (**keyword vs. semantic + query expansion**)
- **Ranks results** using relevance scoring, most contextually appropriate surfaces first
- **Provides citations** so agents can reference source documents

> All this runs **without custom code**.

### Connecting an Agent to a Knowledge Base (Code)

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool

project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)

# Connect to the knowledge base via MCP
knowledge_tool = MCPTool(
    server_label="product-docs",
    server_url=f"{search_endpoint}/knowledgebases/product-documentation/mcp"
)

# Create agent with knowledge access
agent = project_client.agents.create_version(
    agent_name="product-support-agent",
    definition=PromptAgentDefinition(
        model="gpt-4o-mini",
        instructions="Answer product questions using the knowledge base. Always cite your sources.",
        tools=[knowledge_tool]
    )
)
```

> **Key:** Foundry IQ uses **MCP (Model Context Protocol)** to connect agents to knowledge bases, a standardized, secure interface.

### Shared Knowledge Advantage

| Scenario | Traditional RAG | Foundry IQ |
|---|---|---|
| 3 agents, 2 shared knowledge bases | 3 separate retrieval systems | 1 shared knowledge platform |
| Update product docs | Update all 3 systems | Update once → all agents benefit immediately |
| Add a new agent | Build new RAG system | Connect to existing knowledge bases |

---

## 4. Data Sources for Knowledge Bases

> Foundry IQ supports **6 data source types**. Choosing the right one depends on where your data lives and how you need to access it.

### 6 Supported Data Sources

| Data Source | Access Type | Best For |
|---|---|---|
| **Azure AI Search Index** | Indexed | Enterprise search with custom pipelines; existing Azure AI Search investment |
| **Azure Blob Storage** | Direct | Document files in Azure Storage (PDF, DOCX, TXT, MD, HTML) |
| **Web (Bing)** | Real-time | Current, public information; recent events, pricing, changing info |
| **SharePoint (Remote)** | Real-time | Live SharePoint content with Microsoft 365 governance; always current |
| **SharePoint (Indexed)** | Indexed | Advanced search on SharePoint with **custom pipelines**; faster responses |
| **OneLake** | Direct | **Unstructured** data in Microsoft Fabric; business intelligence, analytics |

### Data Source Deep Dives

#### Azure AI Search Index
- Best when you already **invested in Azure AI Search** and have existing indexes
- Supports: **semantic ranking, custom scoring, faceted navigation, multi-language**
- Can aggregate data from multiple origins already processed and indexed

#### Azure Blob Storage
- Direct path from files to knowledge base: **no index to build or maintain**
- Supported file types: PDF, `.docx`, `.txt`, `.md`, `.html`
- Organize blobs into containers by topic or access level for governance

#### Web (Bing)
- Grounds agent with **real-time internet content**
- Use for: recent events, current pricing/availability, frequently changing information
- **Warning:** Less control over sources: **not ideal when accuracy and source verification are critical**
- Can be combined with internal sources as a **supplementary fallback**

#### SharePoint: Remote vs. Indexed

| Feature | Remote | Indexed |
|---|---|---|
| **Access method** | Real-time queries | Preprocessed index |
| **Response time** | Depends on SharePoint | Faster |
| **Maintenance** | No index to maintain | Requires index updates |
| **Advanced search** | Limited | **Full Azure AI Search** capabilities |
| **Data freshness** | Always current | Depends on indexing schedule |
| **Permission handling** | Respects SharePoint permissions automatically | Configured during indexing |

- **Use Remote when:** Simple setup, always-current data, no advanced search needed
- **Use Indexed when:** Advanced search, custom analyzers, AI enrichment pipelines, combining with other sources

#### OneLake (Microsoft Fabric)
- Access to unstructured data in your **Microsoft Fabric data lakehouse**
- Use cases: business intelligence reports, data documentation, analytical findings, research outputs

### Data Source Decision Guide

| If your data is... | And you need... | Choose... |
|---|---|---|
| In SharePoint | Simple setup, always current | **SharePoint Remote** |
| In SharePoint | Advanced search, custom pipelines | **SharePoint Indexed** |
| Files in Azure | Direct file access | **Azure Blob Storage** |
| In Microsoft Fabric | Data lakehouse content | **OneLake** |
| Already indexed in Azure AI Search | Existing investment | **Azure AI Search Index** |
| Public, current information | Real-time web content | **Web (Bing)** |

> You can **combine multiple sources** in a single knowledge base (e.g., SharePoint as primary + Web as supplementary fallback).

---

## 5. Configuring Retrieval Behavior

> Having great indexed content is not enough. Agents must be **explicitly instructed** on when and how to use knowledge bases, otherwise behavior is inconsistent.

### The 3 Retrieval Behaviors (Only One is Acceptable)

| Behavior | Example Response | Problem |
|---|---|---|
| **Answers from training data** | "Most companies offer 2-3 weeks vacation" | not your actual policy |
| **Searches but doesn't cite** | "You get 15 days PTO" | Correct but unverifiable, no accountability |
| **Searches, cites, and grounds** | "You receive 15 days PTO【doc_id:1†Employee Handbook 2024】" | **This is the only acceptable behavior** |

### Writing Effective Retrieval Instructions

Effective instructions must specify **3 critical behaviors**:

1. **When to retrieve**: always use the knowledge base; never rely on training data
2. **How to cite**: specify the exact format for source attribution
3. **What to do when unsure**: define fallback behavior when information is not found

**Example of a BAD instruction (too vague):**
```python
instructions="Answer HR questions using the knowledge base."
# Problem: doesn't say WHEN to use it or HOW to present results
```

**Example of a GOOD instruction:**
```python
retrieval_instructions = """You are a helpful HR assistant.

CRITICAL RULES:
- You must ALWAYS search the knowledge base before answering any question
- You must NEVER answer from your own knowledge or training data
- Every answer must include citations in this format: 【doc_id:search_id†source_name】
- If the knowledge base doesn't contain the answer, respond with:
  "I don't have that information in our current documentation. Please contact HR directly."

Your role is to provide accurate, verifiable information from company documentation."""
```

### 4 Query Types to Test

| Query Type | Example | Expected Behavior |
|---|---|---|
| **Straightforward factual** | "What is our vacation policy?" | Direct retrieval with citations |
| **Requires synthesis** | "What are the differences between our leave types?" | Multiple docs retrieved; synthesized answer with multiple citations |
| **Outside knowledge base** | "What's the weather like today?" | **Graceful fallback**: "I don't have that information..." |
| **Ambiguous** | "What about benefits?" | **Clarifying question** or focused search on most relevant topic |

### 4 Characteristics of a Good Response

| Characteristic | Description |
|---|---|
| **Grounding** | Information comes from the knowledge base, **not training data** |
| **Citation** | Every factual claim includes **source references** |
| **Relevance** | Retrieved content **actually answers the question** |
| **Completeness** | All necessary information provided, not just fragments |

### Retrieval Strategies by Agent Type

| Agent Type | Key Instruction Pattern |
|---|---|
| **Customer-facing support** | Always cite; if not in docs, escalate **("Let me connect you with a specialist"); never guess** |
| **Internal research assistant** | Synthesize across multiple sources; **cite all; indicate confidence level**; suggest related topics |
| **Domain expert (e.g., compliance)** | Only answer in-scope questions; cite specific document + section; refer interpretation questions to humans; note policy effective dates |

### Production Monitoring

| Metric | Why It Matters |
|---|---|
| **Citation frequency** | Are agents consistently citing sources? |
| **Fallback frequency** | How often do agents say "I don't know"? |
| **Query types** | What categories of questions appear most? |
| **Retrieval accuracy** | Do retrieved documents actually contain the answers? |

> Retrieval quality improves through **iteration based on real-world usage**: test → deploy → monitor → refine instructions and knowledge base content.
