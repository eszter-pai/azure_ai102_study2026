# Module: Orchestrate a Multi-Agent Solution Using the Microsoft Agent Framework
## Session: Agent Framework Overview + Orchestration Patterns
**Sources:**
- [Understand the Microsoft Agent Framework](https://learn.microsoft.com/en-us/training/modules/orchestrate-semantic-kernel-multi-agent-solution/2-understand-agent-framework)
- [Understand Agent Orchestration](https://learn.microsoft.com/en-us/training/modules/orchestrate-semantic-kernel-multi-agent-solution/3-understand-agent-orchestration)
- [Use Concurrent Orchestration](https://learn.microsoft.com/en-us/training/modules/orchestrate-semantic-kernel-multi-agent-solution/4-use-concurrent-orchestration)
- [Use Sequential Orchestration](https://learn.microsoft.com/en-us/training/modules/orchestrate-semantic-kernel-multi-agent-solution/5-use-sequential-orchestration)
- [Use Group Chat Orchestration](https://learn.microsoft.com/en-us/training/modules/orchestrate-semantic-kernel-multi-agent-solution/6-use-group-chat-orchestration)
- [Use Handoff Orchestration](https://learn.microsoft.com/en-us/training/modules/orchestrate-semantic-kernel-multi-agent-solution/7-use-handoff-orchestration)
- [Use Magentic Orchestration](https://learn.microsoft.com/en-us/training/modules/orchestrate-semantic-kernel-multi-agent-solution/8-use-magentic-orchestration)

---

## 1. What Is the Microsoft Agent Framework?

> **Microsoft Agent Framework** = an open-source SDK for building AI-powered agents that can process user inputs, make decisions, and execute tasks autonomously (LLMs and traditional programming logic).

**Key design principles:**
- Agents can work **independently** or **collaborate** with other agents
- **Provider-agnostic**: **switch between** Azure OpenAI, OpenAI, Anthropic, etc. without changing code
- Supports both **multi-agent collaboration** and **human-agent interaction**

---

## 2. Core Components of the Agent Framework

| Component | Description |
|---|---|
| **Agents** | AI-driven entities that reason and execute tasks using LLMs, tools, and conversation history |
| **Agent orchestration** | **Multiple agents collaborate** using different patterns; unified interface to switch between them |
| **Chat clients** | **Abstractions connecting to AI services** (`BaseChatClient`); supports Azure OpenAI, OpenAI, Anthropic, etc. |
| **Tools and function integration** | Custom functions + built-in tools (Code Interpreter, File Search, Web Search); agents auto-invoke |
| **Conversation management** | `AgentSession` tracks history across interactions; role-based messages: USER, ASSISTANT, SYSTEM, TOOL |

---

## 3. Why Use the Microsoft Agent Framework?

| Advantage | Description |
|---|---|
| **Multi-source integration** | Integrate **agents from multiple sources** including Foundry Agent Service |
| **Multi-agent collaboration** | Agents specialize and work together on complex workflows |
| **Human-in-the-loop** | Agents augment human decision-making; support for human-agent interaction |
| **Provider-agnostic** | Switch AI providers without rewriting code |
| **Scalable** | From simple chatbots to complex enterprise solutions |

---

## 4. Why Multi-Agent Orchestration?

> Single-agent systems are limited by one set of instructions or one model prompt. Multi-agent orchestration solves this.

**What orchestration allows you to do:**
- Assign **distinct skills, responsibilities, or perspectives** to each agent
- **Combine outputs** from multiple agents to improve decision-making and accuracy
- **Coordinate steps** so each agent's work builds on the last
- **Dynamically route control** between agents based on context or rules

> Result: more **flexible, efficient, and scalable** solutions 

---

## 5. Workflows in the Microsoft Agent Framework



**3 things workflows provide:**
- Control over **how tasks are executed**
- **Multi-agent orchestration** support
- **Checkpointing**: save and resume workflow states

### 5.1 Core Workflow Components

#### Executors
> **Executors** = the main workers in a workflow. They r**eceive input, perform actions, and produce outputs**.

- Executors can be **AI agents** or **custom logic** components
- Example: one executor analyzes a travel request; another books the flight

#### Edges
> **Edges** = define **how messages flow between executors** (the **logic and order** of execution).

| Edge Type | Description | Example |
|---|---|---|
| **Direct Edge** | Connect one executor to another in sequence | After gathering input, next executor processes the booking |
| **Conditional Edge** | Trigger only when certain conditions are met | **If hotel unavailable** → suggest alternative dates |
| **Switch-Case Edge** | Route to different executors based on predefined conditions | VIP → premium executor; others → standard |
| **Fan-Out Edge** | **Send one message to multiple executors** simultaneously | One request → flight checker + hotel checker at once |
| **Fan-In Edge** | **Combine outputs from multiple executors into one** final step | Flight + hotel results → summary executor compiles itinerary |

#### Events (Observability & Debugging)

| Event | Triggered When |
|---|---|
| **WorkflowStartedEvent** | Workflow execution begins |
| **WorkflowOutputEvent** | Workflow produces an output |
| **WorkflowErrorEvent** | An error is encountered |
| **ExecutorInvokeEvent** | An executor starts processing a task |
| **ExecutorCompleteEvent** | An executor finishes its work |
| **RequestInfoEvent** | An external request is issued |

---

## 6. Supported Orchestration Patterns

> The framework provides **5 built-in orchestration patterns** — all technology-agnostic and sharing the same unified interface.

| Pattern | How It Works | Best For |
|---|---|---|
| **Concurrent** | Broadcast **the same task to multiple agents** simultaneously; collect results independently | Parallel analysis, independent subtasks, ensemble decision-making |
| **Sequential** | Pass output from one agent to the next in a fixed order | Step-by-step workflows, pipelines, progressive refinement |
| **Handoff** | **Dynamically transfer control** between agents based on context or rules | **Escalation, fallback, expert routing**: one agent works at a time |
| **Group chat** | Shared conversation among multiple agents (+ optional human); **a chat manager chooses who speaks next** | Brainstorming, collaborative problem-solving, building consensus |
| **Magentic** | Manager-driven; **plans, delegates, and adapts across specialized agents** | Complex, open-ended problems where the solution path evolves |

### 6.1 Concurrent Orchestration

> All agents receive **the same task** and work **simultaneously and independently**. Results are then gathered and combined.

**Key behaviours:**
- Agents do **not share results with each other** during execution
- An agent can call other agents internally via its own orchestration
- Results can be **combined into one final answer**, or each agent can produce its **own separate result**
- You can call **all registered agents every time**, or **select agents dynamically** based on the task

#### When to Use Concurrent

| Use It When | Example |
|---|---|
| Tasks can run independently at the same time | Checking multiple data sources in parallel |
| You need diverse specialized skills or approaches | Technical + business + creative agents all tackling same problem |
| Brainstorming or generating multiple ideas | Generate several solutions and pick the best |
| Ensemble **reasoning / voting / quorum** decisions | Multiple agents vote on the correct answer |
| Speed matters and parallel execution cuts wait time | Time-sensitive tasks |

#### When to Avoid Concurrent

| Avoid It When |
|---|
| Agents **need to build on each other's work** or share context in order |
| Task requires **a strict sequence** or predictable, repeatable results |
| **Resource/quota limits** make parallel execution inefficient |
| Agents can't reliably coordinate changes to shared data or external systems |
| No clear way to resolve conflicts between agent results |
| Combining results is too complex or lowers overall quality |

#### How to Implement (6 Steps)

| Step | Action |
|---|---|
| **1** | Create a **chat client** (e.g., `AzureOpenAIChatClient`) with credentials |
| **2** | Create **agent instances** using `chat_client.create_agent()` with instructions + name |
| **3** | Use **`ConcurrentBuilder`** class → add agents via `participants()` → call `build()` |
| **4** | Call workflow's **`run()`** method with the task |
| **5** | Extract outputs from workflow events using **`get_outputs()`** |
| **6** | Process aggregated messages, each includes **author name + content** to identify which agent responded |


---

### 6.2 Sequential Orchestration

> Each agent processes the task one after another. The **output of one becomes the input of the next**.

**Key behaviours:**
- Order is **fixed and decided beforehand**, agents don't decide what happens next
- Each step **builds on and improves** the previous one
- Best for **gradual refinement** (e.g., draft → review → polish)

#### When to Use Sequential

| Use It When | Example |
|---|---|
| Steps must happen in a specific order, each relying on the one before | Document review pipeline |
| Data workflows where each stage adds something the next stage needs | Data transformation pipeline |
| Stages can't run in parallel | Multi-stage reasoning |
| Gradual improvement is the goal | Draft → review → polish content |
| You know **how each agent performs and can handle delays/failures** | Controlled production pipelines |

#### When to Avoid Sequential

| Avoid It When |
|---|
| Stages can run independently and in parallel without affecting quality |
| A single agent can perform the entire task effectively |
| **Early stages may fail** and there's no way to stop downstream processing |
| Agents need to collaborate dynamically rather than hand off work |
|**Workflow requires iteration, backtracking, or dynamic routing** |

#### How to Implement (6 Steps)

| Step | Action |
|---|---|
| **1** | Create a **chat client** (e.g., `AzureOpenAIChatClient`) with credentials |
| **2** | Create **agent instances** using `chat_client.create_agent()` with instructions + name (defining pipeline role) |
| **3** | Use **`SequentialBuilder`** class → add agents via `participants()` → call `build()` |
| **4** | Call workflow's **`run_stream()`** method with the task |
| **5** | Iterate through workflow events with **async loop**; look for **`WorkflowOutputEvent`** instances |
| **6** | Collect the **final conversation** — shows how each agent in sequence contributed |

> **Builder class**: `SequentialBuilder`
> **Key difference from Concurrent**: uses `run_stream()` instead of `run()` and processes events as a stream

---

### 6.3 Group Chat Orchestration

> Multiple AI agents (and optionally a human) collaborate in a **managed conversation**. A **central chat manager** controls the flow, deciding which agent responds next and when to request human input.

**Key behaviours:**
- Agents don't directly change running systems, they **mainly contribute to the conversation**
- All output collected in a **single thread** → transparent and auditable
- Supports **human-in-the-loop**: a human can guide or intervene at any point
- Supports different styles: **free-flowing** ideation → **formal workflows** with defined roles

#### Maker-Checker Loop (Common Special Case)
> One agent (**maker**) proposes content/solutions; another agent (**checker**) reviews and critiques. Cycle repeats until the result is satisfactory. **Managed by the chat manager** turn-by-turn.

#### When to Use Group Chat

| Use It When | Example |
|---|---|
| Spontaneous or guided collaboration among agents (+ optional human) | Creative brainstorming |
| Iterative maker-checker loops | Draft → review → revise cycle |
| Real-time human oversight or participation | Human guides an agent debate |
| Transparent, auditable conversations needed | All output in one thread |
| Cross-disciplinary dialogue | Technical + legal + creative agents |
| Quality control requiring multiple expert perspectives | Content validation workflow |

#### When to Avoid Group Chat

| Avoid It When |
|---|
| Simple task delegation or linear pipelines suffice |
| Real-time speed requirements make discussion overhead impractical |
| Hierarchical or deterministic workflows needed (no discussion) |
| Chat manager can't clearly determine when the task is complete |
| Many agents involved, limit to **3 or fewer** for easier control |

#### How to Implement (6 Steps)

| Step | Action |
|---|---|
| **1** | Create a **chat client** (e.g., `AzureOpenAIChatClient`) with credentials |
| **2** | Create **agent instances** with instructions + name defining each role |
| **3** | Use **`GroupChatBuilder`** → add agents via `participants()` → call `build()` |
| **4** | Call workflow's **`run()`** method with the task |
| **5** | Extract outputs using **`get_outputs()`** |
| **6** | Process aggregated messages, each includes **author name + content** |


#### Custom Group Chat Manager

Extend the base **`GroupChatManager`** class to customize the chat flow. The manager calls these methods **in order each round**:

| Order | Method | Purpose |
|---|---|---|
| 1 | `should_request_user_input` | Check if human input is needed before the next agent speaks |
| 2 | `should_terminate` | Determine if the conversation should end (e.g., max rounds reached) |
| 3 | `filter_results` | If ending: summarize or process the final conversation |
| 4 | `select_next_agent` | If continuing: choose which agent speaks next |

---

### 6.4 Handoff Orchestration

> AI agents **transfer control to one another** based on task context or user requests. Each agent can "hand off" to another with the right expertise. Only **one agent works at a time**.

**Key behaviours:**
- routing emerges dynamically during processing
- Unlike concurrent/group chat: **strictly one agent active** at a time, full transfer of control
- Uses **switch-case routing** to direct the task based on classification results

#### When to Use Handoff

| Use It When | Example |
|---|---|
| Specialized knowledge needed but order/number of agents unknown upfront | Customer support triage |
| Expertise requirements emerge dynamically during processing | Content analysis triggers routing |
| **Multiple-domain** problems requiring different specialists sequentially | Legal → financial → technical review |
| Clear signals/rules define when and to whom control should transfer | Score threshold triggers escalation |

#### When to Avoid Handoff

| Avoid It When |
|---|
| Agents and their order are known upfront and fixed (use Sequential instead) |
| Task routing is simple and rule-based, not needing dynamic interpretation |
| Poor routing decisions would frustrate users |
| Multiple operations must run simultaneously (use Concurrent instead) |
| **Risk of infinite handoff loops** or excessive bouncing between agents |

#### How to Implement (4 Steps)

| Step | Action |
|---|---|
| **1** | Set up chat client + define **Pydantic models** for structured **JSON responses** + configure agents with `response_format` |
| **2** | Create **specialized executor functions**: **input storage, transformation** (JSON → typed routing object), handler **executors per classification outcome** |
| **3** | Build **routing logic**: factory functions for condition checkers per classification value; use with `Case` objects in switch-case edge groups; always include a **Default case** as fallback |
| **4** | Assemble with **`WorkflowBuilder`**: connect executors with **edges + switch-case edge** group for routing + terminal executor for final output |

---

### 6.5 Magentic Orchestration

> A **Magentic manager** coordinates a team of specialized agents for complex, open-ended tasks. The manager decides which agent acts next based on **evolving context, task progress, and agent capabilities**.

**Key behaviours:**
- Manager maintains a **shared context** and **dynamic task ledger** (records goals, subgoals, execution plans)
- Ledger is **built and refined in real time** as the workflow progresses
- Focuses on **building and documenting the approach** as much as on delivering the final solution
- The solution path is **not predetermined**, it adapts as **new information emerges**

#### When to Use Magentic

| Use It When | Example |
|---|---|
| Problem is **complex or open-ended** with no predetermined solution path | Research + analysis tasks |
| Input from multiple specialized agents needed to shape the solution | Cross-domain problem solving |
| System must generate a **documented plan** for human review | Auditable AI workflows |
| Agents have tools that interact **with external systems** | Real-world action agents |
| Step-by-step, **dynamically built execution plan** adds value | Planning before doing |

#### When to Avoid Magentic

| Avoid It When |
|---|
| Solution path is fixed or deterministic |
| No need for a ledger or plan of approach |
| Task is simple: use a lighter pattern |
| **Speed is the priority**: Magentic emphasizes planning over fast execution |
| Frequent stalls or loops without clear resolution path expected |

#### How to Implement (7 Steps)

| Step | Action |
|---|---|
| **1** | Create **specialized agent instances** (`ChatAgent`) with role-specific instructions |
| **2** | Define **async event handling callback** for orchestrator messages, agent updates, agent messages, and final results |
| **3** | Use **`MagenticBuilder`** → add agents via `participants()` → configure event callback with streaming mode |
| **4** | Configure **standard manager**: set `max_round_count`, `stall_count`, `reset_count` parameters |
| **5** | Call workflow's **`run_stream()`** method with the complex task |
| **6** | Iterate through workflow events with **async loop**; handle `WorkflowOutputEvent` for results |
| **7** | Extract final output — contains complete solution from collaborative effort |


> **Key feature**: dynamic task ledger built and refined throughout execution

---

## 7. Unified Orchestration Workflow (6 Steps)

> All 5 patterns share the **same interface**, you can switch between them without rewriting agent logic.

| Step | Action |
|---|---|
| **1** | Define your agents and describe their capabilities |
| **2** | Select and create an orchestration pattern (**+ optional manager agent**) |
| **3** | Optionally configure callbacks or transforms for custom input/output handling |
| **4** | **Start a runtime** to manage execution |
| **5** | **Invoke the orchestration** with your task |
| **6** | Retrieve results **asynchronously (non-blocking)** |

---

## 8. Edge Types Visual Summary

```
Direct:        A → B → C               (one path, sequential)

Conditional:   A →[if X]→ B            (branch when condition met)
                 →[else]→ C

Switch-Case:   A →[case 1]→ B          (predefined routes)
                 →[case 2]→ C

Fan-Out:       A → B                   (one message, many receivers)
                 → C
                 → D

Fan-In:        B →                     (many messages, one collector)
               C → [Fan-In] → E
               D →
```

