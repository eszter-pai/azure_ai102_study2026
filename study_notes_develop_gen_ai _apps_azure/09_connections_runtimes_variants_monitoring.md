# Module: Get Started with Prompt Flow in Microsoft Foundry
## Session: Connections, Runtimes, Variants & Monitoring
**Sources:**
- [Explore connections and runtimes](https://learn.microsoft.com/en-us/training/modules/get-started-prompt-flow-ai-studio/4-connections-runtimes)
- [Explore variants and monitoring options](https://learn.microsoft.com/en-us/training/modules/get-started-prompt-flow-ai-studio/5-variants-monitor)

---

## 1. Connections

> A **connection** is a secure, configured link between **prompt flow** and an **external service, data source, or API**.

### 1.1 Why Connections Are Needed

- It is creaed to ensure prompt flow can securely call the deployed model (from Azure OpenAI)
- Flows often need to call external services (e.g., an **LLM, a search index**)
- To do this, the flow must be **authorized** (it needs credentials or API keys)
- Instead of exposing secrets, a connection **stores credentials securely**
- Secrets are kept in **Azure Key Vault** (never exposed to users directly)

**Two key roles of connections:**

| Role | What It Does |
|---|---|
| **API credential management** | **Automates and secures the handling** of sensitive access information (keys, tokens) |
| **Secure data transfer** | Enables safe data transfer **from various sources**, maintaining data integrity and privacy |

> Once a connection is set up, it can be **reused across multiple flows and tools**, no need to reconfigure each time.

---

### 1.2 Connection Types and Their Built-in Tools

> Certain built-in tools **require** a specific connection type to be configured before they can work.

| Connection Type | Compatible Built-in Tools |
|---|---|
| **Azure OpenAI** | LLM tool or Python tool |
| **OpenAI** | LLM tool or Python tool |
| **Azure AI Search** | **Vector DB Lookup** tool or Python tool |
| **Serp** | **Serp API tool** or Python tool |
| **Custom** | Python tool |

> The **Python tool** is compatible with every connection type, it **can use any external service through custom code**.

---

## 2. Runtimes

> A **runtime** provides the **compute and environment** needed to actually run a flow.

### 2.1 Two Components of a Runtime

```
[Runtime]
    ├── [Compute Instance]   ← provides CPU/GPU compute resources (processing power to execute the flow)
    └── [Environment]        ← specifies packages/libraries needed to run the flow
```
---

### 2.2 Default vs. Custom Environment

| Environment | When to Use |
|---|---|
| **Default environment** | Available out of the box: **use for quick development** and testing |
| **Custom environment** | Use when your flow **requires packages/libraries** not included in the default |

> A **runtime** gives you a **controlled, stable environment** where flows can be run and validate: ensuring everything works as expected before production.

---

## 3. Variants

> **Variants** are **different versions of a tool node** with distinct settings: to **compare and optimize node behavior**.

- Currently, variants are **only supported in the LLM tool**
- A variant can differ in:
  - **Prompt content** (**different wording** of the prompt)
  - **Connection settings** (e.g., different **model, temperature, max tokens**)

**Example use case:** Creating **multiple variants of a summarization node** to find **which prompt produces the best summary quality**.

---

### 3.1 Benefits of Using Variants

| Benefit | Description |
|---|---|
| **Enhance quality** | Create diverse variants to find the best prompt and settings for high-quality LLM output |
| **Save time and effort** | Easy management and comparison of prompt versions: simplifies **historical tracking and prompt tuning** |
| **Boost productivity** | Quicker creation and management of variations → better results in less time |
| **Facilitate easy comparison** | Side-by-side result comparisons — choose the **best variant based on data-driven decisions** |

---

## 4. Deploy a Flow to an Endpoint

> When you are satisfied with your flow's performance, **deploy it to an online endpoint** to **make it accessible from any application**.

**How it works:**

```
[Deploy flow to online endpoint]
         ↓
[Prompt flow generates a URL + key]
         ↓
[External app calls the endpoint URL (API call)]
         ↓
[Flow runs and returns output in real-time]
```

| Term | Meaning |
|---|---|
| **Online endpoint** | A URL that you call from any application to trigger the flow |
| **URL + key** | Generated automatically on deployment: used to securely integrate the flow |
| **Real-time response** | Calling the endpoint returns output almost immediately (online inference) |

> **Use cases:** Chat responses, agentic responses (any output you want to return in another application) .

---

## 5. Monitor Evaluation Metrics

> Monitoring tells you whether your deployed LLM application is actually meeting **real-world expectations**.

**Two approaches to monitoring:**

| Approach | How |
|---|---|
| **End-user feedback** | Collect feedback to assess whether the application is useful in practice |
| **Prediction vs. ground truth** | Compare LLM outputs against expected (correct) responses to gauge accuracy |

> Whenever the application **underperforms**, revert to **Experimentation** to iteratively improve the flow.

---

### 5.1 The 5 Evaluation Metrics

| Metric | What It Measures |
|---|---|
| **Groundedness** | Alignment of the output with the **input source or database** — is the **answer grounded in the data?** |
| **Relevance** | How **pertinent** the output is to the given input — **does it answer the actual question?** |
| **Coherence** | **Logical flow and readability** of the text — does it make sense as a whole? |
| **Fluency** | **Grammatical and linguistic accuracy** — is the language correct? |
| **Similarity** | **Contextual and semantic match** between the output and the **ground truth** response |

> These same 5 metrics appear in the **model catalog benchmarks** (note 04)


---

## 6. Quick Reference

### Connections Key Facts

| Fact | Detail |
|---|---|
| **Purpose** | Securely link **prompt flow to external services** |
| **Secret storage** | Credentials stored in **Azure Key Vault** |
| **Reusable** | One connection can be used across multiple flows/tools |
| **Python tool** | Compatible with ALL connection types |

### Runtime Key Facts

| Fact | Detail |
|---|---|
| **Purpose** | Provide **compute + environment** to run a flow |
| **Compute instance** | Provides processing power |
| **Environment** | Defines required packages/libraries |
| **Default environment** | Available out of the box for quick start |
| **Custom environment** | Needed when additional packages are required |

### Variants Key Facts

| Fact | Detail |
|---|---|
| **What they are** | Versions of a tool node with different settings |
| **Supported tool** | **LLM tool only** (currently) |
| **Can vary** | **Prompt content OR connection settings** (model, temperature, etc.) |
| **Main benefit** | **Compare** and optimize prompts/settings side-by-side |

### Evaluation Metrics — One-Line Definitions

| Metric | One-Line Definition |
|---|---|
| **Groundedness** | Output aligned with source/database |
| **Relevance** | Output pertinent to the input question |
| **Coherence** | Output reads logically and naturally |
| **Fluency** | Output is grammatically correct |
| **Similarity** | Output matches ground truth semantically |
