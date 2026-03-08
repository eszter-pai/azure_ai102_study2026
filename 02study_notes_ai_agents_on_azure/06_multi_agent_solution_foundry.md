# Module: Develop a Multi-Agent Solution with Microsoft Foundry Agent Service
## Session: Connected Agents + Designing a Multi-Agent Solution
**Sources:**
- [Understand connected agents](https://learn.microsoft.com/en-us/training/modules/develop-multi-agent-azure-ai-foundry/2-understand-connected-agents)
- [Design a multi-agent solution with connected agents](https://learn.microsoft.com/en-us/training/modules/develop-multi-agent-azure-ai-foundry/3-design-multi-agent-solution)

---

## 1. The Problem with a Single Agent

As AI solutions grow in complexity, a single agent handling everything becomes:
- **Hard to manage**: scope creep makes it unmanageable
- **Hard to debug**: failures are harder to isolate
- **Hard to extend**: adding new capabilities risks breaking existing ones

> **Solution**: Use **connected agents**, multiple specialized agents that collaborate, each with a focused role.

---

## 2. What Are Connected Agents?

> **Connected agents** = a feature in Microsoft Foundry Agent Service that lets you **break large tasks into smaller, specialized sub-agents**, **without building a custom orchestrator** or hardcoding routing logic.

**Structure:**
```
User
  ↓
Main Agent (orchestrator)
  ├── Sub-Agent A (e.g., summarize document)
  ├── Sub-Agent B (e.g., validate policy)
  └── Sub-Agent C (e.g., retrieve data from knowledge source)
```

- The **main agent** interprets user input and delegates tasks to the right sub-agent
- Each **sub-agent** has a clearly defined, single responsibility
- The main agent aggregates results and returns a final response to the user

> Only the **main agent's response** is visible to the end user, sub-agent outputs are internal.

---

## 3. Why Use Connected Agents?

### 3 Core Benefits

| Benefit | Description |
|---|---|
| **No custom orchestration required** | The main agent uses **natural language** to route tasks|
| **Improved reliability and traceability** | Clear separation of responsibilities; agents can be **tested individually** |
| **Flexible and extensible** | **Add or swap sub-agents** without reworking the entire system or modifying the main agent |

### Additional Advantages

- Build **modular solutions** that are easier to develop and debug
- Assign **specialized capabilities** to agents that can be **reused across solutions**
- Scale your system in a way that aligns with real-world business logic
- Handle **sensitive tasks independently** (e.g., private data, personalized content) in isolated sub-agents

---

## 4. Agent Roles and Responsibilities

### Main Agent (Orchestrator)

| Responsibility | Description |
|---|---|
| Interpret user input | Understand the intent behind the request |
| Select the right sub-agent | Determine which connected agent is best suited |
| Forward context and instructions | Pass relevant information to the sub-agent |
| Aggregate results | Combine or summarize sub-agent outputs for the user |

### Connected Sub-Agents

| Responsibility | Description |
|---|---|
| Complete a specific action | Based on a clear, focused prompt |
| Use tools (if needed) | To complete their assigned task |
| Return results | Send results back to the main agent |

> **Design principle**: Each sub-agent should have a **single responsibility** (easier to **debug, extend, and reuse.**)

---

## 5. Setting Up a Multi-Agent Solution (7 Steps)

| Step | Action | Details |
|---|---|---|
| **1** | Initialize the agents client | Connect to your Microsoft Foundry project |
| **2** | Create the connected (sub) agent | Use `create_agent` on `AgentsClient`; define its purpose clearly in instructions |
| **3** | Initialize the `ConnectedAgentTool` | **Wrap the sub-agent** definition; assign a **name + description** so the main agent knows when/how to use it |
| **4** | Create the main agent | Use `create_agent`; add connected agents via the `tools` property using `ConnectedAgentTool` definitions |
| **5** | Create a thread and send a message | Thread manages conversation context; message contains the user's request |
| **6** | Run the agent workflow | Create a run → main agent routes tasks to sub-agents as needed → compiles final response |
| **7** | Handle the results | Review the main agent's response; it may incorporate insights from one or more sub-agents |

### Code Pattern

```python
# Step 1: Connect to Foundry project
client = AgentsClient(...)

# Step 2: Create a sub-agent
sub_agent = client.create_agent(
    name="stock-price-agent",
    instructions="You retrieve current stock prices for given ticker symbols.",
    model="gpt-4.1",
)

# Step 3: Wrap as a ConnectedAgentTool
connected_tool = ConnectedAgentTool(
    id=sub_agent.id,
    name="stock_price_agent",
    description="Retrieves current stock prices for a given ticker symbol.",
)

# Step 4: Create the main agent with the connected tool
main_agent = client.create_agent(
    name="financial-assistant",
    instructions="You are a financial assistant. Use your tools to answer user questions.",
    model="gpt-4.1",
    tools=[connected_tool],
)

# Step 5: Create a thread and send a message
thread = client.create_thread()
client.create_message(thread_id=thread.id, role="user", content="What is the stock price of MSFT?")

# Step 6: Run the workflow
run = client.create_run(thread_id=thread.id, agent_id=main_agent.id)
# ... poll until complete ...

# Step 7: Get the result
messages = client.list_messages(thread_id=thread.id)
print(messages[-1].content)  # Main agent's final response
```