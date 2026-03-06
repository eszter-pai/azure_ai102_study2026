# Module: Develop an AI Agent with Microsoft Agent Framework
## Session: Understanding Agent Framework, Creating Azure AI Agents & Adding Tools
**Sources:**
- [Understand Microsoft Agent Framework AI agents](https://learn.microsoft.com/en-us/training/modules/develop-ai-agent-with-semantic-kernel/2-understand-semantic-kernel-agents)
- [Create an Azure AI agent with Microsoft Agent Framework](https://learn.microsoft.com/en-us/training/modules/develop-ai-agent-with-semantic-kernel/3-create-azure-ai-agent)
- [Add tools to Azure AI agent](https://learn.microsoft.com/en-us/training/modules/develop-ai-agent-with-semantic-kernel/4-add-plugins-to-agent)

---

## 1. What Is the Microsoft Agent Framework?

> **Microsoft Agent Framework** = an open-source SDK that enables developers to integrate AI models into applications and build agents that use natural language processing to complete tasks and collaborate with other agents.

- Supports creating agents backed by **multiple providers**: Azure OpenAI, OpenAI, Anthropic, Copilot, and more
- Agents can work **autonomously**, handling complex workflows without continuous human oversight
- Supports everything from simple chatbots to complex multi-agent business solutions

---

## 2. Core Components of the Microsoft Agent Framework

| Component | Description |
|---|---|
| **Agents** | Consistent interface for all agent types; supports function calling, multi-turn chat history, built-in tools, structured outputs, streaming |
| **Chat providers** | Abstractions for connecting to AI services (Azure OpenAI, OpenAI, Anthropic, Copilot, etc.) via `BaseAgent` |
| **Function tools** | Containers for custom functions that extend agent capabilities; agents auto-invoke them |
| **Built-in tools** | Code Interpreter (Python), File Search (documents), Web Search (internet) |
| **Conversation management** | Role-based message system (USER, ASSISTANT, SYSTEM, TOOL); `AgentSession` for persistent context |
| **Workflow orchestration** | Sequential, concurrent, group chat, and handoff patterns for multi-agent collaboration |

### Core Concepts

| Concept | Definition |
|---|---|
| **BaseAgent** | Foundation class for all agents; provides unified interface across all agent types |
| **AgentSession** | Manages persistent **conversation context and chat history** across sessions |
| **Chat messages** | **Role-based** messaging: USER, ASSISTANT, SYSTEM, TOOL |
| **Multi-modal support** | Agents work with text, images, and structured outputs (vision + type-safe responses) |
| **Authentication methods** | Azure CLI credentials, API keys, MSAL(Microsoft Authentication Library, for business login flow) , (Role-Based Access Control, to control which agents or services can access which Azure resources. e.g. only this agent can write to that storage account) |

---

## 3. Supported Agent Types

> you can **switch between providers without changing your code**.

| Provider | Notes |
|---|---|
| **Microsoft Foundry** | Enterprise-level; Azure-native; full Azure service integration |
| **Azure OpenAI** | OpenAI models hosted on Azure |
| **OpenAI** | Direct OpenAI API integration |
| **Microsoft Copilot Studio** | Copilot-based agents |
| **Anthropic** | Claude models |

---

## 4. What Is a Microsoft Foundry Agent (within Agent Framework)?

> **Microsoft Foundry Agent** = a specialized agent type within the framework designed for **enterprise-level** conversational AI with automatic tool calling and thread-based conversation management.

### 4 Key Benefits

| Benefit | Description |
|---|---|
| **Enterprise-level capabilities** | Built for Azure; supports Code Interpreter, Function tools, MCP |
| **Automatic tool invocation** | Agents automatically call and execute tool |
| **Thread and conversation management** | Built-in persistent conversation state across sessions |
| **Secure enterprise integration** | Azure CLI auth, RBAC, customizable storage |

---

## 5. Creating a Microsoft Foundry Agent (5 Steps)

| Step | Action |
|---|---|
| **1** | Create a Microsoft Foundry project |
| **2** | Add the project **connection string** to your application code |
| **3** | Set up authentication with `AzureCliCredential` |
| **4** | **Connect to project** with `AzureOpenAIResponsesClient` |
| **5** | Create an `Agent` instance with client, instructions, and tools |

After creating the agent: create an `AgentSession` to interact and get responses.

### Key Components Used in Code

| Component | Role |
|---|---|
| **`AzureOpenAIResponsesClient`** | Manages connection to Microsoft Foundry project; handles auth + security |
| **`Agent`** | Main agent class, combines **client + instructions + tools** |
| **`AgentSession`** | Tracks **conversation history**; manages thread state across interactions |
| **`AzureCliCredential`** | Authentication method for **accessing Foundry Tools** securely |
| **Tools integration** | **Custom functions auto-registered**; called by agent when needed |
| **Thread management** | Auto-create threads (simple) or explicit thread management (**ongoing conversations**) |

---

## 6. Adding Tools to a Microsoft Foundry Agent

### 6.1 Built-in Tools (No Setup Required)

| Tool | What It Does |
|---|---|
| **Code Interpreter** | Executes Python code for calculations and data analysis |
| **File Search** | Searches through and analyzes documents |
| **Web Search** | Retrieves information from the internet |

> These tools are automatically available, no extra configuration needed.

### 6.2 Custom Function Tools

> Custom tools use the **`@tool` decorator** from the Microsoft Agent Framework to register a Python function as a callable tool.

**5-step process for custom tools:**

| Step | Action | Details |
|---|---|---|
| **1** | Use `@tool` decorator | Registers function as a tool the AI can call; includes `name`, `description`, `approval_mode` parameters |
| **2** | Define function with annotations | Use Python type hints + `Annotated` and `Field` from **Pydantic** (a python lib for data validation using Python type hints.) for detailed parameter descriptions |
| **3** | Add tools to agent | Pass functions to agent via `tools` parameter during creation (single function or a list) |
| **4** | Invoke through conversation | No manual invocation needed, agent automatically calls tools based on context + descriptions |
| **5** | Use multiple tools | Add multiple functions; agent automatically chooses the right tool per request |

### Pydantic `Annotated` + `Field` (for parameter descriptions)

> Use `Annotated[type, Field(description="...")]` on function parameters so the AI understands **what each input means** and **how to use the function** correctly.

---

## 7. How Tool Calling Works (Automatic)

```
User sends message to agent
         ↓
Agent (LLM) reads tool names, descriptions, and parameter annotations
         ↓
Agent decides if a tool is needed for this request
         ↓
Framework routes request → executes the function in your code
         ↓
Result returned to LLM
         ↓
LLM generates final response using the result
```

---

## 8. Best Practices for Tool Development

| Practice | Why It Matters |
|---|---|
| **Clear descriptions** | Helps AI understand the tool's purpose and when to call it |
| **Type annotations** | Specify expected input/output types — required for schema generation |
| **Error handling** | Gracefully handles unexpected inputs |
| **Return meaningful data** | AI uses the return value to generate its response |
| **Keep functions focused** | Each tool should handle one specific task |

---

## 9. Agent Framework vs. Foundry Agent Service & When to Use Which

| Scenario | Use |
|---|---|
| Need **enterprise** features + Azure integration (RBAC, Key Vault, AI Search) | **Foundry Agent Service** (directly) |
| Need **multi-agent** orchestration, group chat, handoff patterns | **Microsoft Agent Framework** |
| Need to **switch between AI providers** (OpenAI, Anthropic, etc.) | **Microsoft Agent Framework** |
| Simple single-agent conversational app | Either works |
| **M365 integration** (Teams, Outlook, Copilot) | **Copilot Studio** |

---

## 10. Quick Reference — Exam Tips

| Concept | Key Point |
|---|---|
| **Microsoft Agent Framework** | Open-source SDK; supports multiple AI providers; function tools + orchestration |
| **BaseAgent** | Foundation class for all agent types in the framework |
| **AgentSession** | Manages persistent conversation context and thread history |
| **Microsoft Foundry Agent** | Enterprise-level agent type within the framework; automatic tool calling; thread management |
| **`AzureOpenAIResponsesClient`** | Connects agent to Microsoft Foundry project |
| **`AzureCliCredential`** | Authentication for Foundry Tools access |
| **`@tool` decorator** | Registers a Python function as a callable tool for the agent |
| **`approval_mode`** | Parameter on `@tool`; determines if human approval is needed per tool call |
| **Pydantic `Annotated` + `Field`** | Used to describe function parameters so AI knows how to use them |
| **Built-in tools** | Code Interpreter, File Search, Web Search — no setup required |
| **Automatic tool calling** | Agent decides when to call tools — no explicit invocation in code |
| **Provider flexibility** | Switch between OpenAI, Azure OpenAI, Anthropic without changing code |
| **Workflow patterns** | Sequential, concurrent, group chat, handoff — supported by the framework |
| **Chat message roles** | USER, ASSISTANT, SYSTEM, TOOL |
