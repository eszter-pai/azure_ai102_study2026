# Module: Discover Azure AI Agents with A2A
## Session: Agent-to-Agent (A2A) Protocol; Define, Implement, Host, Connect

**Sources:**
- [Define an A2A Agent](https://learn.microsoft.com/en-us/training/modules/discover-agents-with-a2a/2-define-a2a-agent)
- [Implement an Agent Executor](https://learn.microsoft.com/en-us/training/modules/discover-agents-with-a2a/3-implement-agent-executor)
- [Host an A2A Agent Server](https://learn.microsoft.com/en-us/training/modules/discover-agents-with-a2a/4-host-a2a-agent-server)
- [Connect to an A2A Agent](https://learn.microsoft.com/en-us/training/modules/discover-agents-with-a2a/5-connect-to-a2a-agent)

---

## 1. What Is the A2A Protocol?

> **Agent-to-Agent (A2A) protocol** = a **standardized communication protocol** that allows **AI agents from different vendors or platforms to discover each other**, share context, invoke each other's capabilities, and exchange information securely.

**Key idea:** Agents don't need to be built on the same platform or use the same, LLM A2A provides the common language that lets them collaborate.

### 3 Core Advantages of A2A

| Advantage | Description |
|---|---|
| **Enhanced Collaboration** | Agents from different vendors/platforms can **share context and work together**, enabling automation across traditionally disconnected systems |
| **Flexible Model Selection** | **Each A2A agent** independently chooses **which LLM to use**, unlike some MCP scenarios that rely on a single shared LLM connection |
| **Integrated Authentication** | Authentication is **built into the protocol**, providing a robust security framework for agent-to-agent communication |

### A2A vs MCP

| Aspect | A2A | MCP |
|---|---|---|
| **Purpose** | Agent-to-agent communication | Model-to-tool communication |
| **LLM usage** | Each agent picks its own LLM | Typically one LLM connection |
| **Discovery** | **Via Agent Card** | Via tool definitions |
| **Authentication** | Built into protocol | Varies by implementation |

---

## 2. Agent Skills

> **Agent Skill** = a specific **capability** or function the agent can **perform**. It tells other agents and clients **what tasks the agent is designed to handle**.

Think of Agent Skills as building blocks that advertise the agent's abilities.

### Key Elements of an Agent Skill

| Element | Description |
|---|---|
| **ID** | Unique identifier **for the skill** |
| **Name** | **Human-readable name** describing the skill |
| **Description** | Detailed explanation of what the skill does |
| **Tags** | Keywords for categorization and easier discovery |
| **Examples** | Sample prompts or use cases illustrating the skill in action |
| **Input/Output Modes** | Supported data formats or media types (e.g., text, JSON) |

**Examples of skills:**
- Simple: "Hello World" skill → returns a basic greeting in text format
- Complex: Blog-writing skill → accepts a topic and returns a suggested title or outline

---

## 3. Agent Card

> **Agent Card** = a structured document (like a **digital business card**) that a routing agent or client retrieves to **discover an agent's capabilities** and learn how to interact with it.

The Agent Card is **how agents make themselves discoverable** in an A2A ecosystem.

### Key Elements of an Agent Card

| Element | Description |
|---|---|
| **Identity Information** | Name, description, and version of the agent |
| **Endpoint URL** | Where the agent's A2A service can be accessed |
| **Capabilities** | Supported A2A features such as streaming or push notifications |
| **Default Input/Output Modes** | Primary media types the agent can handle |
| **Skills** | List of the agent's skills that **other agents can invoke** |
| **Authentication Support** | Indicates if the agent requires credentials for access |

### Where the Agent Card is exposed

- Standard endpoint: `/.well-known/agent-card.json`
- Can include multiple versions or an "extended" card for authenticated users

### Discovery Flow

```
1. Agent defines its Skills
2. Agent publishes an Agent Card (at /.well-known/agent-card.json)
3. Other agents/clients retrieve the Agent Card
4. Requests are routed to the appropriate skill
5. Responses returned in supported formats
```

**Example workflow (technical writer):**
- Agent A: skill = generate article titles
- Agent B: skill = create outlines
- Routing agent retrieves both Agent Cards → orchestrates: title from Agent A → fed into Agent B → final outline produced

---

## 4. Agent Executor

> **Agent Executor** = the **core processing component** of an A2A agent. It defines how the agent processes **incoming requests, generates responses, and communicates with clients or other agents**. It is the bridge **between the A2A protocol and your agent's specific business logic**.

### Key Responsibilities

- Execute tasks requested by users or other agents
- Stream responses or send individual messages back to the client
- Handle task cancellation (if supported)

### Two Primary Operations

| Operation | Description |
|---|---|
| **Execute** | Processes incoming requests and generates responses; accesses request details (user input, task context); sends results via an **event queue** (messages, task updates, or artifacts) |
| **Cancel** | Handles requests to cancel an ongoing task; may not be supported for simple agents |

### Key Objects Used by the Executor

| Object | Role |
|---|---|
| **RequestContext** | Contains information about the incoming request (user input, task context) |
| **EventQueue** | **Communication channel for sending results and events** back to the client |

### Request Handling Flow (Hello World Example)

```
1. Agent has a helper class implementing its core logic (e.g., returns a string)
2. Executor receives a request → calls the agent's core logic
3. Executor wraps the result as an event → places it on the EventQueue
4. Routing mechanism delivers the event back to the requester
```

> For cancellation: a basic agent may only indicate that cancellation is **not supported**.

---

## 5. Hosting an A2A Agent Server

> Hosting your agent makes it **accessible over HTTP** to clients and other agents, enabling real-time interactions and multi-agent workflows.

### What Hosting Enables

- Exposes agent capabilities through the **Agent Card** (discoverable)
- Receives incoming A2A requests and **forwards them to the Agent Executor**
- Manages **task lifecycles**, including **streaming responses and stateful interactions**

The server acts as the **bridge between the agent's logic and the external world**.

### 3 Core Components of the Agent Server

| Component | Description |
|---|---|
| **Agent Card** | Describes capabilities, skills, and I/O modes; exposed at `/.well-known/agent-card.json`; can include an extended card for authenticated users |
| **Request Handler** | **Routes incoming requests** to the correct `AgentExecutor` method (execute or cancel); manages task lifecycle using a **Task Store** |
| **Server Application** | Built with **a web framework** (Python: **Starlette**); combined with an **ASGI server** (**Uvicorn**) to listen on a network interface and port |

### Task Store

> **Task Store** = tracks tasks, streaming data, and resubscriptions. Even simple agents require a Task Store to handle interactions reliably.

### 5-Step Setup: Hosting an A2A Agent Server

| Step | Action |
|---|---|
| **1** | Define the agent's skills and Agent Card |
| **2** | Initialize a **Request Handler** linking the Agent Executor with a Task Store |
| **3** | Set up the **Server Application** providing the Agent Card and Request Handler |
| **4** | Start the server using **Uvicorn (ASGI server)** to make it accessible on the network |
| **5** | Agent is now live, listens for incoming requests and responds per its defined skills |

### Technology Stack Summary

| Layer | Technology |
|---|---|
| **Web framework** | Starlette (Python) |
| **ASGI server** | Uvicorn |
| **Task management** | Task Store |
| **Routing** | Request Handler |

---

## 6. Connecting a Client to an A2A Agent

> A client is the **bridge between your application and the agent server**. It discovers, connects to, and communicates with the A2A agent.

### Client Responsibilities

- **Discover** the Agent Card (metadata about the agent and its endpoints)
- **Send requests** to the agent for processing
- **Receive and interpret** the agent's responses (direct messages or task-based results)

### 3-Step Connection Process

| Step | Action |
|---|---|
| **1** | Client must know the **base URL** of the server |
| **2** | Client retrieves the **Agent Card** from the well-known endpoint (`/.well-known/agent-card.json`) |
| **3** | Client is **initialized with the Agent Card**, establishing a connection ready to send messages |

### 2 Types of Requests

| Request Type | How It Works | When to Use |
|---|---|---|
| **Non-Streaming** | Client sends a message and waits for a **complete response** | Simple interactions; single response expected |
| **Streaming** | Client sends a message and receives responses **incrementally** as the agent processes | Long-running tasks; real-time user updates |

Both request types include:
- A `role` (e.g., `user`) and the message content
- A **unique identifier** for each request (typically a generated ID)

### 2 Types of Responses

| Response Type | Description |
|---|---|
| **Direct messages** | Immediate outputs from the agent (text or structured content) |
| **Task-based responses** | **Objects representing ongoing** tasks; may require follow-up calls to check status or retrieve results |

> Clients should be prepared to handle **both** response types.

### Streaming Behaviour

- Asynchronous, may provide **partial results** before the final output
- Simple agents return messages directly
- Advanced agents may manage **multiple simultaneous tasks**

---

## 7. Full A2A Architecture — How Everything Connects

```
CLIENT
  |
  |-- (1) Fetch Agent Card from /.well-known/agent-card.json
  |
  |-- (2) Send Request (non-streaming or streaming)
  |
SERVER (Starlette + Uvicorn)
  |
  |-- Request Handler
  |     |-- Task Store (tracks task state)
  |     |-- Routes to --> Agent Executor
  |                         |
  |                         |-- RequestContext (request details)
  |                         |-- Calls agent logic
  |                         |-- Places result on EventQueue
  |
  |-- Agent Card (/.well-known/agent-card.json)
        |-- Skills, Endpoint, Auth, I/O Modes
```

---

## 8. Component Reference Summary

| Component | What It Is | Key Role |
|---|---|---|
| **A2A Protocol** | Standardized agent communication standard | Enables cross-vendor/platform agent collaboration |
| **Agent Skill** | Description of one capability the agent can perform | Tells clients/agents what the agent can do |
| **Agent Card** | Structured discovery document for the agent | Published at `/.well-known/agent-card.json`; discoverable |
| **Agent Executor** | Core logic processor for incoming A2A requests | Bridges protocol ↔ business logic; uses RequestContext + EventQueue |
| **RequestContext** | Object containing the incoming request details | Read by executor to understand the task |
| **EventQueue** | Communication channel for sending results back | Used by executor to return responses/events |
| **Task Store** | Tracks task state, streaming data, resubscriptions | Required even for simple agents |
| **Request Handler** | Server-side router for incoming A2A requests | Links Agent Executor + Task Store |
| **Server Application** | HTTP server (Starlette + Uvicorn) | Hosts the agent; exposes Agent Card + request endpoints |
| **Client** | Application-side connector to the agent | Fetches Agent Card, sends requests, handles responses |

---

## Quick Reference — Exam Tips

| Exam Scenario | Key Answer |
|---|---|
| "How do agents from different vendors discover each other?" | Via the **Agent Card** published at `/.well-known/agent-card.json` |
| "What describes an agent's capabilities in A2A?" | **Agent Card** (identity, endpoint, capabilities, skills, auth) |
| "What defines a specific task an agent can perform?" | **Agent Skill** (ID, name, description, tags, examples, I/O modes) |
| "What is the bridge between A2A protocol and agent logic?" | **Agent Executor** |
| "What two objects does the Agent Executor use?" | **RequestContext** (input) + **EventQueue** (output) |
| "What are the two operations of an Agent Executor?" | **Execute** and **Cancel** |
| "What is required to track tasks on the server side?" | **Task Store** (required even for simple agents) |
| "What web framework/server hosts an A2A agent in Python?" | **Starlette** (framework) + **Uvicorn** (ASGI server) |
| "How does a client first connect to an A2A agent?" | Retrieve the **Agent Card** from the server's well-known endpoint |
| "What are the two types of client requests?" | **Non-Streaming** (wait for complete response) and **Streaming** (incremental) |
| "What are the two types of agent responses?" | **Direct messages** and **Task-based responses** |
| "A2A advantage over MCP for LLM selection?" | Each A2A agent independently selects its own LLM |
| "What is built into A2A that makes it enterprise-ready?" | **Integrated Authentication** |
