# Module: Plan and prepare to develop AI solution on Azure
## Session: Microsoft Foundry + Developer Tools / SDKs
**Sources:**
- [Microsoft Foundry](https://learn.microsoft.com/en-us/training/modules/prepare-azure-ai-development/4-azure-ai-foundry)
- [Developer Tools and SDKs](https://learn.microsoft.com/en-us/training/modules/prepare-azure-ai-development/5-tools-and-sdks)

---

## 1. Microsoft Foundry

> **Definition:** Microsoft Foundry is the **recommended platform for AI development on Azure**. It provides **project organization, resource management, and AI development capabilities** through a web portal and an SDK.

- You can build AI solutions without it (directly using Foundry Tools resources), but Foundry is strongly recommended for all but the simplest solutions.
- Provides two interfaces:
  - **Microsoft Foundry Portal** — **web-based** visual interface
  - **Microsoft Foundry SDK** — build AI solutions programmatically

---

### 1.1 Microsoft Foundry Projects

> **Projects** are where you manage **resource connections, data, code**, and other elements of your AI solution.

There are **two types of projects**:

---

#### Type 1: Foundry Projects

| Property | Detail |
|---|---|
| **Associated resource** | **Microsoft Foundry** resource (in Azure subscription) |
| **Supports** | Microsoft Foundry Models (incl. OpenAI), Foundry Agent Service, Foundry Tools, evaluation & responsible AI tools |
| **Best for** | Generative AI **chat apps and agents** (most common AI development tasks) |
| **Admin overhead** | Minimal (right level of centralization for most use cases) |
| **Portal support** | Microsoft Foundry portal |

**Key capabilities:**
- Add connected resources easily
- Manage model and agent deployments
- Suitable for the majority of AI development scenarios

---

#### Type 2: Hub-Based Projects

| Property | Detail |
|---|---|
| **Associated resource** | **Azure AI Hub** resource (in Azure subscription) |
| **Includes** | Everything in a Foundry project + managed **compute** + **Prompt Flow** support + Azure **Storage** + **Azure Key Vault**|
| **Best for** | Advanced AI development: Prompt Flow apps, **fine-tuning** models, **collaborative** data science |
| **Admin overhead** | Higher (more infrastructure components managed) |
| **Portal support** | Microsoft Foundry portal **AND** **Azure Machine Learning portal** |

**Key capabilities:**
- **Prompt Flow** based application development
- **Fine-tuning** models
- **Secure** data storage via Azure Storage + Azure Key Vault
- **Collaborative** projects involving data scientists + ML specialists + developers

---

### 1.2 Project Type Comparison

| Feature | Foundry Project | Hub-Based Project |
|---|---|---|
| Microsoft Foundry resource | **Yes** | Yes (included) |
| Azure AI Hub resource | No | Yes |
| OpenAI / Foundry Models | **Yes** | Yes |
| Foundry Agent Service | **Yes** | Yes |
| Managed compute | No | Yes |
| Prompt Flow development | No | Yes |
| Fine-tuning models | No | Yes |
| Azure Storage integration | No | Yes |
| Azure Key Vault integration | No | Yes |
| ML portal access | No | Yes |
| Admin complexity | Low | Higher |
| **Use when...** | Building gen AI apps/agents | Advanced ML, Prompt Flow, fine-tuning |

---

## 2. Developer Tools and Environments

> While many tasks can be done in the Foundry portal, developers also need to **write, test, and deploy code** using standard development tools.

### 2.1 Supported IDEs (integrated development environment) / Editors

| Tool | Type | Best For |
|---|---|---|
| **Microsoft Visual Studio** | Full IDE | .NET / Windows application developers |
| **Visual Studio Code (VS Code)** | Code editor | Web developers; broad language/library support |

Both are suitable for developing AI applications on Azure.

---

### 2.2 Microsoft Foundry for VS Code Extension

> A VS Code extension that simplifies key tasks when building Microsoft Foundry generative AI applications.

**What it lets you do directly from VS Code:**
- Create a project
- Select and deploy a model
- Test a model in the playground
- Create an agent

---

### 2.3 GitHub and GitHub Copilot

| Tool | Role |
|---|---|
| **GitHub** | Source control + DevOps management: critical for team development |
| **GitHub Copilot** | AI assistant inside VS Code: improves developer productivity |

---

## 3. Programming Languages, APIs, and SDKs

> Azure AI applications can be built using many common languages. Key SDKs and APIs you need to know:

### 3.1 Supported Languages
- C# (.NET)
- Python
- Node.js
- TypeScript
- Java
- (and others)

---

### 3.2 Key SDKs and APIs

| SDK / API | Purpose | Notes |
|---|---|---|
| **Microsoft Foundry SDK** | Connect to **Foundry projects**; access resource connections | Gateway to other service-specific SDKs |
| **Microsoft Foundry Models API** | Work with **generative AI model endpoints** hosted in Foundry | **REST** interface |
| **Azure OpenAI in Foundry Models API** | Build **chat applications using OpenAI models** hosted in Foundry | Specifically for OpenAI-based apps |
| **Foundry Tools SDKs** | **Service-specific libraries (per AI service)** for multiple languages | Also accessible via **REST** APIs |
| **Microsoft Foundry Agent Service** | Build AI agent solutions | Accessed via **Foundry SDK**; integrates with **Semantic Kernel** |

---

### 3.3 SDK Relationship Diagram

```
Microsoft Foundry SDK
    │
    ├── Microsoft Foundry Models API        (generative AI endpoints)
    ├── Azure OpenAI in Foundry Models API  (OpenAI chat apps)
    ├── Foundry Tools SDKs                  (per-service: Vision, Speech, Language...)
    └── Microsoft Foundry Agent Service     (AI agents → integrates with Semantic Kernel)
```

---

### 3.4 Semantic Kernel

- A **framework** that can be **integrated with the Foundry Agent Service**
- Used to **build comprehensive AI agent solutions**
- Works alongside the Microsoft Foundry SDK

---

## 4. Quick Reference

### Decision Guide: Which Project Type?

| Scenario | Project Type |
|---|---|
| Building a chatbot / generative AI app | Foundry Project |
| Deploying and testing an OpenAI agent | Foundry Project |
| Fine-tuning a language model | Hub-Based Project |
| Building a Prompt Flow pipeline | Hub-Based Project |
| Collaborating with data scientists in Azure ML | Hub-Based Project |
| Need secure storage with Key Vault | Hub-Based Project |

### SDK Quick Pick

| Task | SDK / API |
|---|---|
| Connect to a Foundry project in code | Microsoft Foundry SDK |
| Call a generative AI model endpoint | Microsoft Foundry Models API |
| Build an OpenAI chat app | Azure OpenAI in Foundry Models API |
| Use Azure Vision / Speech / Language etc. | Foundry Tools SDKs (service-specific) |
| Build an autonomous AI agent | Microsoft Foundry Agent Service (+ Semantic Kernel) |
