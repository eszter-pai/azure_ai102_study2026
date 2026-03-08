# Module: Integrate MCP Tools with Azure AI Agents
## Session: MCP Tool Discovery, Client-Server Setup & Azure AI Agent Integration
**Sources:**
- [Understand MCP tool discovery](https://learn.microsoft.com/en-us/training/modules/connect-agent-to-mcp-tools/2-understand-mcp-tool-discovery)
- [Integrate agent tools using an MCP server and client](https://learn.microsoft.com/en-us/training/modules/connect-agent-to-mcp-tools/3-mcp-client-server-setup)
- [Use Azure AI agents with MCP servers](https://learn.microsoft.com/en-us/training/modules/connect-agent-to-mcp-tools/4-use-azure-ai-agents-with-mcp)

---

## 1. The Problem: Managing Tools Is Complex

As AI agents grow, so does the number of tools they need. Traditional approach:
- Each integration requires **manual coding**
- Every API change requires **updating agent code**
- Managing many tools = increased complexity and maintenance

> **Solution**: Use **MCP (Model Context Protocol)**

---

## 2. What Is MCP (Model Context Protocol)?

> **MCP** = an open, standardized protocol that allows AI agents to **discover, connect to, and use tools** hosted on MCP servers, without needing to know each tool's details in advance.

### 3 Key Advantages of MCP

| Advantage | Description |
|---|---|
| **Dynamic Tool Discovery** | Agent automatically receives a list of available tools from a server at runtime |
| **Interoperability Across LLMs** | Works with different LLMs; switch or evaluate core models without reworking integrations |
| **Standardized Security** | Consistent authentication across multiple MCP servers, **no separate keys per API** |

---

## 3. What Is Dynamic Tool Discovery?

> **Dynamic tool discovery** = agent queries a centralized MCP server to find available tools

The MCP server acts as a **live catalog** of tools. This means:

- Tools can be **added, updated, or removed centrally** without modifying agent code
- Agents always use the **latest version** of each tool
- Tool management complexity moves **away from the agent** into a dedicated service

### 4 Benefits of Dynamic Tool Discovery

| Benefit | Description |
|---|---|
| **Scalability** | **Add/update** tools without redeploying agents |
| **Modularity** | **Agents focus on delegation**, not managing tool details |
| **Maintainability** | Centralized tool management reduces duplication and errors |
| **Flexibility** | Supports diverse tool types and complex workflows |

---

## 4. MCP Architecture: Server + Client

### How the Pipeline Works

```
MCP Server (hosts tools)
       ↓
MCP Client (discovers tools dynamically)
       ↓
Azure AI Agent (uses tools to respond to user)
```

### MCP Server

> The **MCP server** = a **registry/catalog** of tools your agent can use.

| Concept | Detail |
|---|---|
| Initialize with | `FastMCP("server-name")` |
| Tool decorator | `@mcp.tool`: marks a function **as an exposed tool** |
| Auto-generation | `FastMCP` uses **Python type hints + docstrings** to automatically generate tool definitions |
| Tool definitions served | Over HTTP when the client requests them |
| Update tools | Add/update tools on the server, **no need to modify or redeploy the agent** |

### MCP Client

> The **MCP client** = a bridge between the MCP server and the Azure AI Agent Service.

**3 tasks the client performs:**

1. **Discover available tools** from the server using `session.list_tools()`
2. **Generate** Python function stubs that wrap each tool
3. **Register** those functions with the agent

Each tool is wrapped in an **async function** (a function that can pause and wait) that invokes `session.call_tool(tool_name, tool_args)`.
**This enable asynchoronous invocation so the agent can call tools without blockingl.**
**The wrapped functions** are bundled into `FunctionTool` objects and **added to the agent's toolset**.

### Full Integration Flow (Client Setup)

```
MCP server hosts tool definitions → decorated with @mcp.tool
         ↓
MCP client connects to server
         ↓
Client fetches tools with session.list_tools()
         ↓
Each tool wrapped in async function → invokes session.call_tool()
         ↓
Tool functions bundled into FunctionTool
         ↓
FunctionTool registered to agent's toolset
         ↓
Agent invokes tools through natural language interaction
```

---

## 5. Using Azure AI Agents with Remote MCP Servers (Simplified Approach)

> When using **Foundry Agent Service** with MCP, you **don't need to manually create an MCP client session** or wrap function tools. Instead, use the built-in `MCPTool` object.

### What You Need

- A **remote MCP server endpoint** (e.g., `https://api.githubcopilot.com/mcp/`)
- A Microsoft Foundry **agent configured with an** `MCPTool`

### MCPTool Parameters

| Parameter | Required | Description |
|---|---|---|
| `server_label` | Yes | Unique identifier for the MCP server (e.g., `"GitHub"`) |
| `server_url` | Yes | The MCP server's URL |
| `allowed_tools` | Optional | List of specific tools the agent is allowed to access |
| `require_approval` | Optional | Boolean, if `true`, **agent pauses and waits for human approval** before invoking tools |

### How to Add Headers (Authentication)

Use `update_headers` to pass:
- **API keys**
- **OAuth tokens**
- Any other headers required by the MCP server

### Approval Settings for `require_approval`

| Value | Behavior |
|---|---|
| `always` (default) | Developer must approve every tool call |
| `never` |  tools invoke automatically |

---

## 6. Tool Invocation Flow (Foundry Agent Service + MCPTool)

```
1. Create MCPTool with server_label and server_url
2. Use update_headers for authentication
3. Set require_approval (always / never)
4. Create agent — add MCPTool to tools list
5. Invoke a prompt on the agent
         ↓ (if require_approval = always)
   Agent returns mcp_approval_request
   → contains info about which tool is being invoked
   → Developer reviews and approves
   → Send follow-up with mcp_approval_response
      (includes approval_request_id + approve: true/false)
         ↓ (if require_approval = never)
   Tools invoked automatically — results appear in response
```

---

## 7. MCP Client Setup vs. Foundry MCPTool

| Approach | When to Use | Key Difference |
|---|---|---|
| **MCP Client + FunctionTool** (manual) | Custom setups; need fine-grained control | Must create **client session**, wrap tools in async functions, bundle into FunctionTool |
| **MCPTool (Foundry built-in)** | Foundry Agent Service; simpler integration | **No manual client session; no function wrapping**; just configure MCPTool + add to agent |

---

## 8. Multiple MCP Servers

> You can connect an agent to **multiple MCP servers** by adding multiple `MCPTool` objects, each with its own `server_label` and `server_url`.

This allows you to:
- Pull tools from **different providers** (e.g., GitHub, a weather API, an internal tool server)
- Use **different tools per request** based on the user's needs

---

## 9. Quick Reference — Exam Tips

| Concept | Key Point |
|---|---|
| **MCP** | Open, standardized protocol for dynamic tool discovery |
| **Dynamic tool discovery** | Agent queries MCP server at runtime — no hardcoded tool knowledge |
| **"Integrate once"** | Core MCP advantage — add tools to server without touching agent code |
| **Interoperability** | MCP works across different LLMs |
| **`@mcp.tool`** | Decorator that marks a function as an MCP-exposed tool on the server |
| **`FastMCP`** | Class to initialize an MCP server; auto-generates tool defs from type hints + docstrings |
| **`session.list_tools()`** | Client method to discover available tools from the MCP server |
| **`session.call_tool()`** | Client method to invoke a specific tool |
| **`FunctionTool`** | SDK object used to bundle wrapped tool functions and register them with the agent |
| **`MCPTool`** | Foundry built-in — connects agent to remote MCP server; no manual client session needed |
| **`require_approval`** | `always` (default) = human approves each call; `never` = automatic invocation |
| **`mcp_approval_request`** | Returned by agent when tool needs approval; contains tool info |
| **`mcp_approval_response`** | Sent by developer to approve/deny; includes `approval_request_id` + `approve` boolean |
| **Multiple servers** | Add multiple `MCPTool` objects to connect to different MCP servers |
| **Clean separation** | Server manages tools; agent focuses on logic — update tools without redeploying agent |
