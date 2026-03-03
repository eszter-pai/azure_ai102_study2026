# Module: Plan and prepare to develop AI solution on Azure
## Session: What is AI + Foundry Tools 
**Sources:**
- [What is AI?](https://learn.microsoft.com/en-us/training/modules/prepare-azure-ai-development/2-what-is-ai)
- [Foundry Tools (Azure AI Services)](https://learn.microsoft.com/en-us/training/modules/prepare-azure-ai-development/3-azure-ai-services)

---

## 1. What is AI?

> **Definition:** AI (Artificial Intelligence) enables applications to exhibit human-like behavior. Modern AI solutions are built on **ML models** that learn semantic relationships found in huge quantities of data.

### AI allows app to:
- Interpret input in like text, image, speech
- Reason over that input
- Generate appropriate responses and predictions

---

### 1.1 Core AI Capabilities

| Capability | Description | Example Use Case |
|---|---|---|
| **Generative AI** | Generates original responses to natural language prompts | Auto-generate property descriptions for real estate listings |
| **Agents** | Generative AI apps that respond autonomously to input and take actions | "Executive assistant" agent that books a taxi |
| **Computer Vision** | Accepts, interprets, and processes visual input from images, videos, live cameras | Automated grocery checkout, identifies products without barcode scanning |
| **Speech** | Recognizes and synthesizes speech | Digital assistant responds to voice commands |
| **Natural Language Processing (NLP)** | analyze written or spoken text, extract key points, summarize, classify | Social media sentiment analysis |
| **Information Extraction** | Uses Computer Vision + Speech + NLP to extract key info from documents, images, audio | Automated expense processing, extract dates, line items, totals from receipts |
| **Decision Support** | Uses historic data and learned correlations to make predictions for business decisions | Predict real estate market trends from demographic/economic data |

---

### 1.2 Generative AI

**How it works:**
```
[Prompt] → [Language Model] → [Response]
```

**Types of Language Models:**

| Type | Description |
|---|---|
| **LLM (Large Language Model)** | Trained on huge volumes of data; contains many millions of parameters |
| **SLM (Small Language Model)** | Optimized for specific scenarios; lower overhead |

**Multi-modal models**
- Accept: text, image, or speech prompts
- Generate: text, code, speech, or images

**Common use cases for Generative AI:**
- Conversational apps and agents
- Research assistance
- Content creation
- Task automation

---

## 2. Azure AI Services (Foundry Tools)

> **Definition:** Foundry Tools are Microsoft Azure's set of **out-of-the-box prebuilt APIs and models** that you integrate into applications. They are the most obvious starting point for AI development on Azure.

---

### 2.1 Available Foundry Tools / Services

| Service | Core Capability | Key Features |
|---|---|---|
| **Azure OpenAI** | Generative AI access to OpenAI models | GPT family, DALL-E image generation; scalable & secure Azure cloud service |
| **Azure Vision** | Computer Vision | Detect objects, generate captions/descriptions/tags, read text in images (OCR: Optical character recognition) |
| **Azure Speech** | Speech processing | Text-to-speech, speech-to-text, speaker recognition, speech translation |
| **Azure Language** | Natural Language Processing | Entity extraction, sentiment analysis, summarization, conversational language models, Q&A solutions |
| **Microsoft Foundry Content Safety** | Content moderation | Algorithms to flag offensive, risky, or undesirable text and images |
| **Azure Translator** | Language translation | State-of-the-art models; translates text across large number of languages |
| **Azure AI Face** | Facial recognition | Detect, analyze, and recognize human faces  (⚠️ *restrict access*) |
| **Azure AI Custom Vision** | Custom computer vision | Train custom models for image classification and object detection |
| **Azure Document Intelligence** | Document data extraction | Pre-built or custom models; extract fields from invoices, receipts, forms |
| **Azure Content Understanding** | Multi-modal content analysis | Extract data from forms, images, videos, and audio streams |
| **Azure AI Search** | AI-powered search indexing | Creates vector indexes; commonly used to **ground prompts** for generative AI (RAG pattern) |

---

### 2.2 Resource Provisioning Options

When using Foundry Tools, you choose between two resource types:

#### Option A: Single Service Resources
- Provision only the specific services you need (e.g. just Azure Language)
- Many include a **free-tier SKU** for evaluation/development
- Each provides its own **endpoint + authorization keys API**
- Good for small/targeted solutions

#### Option B: Multi-Service Resources (Two Types)

| Resource Type | Included Services | Notes |
|---|---|---|
| **Foundry Tools** | Azure Speech, Azure Language, Azure Translator, Azure Vision, Azure AI Face, **Azure AI Custom Vision**, Azure Document Intelligence | **Single** endpoint for all listed services |
| **Microsoft Foundry** | **Azure OpenAI**, Azure Speech, Azure Language, **Microsoft Foundry Content Safety**, Azure Translator, Azure Vision, Azure AI Face, Azure Document Intelligence,**Azure Content Understanding** | Supports working through a **Microsoft Foundry project*** |

> \* Microsoft Foundry project enables: centralized access control, cost management, shared resources, and building next-gen generative AI apps/agents. preferred for medium to large scale development

---

### 2.3 Key Considerations When Planning

#### Regional Availability
- not all services and models are available in every Azure region
- Consider regional quota restrictions for your subscription
- Check: [Product Availability Table](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table)
- For Azure OpenAI model availability: check the model availability table in Azure OpenAI docs

#### Cost
- Foundry Tools are charged based on **usage**
- Different pricing schemes per service
- Use the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator) to estimate costs
- Reference: [Foundry Tools Pricing](https://azure.microsoft.com/pricing/details/cognitive-services)
- free tier exists on standalone resources: useful for development/test

#### Key terms
- foundry tools: prebuilt azure APIs, models
- endpoint: URL you call to acess a service from your app.
- API keys: authorization credentials generated per resource
- vector indexes: a serach index storing embedding used to ground GenAI prompt (Azure AI serach)
- grounding: feeding relevant data to a GenAI model to improve accuracy of responses
- Microsoft foundry project: centralize workspace for managing AI resources, access, and costs

---

### 2.4 Development Workflow Summary

```
1. Identify AI capabilities needed
        ↓
2. Choose appropriate Foundry Tools / services
        ↓
3. Provision resource(s) in Azure
   - Via Azure Portal, BICEP/ARM templates, or Azure CLI
        ↓
4. (Recommended for medium/large projects)
   → Provision within a Microsoft Foundry project
        ↓
5. Build client application
   - Use service-specific APIs and SDKs
```

---

## 3. Quick Reference

### Capability → Service Mapping

| If you need... | Use this service |
|---|---|
| Generate text/images from prompts | **Azure OpenAI** |
| Read text from images (OCR) / detect objects | **Azure Vision** |
| Convert speech ↔ text | **Azure Speech** |
| Analyze sentiment / extract entities from text | **Azure Language** |
| Translate between languages | **Azure Translator** |
| Moderate harmful content | **Microsoft Foundry Content Safety** |
| Detect/recognize faces | **Azure AI Face** |
| Train custom image classifier | **Azure AI Custom Vision** |
| Extract fields from invoices/receipts | **Azure Document Intelligence** |
| Analyze multi-modal content (docs, video, audio) | **Azure Content Understanding** |
| Build RAG / vector search for grounding LLMs | **Azure AI Search** |
