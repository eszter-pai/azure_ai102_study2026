# Module: Get Started with AI Agent Development on Azure
## Session: Agent Development Options + Microsoft Foundry Agent Service
**Sources:**
- [Options for agent development](https://learn.microsoft.com/en-us/training/modules/ai-agent-fundamentals/3-agent-development)
- [Microsoft Foundry Agent Service](https://learn.microsoft.com/en-us/training/modules/ai-agent-fundamentals/4-azure-ai-agent-service)

---

## 1. Traditional AI Frameworks vs. AI Agent Frameworks

> Understanding the difference helps you choose the right tool for your scenario.

| | **Traditional AI Frameworks** | **AI Agent Frameworks** |
|---|---|---|
| **What they do** | Add intelligent capabilities to existing applications | Enable **autonomous, goal-oriented** agents that reason, act, and learn |
| **Behavior** | Respond to inputs | **Proactively reason** and take action independently |
| **Examples** | Netflix recommendations, AI chatbots, Siri/Google Assistant | Expense agent, travel booking agent, multi-step workflow automation |

### Traditional AI Framework Capabilities

| Capability | Description | Example |
|---|---|---|
| **Personalization** | Analyzes user behavior → tailored recommendations | Netflix suggests shows based on viewing history |
| **Automation & efficiency** | Automates repetitive tasks, streamlines workflows | AI chatbots handle common customer service inquiries |
| **Enhanced user experience** | NLP, voice recognition, predictive text | Siri and Google Assistant understand voice commands |

### AI Agent Framework Extra Capabilities

| Capability | Description |
|---|---|
| **Agent collaboration & coordination** | **Multiple agents communicate**, share info, and work together to solve complex problems |
| **Task automation & management** | Automates multi-step workflows; **dynamic task delegation** across agents |
| **Contextual understanding & adaptation** | Agents perceive context, make decisions from **real-time data**, adapt to changing conditions |

---

## 2. Agent Development Solutions Overview

> Microsoft offers a **spectrum of tools**, from no-code for business users to full-featured SDKs for professional developers. Choose based on your **skill level** and **use case**.

| Solution | Target User | Key Characteristics |
|---|---|---|
| **Copilot Studio lite (M365 Copilot Chat)** | Business users with no coding experience | Declarative agent creation; describe what you need or use visual interface; no code required |
| **Copilot Studio (full version)** | Business users with low-code/Power Platform skills | Low-code tools + business domain knowledge; extends M365 Copilot; adds agent functionality to Teams, Slack, Messenger |
| **Microsoft 365 Agents SDK** | Professional developers: extending M365 Copilot | Full developer flexibility; targets M365 channels but can also deliver to Slack, Messenger |
| **Foundry Agent Service** | Professional developers: Azure-based AI solutions | Integrates with Azure AI services; supports multiple models, storage, and search; scalable enterprise agents |
| **Microsoft Agent Framework** | Developers building standalone or multi-agent systems | Lightweight kit; single and multi-agent systems; multiple orchestration patterns |
| **AutoGen** | Developers/researchers: rapid prototyping | Open-source; ideal for **experimentation and research** with agents |
| **OpenAI Assistants API** | Developers using OpenAI models specifically | Subset of Foundry Agent Service features; limited to OpenAI models only |

---

### 2.1 Decision Guide by User Type

| User Type / Scenario | Recommended Solution | Typical Use Cases |
|---|---|---|
| **Business user, no coding experience** | Copilot Studio lite (M365 Copilot Chat) | **Automate everyday tasks**; empower non-technical staff |
| **Business user with low-code skills** | Copilot Studio (full version) | Build **low-code agentic solutions**; extend enterprise productivity tools |
| **Professional dev: extending M365 Copilot** | Microsoft 365 Agents SDK | Custom M365 integrations; advanced agent behaviors in Microsoft ecosystem |
| **Professional dev: building Azure AI solutions** | **Foundry Agent Service** | Scalable, customized agentic solutions using Azure infrastructure |
| **Developer: multi-agent or orchestrated systems** | Microsoft Agent Framework | Complex orchestrated agent systems across diverse environments |
| **Developer: experimenting / research** | AutoGen | Rapid prototyping; research and ideation with agents |

> **Note**: There is overlap between solutions, final choice may also depend on existing tool familiarity, programming language, and team preferences.

---

### 2.2 Foundry Agent Service vs. OpenAI Assistants API

| | **Foundry Agent Service** | **OpenAI Assistants API** |
|---|---|---|
| **Basis** | Based on the OpenAI Assistants API | Original API from OpenAI |
| **Model support** | OpenAI models + models from Foundry model catalog | **OpenAI models only** |
| **Data integration** | Broader: Azure AI Search, Bing, custom data | More limited |
| **Enterprise security** | Full Azure enterprise security features | Standard OpenAI security |
| **SDKs supported** | OpenAI SDK + Azure Foundry SDK | OpenAI SDK |
| **Flexibility** | **Greater**: recommended for Azure development | Subset of Foundry Agent Service |

---

## 3. Microsoft Foundry Agent Service (Deep Dive)

> **Foundry Agent Service** is a managed service within Azure for **creating, testing, and managing** AI agents.

**Two development experiences:**
- **Visual**: Agent development in the Microsoft Foundry portal (playground interface)
- **Code-first**: Development using the Microsoft Foundry SDK

---

### 3.1 The 3 Components of a Foundry Agent

> Every agent built with Foundry Agent Service has three elements.

```
[Agent]
    ├── [Model]      ← the AI brain — reasons and generates responses
    ├── [Knowledge]  ← data sources that ground the agent's responses
    └── [Tools]      ← functions the agent can invoke to take action
```

| Component | What It Is | Options Available |
|---|---|---|
| **Model** | A deployed generative AI model that enables the agent to **reason and generate natural language responses** | Common OpenAI models + models from the Foundry model catalog |
| **Knowledge** | Data sources that ground prompts with **contextual, factual data** | **Internet search** (Bing), **Azure AI Search index**, your own data/documents |
| **Tools** | Programmatic functions that enable the agent to **automate actions** | Built-in: **Azure AI Search, Bing, Code Interpreter**; Custom: your own code, Azure Functions |

---

### 3.2 Knowledge Sources (Grounding Options)

| Knowledge Source | What It Provides |
|---|---|
| **Microsoft Bing (Internet search)** | Real-time information **from the web**, up-to-date content |
| **Azure AI Search index** | Your own indexed data (documents, databases), grounded in your private content |
| **Own data and documents** | Uploaded files, documents, or custom data stores |

> This is the same **RAG (grounding) pattern** as mentioned before, the agent retrieves relevant context before generating a response.

---

### 3.3 Built-in Tools

| Built-in Tool | What It Does |
|---|---|
| **Azure AI Search** | Searches and retrieves data from an Azure AI Search index |
| **Bing** | Searches the internet for up-to-date information |
| **Code Interpreter** | Generates and **runs Python code** to perform calculations or data processing tasks |

**Custom tools**: you can also create your own:
- **Your own code** (custom functions)
- **Azure Functions** (**serverless** functions)

---

### 3.4 Threads: Conversation Memory

> A **thread** is the mechanism that gives an agent **conversational memory**.

| Term | Definition |
|---|---|
| **Thread** | A conversation session between a user and an agent, retains the **full history** of messages exchanged |
| **What it stores** | All messages in the conversation + any **data assets** (e.g., files) generated during the conversation |

> Threads are what make agents different from stateless chatbots, the agent **remembers everything said** in the conversation.

---

## 4. Quick Reference

### Traditional vs. Agent Frameworks

| Dimension | Traditional AI | AI Agent Framework |
|---|---|---|
| Behavior | Reactive (responds to input) | **Proactive** (reasons, acts, learns) |
| Agents | Single model interaction | **Multi-agent coordination** |
| Task scope | Single operations | **Multi-step autonomous workflows** |

### All Agent Development Solutions

| Solution | User Type | Code Level |
|---|---|---|
| Copilot Studio lite (M365) | Business users | No-code (declarative) |
| Copilot Studio (full) | Low-code developers | Low-code |
| M365 Agents SDK | Pro devs (M365) | Full code |
| **Foundry Agent Service** | **Pro devs (Azure)** | **Full code** |
| Microsoft Agent Framework | Pro devs (multi-agent) | Full code |
| AutoGen | Researchers/devs | Full code (open-source) |
| OpenAI Assistants API | OpenAI-only devs | Full code (limited) |

### Foundry Agent — 3 Components

| Component | Purpose | Options |
|---|---|---|
| **Model** | Reason + generate responses | OpenAI models + Foundry catalog |
| **Knowledge** | Ground responses with real data | Bing, Azure AI Search, own data |
| **Tools** | Take action | Bing, Azure AI Search, Code Interpreter, custom code, Azure Functions |