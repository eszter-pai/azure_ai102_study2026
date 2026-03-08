# Module: Develop an AI Agent with Microsoft Foundry Agent Service
## Session: What Is an AI Agent, How to Use the Agent Service & Building Agents in Code
**Sources:**
- [What is an AI agent](https://learn.microsoft.com/en-us/training/modules/develop-ai-agent-azure/2-what-is-ai-agent)
- [How to use Microsoft Foundry Agent Service](https://learn.microsoft.com/en-us/training/modules/develop-ai-agent-azure/3-how-use-agent-service)
- [Develop agents with the Microsoft Foundry Agent Service](https://learn.microsoft.com/en-us/training/modules/develop-ai-agent-azure/4-when-use-agent-service)

---

## 1. What Is an AI Agent?

> An **AI agent** is a software service that uses **generative AI** to understand and perform tasks on behalf of a user or another program ( **advanced decision-making algorithms and machine learning models**)

**Key properties of an AI agent:**
- Understands **context**
- Makes **decisions**
- Utilizes **grounding data**
- Takes **actions** to achieve specific goals

---

## 2. Why Are AI Agents Useful?

| Benefit | Description |
|---|---|
| **Automation of routine tasks** | Handles **repetitive and mundane** tasks → frees humans for strategic/creative work → increased productivity |
| **Enhanced decision-making** | Processes **vast data**; analyzes trends; predicts outcomes; provides recommendations from **real-time data**; makes **autonomous decisions in complex scenarios** |
| **Scalability** | **Scale operations without proportional increases in human resources** (grow without significantly increasing costs) |
| **24/7 availability** | Operates continuously without breaks, tasks completed promptly; customer service available around the clock |

---

## 3. Real-World AI Agent Use Cases

| Agent Type | What It Does | Example |
|---|---|---|
| **Personal productivity** | Schedules meetings, sends emails, manages to-do lists, drafts documents, creates presentations | Microsoft 365 Copilot |
| **Research** | Monitors market trends, gathers data, generates reports continuously | Financial services (stock tracking), healthcare (medical research), marketing (consumer behavior) |
| **Sales** | Automates lead generation, qualifies leads, sends personalized follow-ups, schedules calls | Lets sales teams focus on closing deals |
| **Customer service** | Handles routine inquiries, provides information, resolves common issues via chatbots | **Cineplex AI agent**, processes refund requests, reducing handling time |
| **Developer** | Code review, bug fixing, repository management, codebase updates, coding standard enforcement | GitHub Copilot |

---

## 4. Microsoft Foundry Agent Service

> **Microsoft Foundry Agent Service** is a **fully managed service** that empowers developers to securely build, deploy, and scale high-quality, extensible AI agents, **without managing the underlying compute or storage resources**.

### 4.1 Purpose

- Create agents tailored to your needs with **custom instructions** and **advanced tools**
- Agents can: answer questions, perform actions, automate workflows
- Combines **generative AI models** with tools that interact with **real-world data sources**
-  now achievable in **fewer than 50 lines of code**
- instructions: system prompt, define prupose, scope, behavioral/restrictions rules.
- tools: functions, APIs, data sources the agent can call to take actions.


---

### 4.2 Key Features of Foundry Agent Service

| Feature | What It Provides |
|---|---|
| **Automatic tool calling** | Service handles the **entire tool-calling lifecycle**, **running the model, invoking tools, returning results**; no manual wiring needed |
| **Securely managed data** | Conversation states are securely managed using **threads**, developers don't handle this manually |
| **Out-of-the-box tools** | Built-in tools for **file retrieval, code interpretation, Bing, Azure AI Search, Azure Functions** |
| **Model selection** | Choose from various **Azure OpenAI models** |
| **Enterprise-grade security** | Data privacy and compliance; **keyless authentication (Entra ID)** |
| **Customizable storage** | Use **platform-managed storage** OR bring your own **Azure Blob Storage** for full control |

---

### 4.3 Azure Resource Requirements

> At minimum, you need an **Azure AI hub** + **Azure AI project**. You can add more Azure services as required.

**Two common setup architectures:**

| Setup | Resources Included |
|---|---|
| **Basic agent setup** | Azure AI hub + Azure AI project + Foundry Tools resources |
| **Standard agent setup** | Basic setup + **Azure Key Vault** + **Azure AI Search** + **Azure Storage** |

> Resources can be provisioned via the **Microsoft Foundry portal** or using **predefined Bicep templates**.

---

## 5. Agent Development, The 7-Step Code Pattern

> The same high-level code pattern applies regardless of language (Python, REST API, or other SDKs).

| Step | Action | Key Detail |
|---|---|---|
| **1** | Connect to project | Use project **endpoint** + **Entra ID** (keyless) authentication |
| **2** | Get/create agent | Specify model deployment, instructions, tools; can reuse an existing agent from the portal |
| **3** | Create thread | Thread = stateful session; **stores message history + generated data artifacts** |
| **4** | Add messages + invoke | Add user message to thread; run the agent against the thread |
| **5** | Check status + retrieve | Wait for agent to complete; retrieve its response messages and any generated files |
| **6** | Chat loop | Repeat steps 4–5 for multi-turn conversations |
| **7** | Delete + clean up | Delete agent and thread when done; removes data that is no longer needed |

---

## 6. Tools Available to Agents

> Tools give agents **enhanced functionality** beyond just generating text. The agent decides **when and how** to use each tool based on the conversation.

Tools can be assigned:
- In the **Microsoft Foundry portal** (visual)
- In **code using the SDK** (programmatic)

### 6.1 Knowledge Tools: Enhance Context and Grounding

| Tool | What It Does |
|---|---|
| **Bing Search** | Grounds prompts with **real-time live data from the web** using Bing search results |
| **File search** | Grounds prompts with data from **files stored in a vector store** |
| **Azure AI Search** | Grounds prompts with data from **Azure AI Search query results** (your private indexed data) |
| **Microsoft Fabric** | Uses the **Fabric Data Agent** to ground prompts with data from **Microsoft Fabric data stores** |

> You can also integrate **third-party licensed data** using the **OpenAPI Spec** action tool.

---

### 6.2 Action Tools: Perform Actions or Run Functions

| Tool | What It Does |
|---|---|
| **Code Interpreter** | A **sandbox** for model-generated Python code, can **access and process uploaded files**; used for **data analysis, graph generation, calculations** |
| **Custom function** | Call **your own custom function code**, you provide function definitions and implementations |
| **Azure Function** | Call code in **serverless Azure Functions** |
| **OpenAPI Spec** | Call **external APIs** based on the OpenAPI 3.0 spec, also works for third-party data integration |

---

### 6.3 Knowledge Tools vs. Action Tools Summary

| Category | Purpose | Tools |
|---|---|---|
| **Knowledge tools** | Enhance context, give agent access to data sources for grounding | Bing Search, File search, Azure AI Search, Microsoft Fabric |
| **Action tools** | Enable action, let agent execute code, call functions, call APIs | Code Interpreter, Custom function, Azure Function, OpenAPI Spec |

---

## 7. When NOT to Use Foundry Agent Service

> Foundry Agent Service is  **not always the right choice**.

| Scenario | Better Alternative |
|---|---|
| Building an integration **with Microsoft 365** | **Copilot Studio lite** experience |
| **Orchestrating multiple agents** in a complex system | **Semantic Kernel Agents Framework** |

---

## 8. Quick Reference

### Foundry Agent Service Key Features

| Feature | Key Point |
|---|---|
| Automatic tool calling | Full tool lifecycle handled by the service |
| Managed threads | Conversation state automatically stored and secured |
| Out-of-the-box tools | Bing, File search, Azure AI Search, Code Interpreter, Azure Functions |
| Enterprise security | Keyless authentication (Entra ID); data privacy and compliance |
