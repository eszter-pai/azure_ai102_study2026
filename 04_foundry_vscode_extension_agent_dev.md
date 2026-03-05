# Module: Develop AI Agents with the Microsoft Foundry Extension in Visual Studio Code
## Session: VS Code Extension Setup, Agent Development & Extending with Tools
**Sources:**
- [Get started with the Microsoft Foundry extension](https://learn.microsoft.com/en-us/training/modules/develop-ai-agents-vs-code/2-get-started-with-extension)
- [Develop AI agents in Visual Studio Code](https://learn.microsoft.com/en-us/training/modules/develop-ai-agents-vs-code/3-agent-development)
- [Extend AI agent capabilities with tools](https://learn.microsoft.com/en-us/training/modules/develop-ai-agents-vs-code/4-extend-agent-capabilities)

---

## 1. What Is the Microsoft Foundry VS Code Extension?

> The **Microsoft Foundry for Visual Studio Code** extension brings **enterprise-grade AI agent development** directly into VS Code.

**5 integrated experiences provided by the extension:**

| Capability | What It Provides |
|---|---|
| **Agent Discovery & Management** | Browse, create, and manage AI agents within your Foundry projects |
| **Visual Agent Designer** | Intuitive interface to configure agent instructions, tools, and capabilities visually |
| **Integrated Testing (Playground)** | Test agents in real-time using the built-in playground |
| **Code Generation** | Generate sample integration code to connect agents with your applications |
| **Deployment Pipeline** | Deploy agents directly to Microsoft Foundry for production use |

---

## 2. Getting Started Workflow (7 Steps)

| Step | Action |
|---|---|
| **1** | **Install and configure** the extension in VS Code |
| **2** | **Connect** to your Microsoft Foundry project |
| **3** | **Create or import** an AI agent using the designer |
| **4** | **Configure** agent instructions and add necessary tools |
| **5** | **Test** the agent using the integrated playground |
| **6** | **Iterate** on the design based on test results |
| **7** | **Generate code** for application integration |

---

## 3. Creating an Agent in VS Code

### 3.1 Prerequisites

| Prerequisite | Action |
|---|---|
| **Azure account** | Sign in via the extension |
| **Foundry project** | Create a default project OR select an existing one |
| **Model deployment** | Deploy a model for the agent to use, OR use an existing deployment |

### 3.2 Steps to Create a New Agent

1. Open the **Microsoft Foundry Extension view** in VS Code
2. Navigate to the **Resources section**
3. Select the **+ (plus) icon** next to the **Agents subsection**
4. Configure agent properties in the **Agent Designer view** that opens

> When you create an agent, the extension automatically opens **two things simultaneously**:
> - The **agent `.yaml` file** (direct configuration access)
> - The **Designer view** (visual interface)

---

## 4. Configuring Agent Properties

### 4.1 Properties in the Agent Designer

| Property | Description |
|---|---|
| **Agent name** | Descriptive name for your agent |
| **Model selection** | Choose from your deployed models (the **deployment name**) |
| **Description** | Clear description of what the agent does |
| **System instructions** | Defines the agent's behavior, personality, and response style |
| **Agent ID** | **Automatically generated** by the extension |

---

### 4.2 The Agent YAML File

> Every agent is stored as a **YAML configuration file**

```yaml
# yaml-language-server: $schema=https://aka.ms/ai-foundry-vsc/agent/1.0.0
version: 1.0.0
name: my-agent
description: Description of the agent
id: ''
metadata:
  authors:
    - author1
  tags:
    - tag1
model:
  id: 'gpt-4o-1'
  options:
    temperature: 1
    top_p: 1
instructions: Instructions for the agent
tools: []
```

**Key YAML fields:**

| Field | Purpose |
|---|---|
| `name` | Agent identifier |
| `description` | What the agent does |
| `id` | Auto-generated agent ID |
| `model.id` | The deployment name of the model to use |
| `model.options` | Model parameters (temperature, top_p, etc.) |
| `instructions` | The system prompt |
| `tools` | List of tools the agent can use (empty `[]` = no tools) |

---

## 5. Writing Effective Agent Instructions

> **Instructions = system prompt**. 

| Best Practice | What It Means |
|---|---|
| **Be specific and clear** | Define exactly what the agent should do and how it should behave |
| **Provide context** | Explain the agent's role and the environment it operates in |
| **Set boundaries** | Define what the agent should AND should NOT do |
| **Include examples** | Show examples of desired interactions |
| **Define personality** | Establish the tone and communication style |

**Example: customer service agent instructions should cover:**
- The agent's role and purpose
- Guidelines for handling different inquiry types
- Escalation procedures for complex issues
- Tone and communication style preferences

---

## 6. Deploying an Agent

### 6.1 Deployment Steps

| Step | Action |
|---|---|
| **1** | Select **"Create on Microsoft Foundry"** button (bottom-left of the Designer) |
| **2** | Wait for deployment|
| **3** | **Refresh the Azure Resources view** in the VS Code navbar |
| **4** | Verify the agent appears under the **Agents subsection** |

### 6.2 Managing a Deployed Agent

| Action | How |
|---|---|
| **View details** | Select the deployed agent → opens Agent Preferences page |
| **Edit + redeploy** | Select "Edit Agent" → modify → click **"Update on Microsoft Foundry"** |
| **Generate integration code** | Select **"Open Code File"** → sample code to use the agent in an app |
| **Test** | Select **"Open Playground"** → interact with the deployed agent |

---

## 7. Threads, Messages, and Runs

| Concept | Definition |
|---|---|
| **Thread** | A conversation session, stores messages and handles context |
| **Message** | An individual interaction, can include text, images, and files |
| **Run** | A single execution of an agent against the current thread |

> Managed via the **Azure Resources view** in the extension.

---

## 8. Built-in Tools

> Built-in tools are **production-ready**, no additional setup or configuration required.

| Tool | What It Does |
|---|---|
| **Code Interpreter** | Writes and executes Python code, math calculations, data analysis, chart generation, file processing |
| **File Search** | RAG over uploaded/indexed documents; supports PDF, Word, text files; uses a **vector store** |
| **Grounding with Bing Search** | Real-time web search, current events, trending topics; provides **citations and sources** |
| **OpenAPI Specified Tools** | Connects agents to external APIs via **OpenAPI 3.0 specifications** |
| **Model Context Protocol (MCP)** | Standardized interfaces for extended, community-driven tools |

---

## 9. Adding Tools in VS Code (5 Steps)

1. Select your **agent** in the extension
2. Navigate to the **Tools section** in the configuration panel
3. Browse **available tools** from the tool library
4. **Configure** tool settings as needed
5. **Test** tool integration using the playground

> When adding a tool that needs a data store (e.g., File Search), you can **use an existing vector store** or **create a new one** for your uploaded files.

---

## 10. Model Context Protocol (MCP) Servers

> **MCP servers** provide a standardized, open protocol for adding **reusable and community-built tools to agents**.

| Benefit | Description |
|---|---|
| **Standardized protocol** | Consistent communication between **agents and tools** |
| **Reusable components** | Tools work across different agent implementations |
| **Community-driven tools** | Available through MCP registries |
| **Simplified integration** | Consistent interfaces reduce custom work |

Extension supports MCP via: **registry browsing, custom server addition, configuration management, and testing/validation**.

---

## 11. Tool Management Best Practices

| Practice | Why It Matters |
|---|---|
| **Identify requirements first** | Know what capabilities the agent actually needs |
| **Start with built-in tools** | Use **built-ins** before writing custom solutions |
| **Test thoroughly** | Validate tool behavior across various scenarios |
| **Monitor performance** | Track tool usage and effectiveness in production |

---

## 12. Quick Reference

### Extension Capabilities

| Feature | Purpose |
|---|---|
| Visual Agent Designer | Configure agent without writing YAML manually |
| Built-in Playground | Test agent in real-time before and after deployment |
| YAML file | Direct configuration file — editable alongside the designer |
| Code Generation | Create sample integration code for your app |
| Azure Resources view | View/manage threads, runs, and deployed agents |

### Agent YAML Key Fields

| Field | Notes |
|---|---|
| `name` | Your chosen agent name |
| `model.id` | Deployment name from your Foundry project |
| `instructions` | System prompt — behavior + personality + boundaries |
| `id` | Auto-generated — do not set manually |
| `tools` | List of tools; empty `[]` = no tools |

### Built-in Tools Summary

| Tool | Primary Use |
|---|---|
| Code Interpreter | Python execution — math, data analysis, charts |
| File Search | RAG over uploaded docs using a vector store |
| Bing Search (Grounding) | Real-time web data + citations |
| OpenAPI Spec | Call external APIs (OpenAPI 3.0) |
| MCP | Community-built standardized tool interfaces |

### Thread / Message / Run

| Term | What It Is |
|---|---|
| Thread | Conversation session (stateful — stores full history) |
| Message | One interaction (text, images, or files) |
| Run | One agent execution against the thread |

### Exam Tips

| Concept | Key Point |
|---|---|
| **Extension purpose** | Brings Foundry Agent Service into VS Code — no context switching |
| **Two views on agent creation** | YAML file + Designer view open simultaneously |
| **Agent ID** | **Auto-generated** — never set manually |
| **Instructions** | System prompt — defines purpose, behavior, boundaries, tone |
| **Deploy button** | **"Create on Microsoft Foundry"** in bottom-left of Designer |
| **Update after edit** | **"Update on Microsoft Foundry"** button |
| **Integration code** | **"Open Code File"** generates sample code for using the agent |
| **Thread** | Stateful conversation session; stores history + data artifacts |
| **Run** | A single agent execution against the thread |
| **Code Interpreter** | Python sandbox — math, data analysis, chart generation, file processing |
| **File Search** | RAG tool — uses a **vector store** for uploaded documents |
| **Bing Grounding** | Real-time web search + provides citations and sources |
| **OpenAPI Spec** | Calls external APIs using OpenAPI 3.0 spec |
| **MCP servers** | Standardized, community-built tools via open protocol |
| **Best practice** | Start with built-in tools before creating custom solutions |
