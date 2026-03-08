# Module: Choose and deploy models from the model catalog in Microsoft Foundry portal
## Session: Explore the Model Catalog
**Source:** [Explore the model catalog](https://learn.microsoft.com/en-us/training/modules/explore-models-azure-ai-studio/2-select-model)

---

## 1. What is the Model Catalog?

> The **model catalog** in Microsoft Foundry is a **central repository of models** you can browse to find the right language model for your generative AI use case.

- Can AI **solve** my use case?
- How do I **select** the best model for my use case?
- Can I **scale** for real-world workloads?

---

## 2. Can AI Solve My Use Case?

### 2.1 Where to Explore Models — Three Catalogs

| Catalog | Description |
|---|---|
| **Hugging Face** | Vast catalog of open-source models across various domains |
| **GitHub** | Access to diverse models via GitHub Marketplace and GitHub Copilot |
| **Microsoft Foundry** | Comprehensive catalog with robust deployment tools (**recommended** for **prototyping**) |

---

### 2.2 LLM vs. SLM

| Type | Examples | Best For |
|---|---|---|
| **LLM** (Large Language Model) | GPT-4, Mistral Large, Llama3 70B, Llama 405B, Command R+ | Deep reasoning, complex content generation, extensive context understanding |
| **SLM** (Small Language Model) | Phi3, Mistral OSS, Llama3 8B | Cost-effective, faster, lower-end hardware, edge devices; handles common NLP tasks |

---

### 2.3 Model Types by Modality and Task

| Model Type | Description | Examples |
|---|---|---|
| **Chat completion** | Generate coherent, contextually appropriate text responses | GPT-4, Mistral Large |
| **Reasoning** | Higher performance on math, coding, science, strategy, logistics | DeepSeek-R1, o1 |
| **Multi-modal** | Process images, audio, and other data types alongside text | GPT-4o, Phi3-vision |
| **Image generation** | Create realistic visuals from text prompts | DALL·E 3, Stability AI |
| **Embedding models** | Convert **text to numerical representations**; improve search by semantic meaning | Ada, Cohere |
| **Function calling / JSON support** | Interact with software tools dynamically; **automate API calls, DB queries** | (various) |

> **Embedding models** are commonly used in **RAG (Retrieval Augmented Generation)** scenarios to enhance search relevance and recommendation engines.

---

### 2.4 Regional and Domain-Specific Models

> Some models are designed for **specific languages, regions, or industries** and can outperform general-purpose models in their domain.

| Model | Specialization |
|---|---|
| **Core42 JAIS** | Arabic language LLM |
| **Mistral Large** | Strong focus on European languages: better multilingual accuracy |
| **Nixtla TimeGEN-1** | Time-series forecasting: ideal for financial predictions, supply chain, demand forecasting |

---

### 2.5 Open-Source vs. Proprietary Models

| Type | Best For | Examples | Notes |
|---|---|---|---|
| **Proprietary** | Cutting-edge performance, enterprise use | OpenAI GPT-4, Mistral Large, Cohere Command R+ | **Enterprise-level security**, support, high accuracy |
| **Open-source** | Flexibility, cost-efficiency, customization | Meta, Databricks, Snowflake, Nvidia models; Hugging Face catalog | More developer control; **fine-tuning**, local deployment possible |

**Enterprise guarantees when using either through Microsoft Foundry model catalog:**
- **Data and privacy**: you decide what happens with your data
- **Security and compliance**: built-in security
- **Responsible AI and content safety**: evaluations and content safety built in

---

## 3. How Do I Select the Best Model?

### 3.1 Four Key Criteria to Filter Models

| Criterion | Question to Ask |
|---|---|
| **Task type** | Text only? Or also audio, video, multiple modalities? |
| **Precision** | Is a base model good enough, or do I need a fine-tuned model? |
| **Openness** | Do I want to fine-tune the model myself? |
| **Deployment** | Local, serverless endpoint, or managed infrastructure? |

---

### 3.2 Base Model vs. Fine-Tuned Model

| Type | Description | When to Use |
|---|---|---|
| **Base model** | Pretrained on large dataset; handles a wide variety of tasks | General-purpose tasks; use prompt engineering to improve results |
| **Fine-tuned model** | Further trained on a smaller, task-specific dataset | When higher precision is needed for a specific domain or application |


---

### 3.3 Model Benchmarks — Performance Metrics

> Use **model benchmarks** in the Microsoft Foundry catalog to compare models during initial exploration. Note: benchmarks show general performance, not performance on your specific use case.

| Benchmark | What It Measures |
|---|---|
| **Accuracy** | Does generated text match the correct answer exactly? (1 = match, 0 = no match) |
| **Coherence** | Does the **output flow smoothly and read naturally** (human-like)? |
| **Fluency** | Does it follow **grammatical rules and use vocabulary correctly**? |
| **Groundedness** | Is **the generated answer aligned with the input data**? |
| **GPT Similarity** | Semantic similarity between **AI-generated output and a ground truth sentence** |
| **Quality index** | Aggregate comparative score between 0 and 1 (**higher = better**) |
| **Cost** | Price-per-token: useful for comparing **quality vs. cost** tradeoff |

---

### 3.4 Evaluation Approaches

| Approach | Description | When to Use |
|---|---|---|
| **Manual evaluation** | Rate the model's responses yourself | Early stage: quickly assess response quality |
| **Automated evaluation** | Uses ML metrics (precision, recall, F1 score) calculated against your own ground truth | Systematic, scalable, objective comparisons |

---

## 4. Can I Scale for Real-World Workloads?

> After building a prototype, you need to plan for scaling to production.

| Consideration | Question to Answer |
|---|---|
| **Model deployment** | Where to deploy for best balance of performance and cost? |
| **Model monitoring & optimization** | How to monitor, evaluate, and optimize model performance over time? |
| **Prompt management** | How to orchestrate and optimize prompts for accuracy and relevance? |
| **Model lifecycle** | How to m**anage model, data, and code updates** ( **GenAIOps** ) lifecycle? |

> **GenAIOps** = Generative AI Operations: the **ongoing lifecycle management of gen AI solutions** (model updates, data updates, code updates).

Microsoft Foundry provides both **visual** and **code-first tools** to help build and maintain a scalable generative AI solution.

---

## 5. Quick Reference

### Model Selection Decision Flow

```
What do you need?
    │
    ├── Text responses / chat?          → Chat completion model (GPT-4, Mistral Large)
    ├── Math / coding / reasoning?      → Reasoning model (DeepSeek-R1, o1)
    ├── Images + text?                  → Multi-modal model (GPT-4o, Phi3-vision)
    ├── Generate images?                → Image generation (DALL·E 3, Stability AI)
    ├── Semantic search / RAG?          → Embedding model (Ada, Cohere)
    ├── Specific language/region?       → Domain-specific model (JAIS, Mistral Large)
    └── Automate APIs / structured data?→ Function calling / JSON support
```

### Exam Tip

| Concept | Key Point |
|---|---|
| **LLM vs SLM** | LLM = powerful, expensive; SLM = fast, cheap, edge-friendly |
| **RAG** | Uses **embedding models to ground LLM** responses in your own data |
| **Fine-tuning** | Extra training on domain-specific data to improve precision |
| **Benchmarks** | Compare models at catalog level; don't reflect your specific use case |
| **GenAIOps** | Lifecycle management of generative AI solutions (like DevOps for gen AI) |
| **Proprietary vs Open-source** | Proprietary = enterprise-ready; Open = flexible, customizable |
| **Microsoft Foundry catalog** | Best place to **explore + deploy**; **enforces data privacy, security, responsible AI** |
