# Module: Build Agent-Driven Workflows Using Microsoft Foundry
## Session: Workflows: Patterns, Nodes, Agents, Power Fx, Maintenance, Code Integration

**Sources:**
- [Understand Workflows](https://learn.microsoft.com/en-us/training/modules/build-agent-workflows-microsoft-foundry/2-understand-workflows)
- [Identify Workflow Patterns](https://learn.microsoft.com/en-us/training/modules/build-agent-workflows-microsoft-foundry/3-identify-workflow-patterns)
- [Create Workflows in Microsoft Foundry](https://learn.microsoft.com/en-us/training/modules/build-agent-workflows-microsoft-foundry/4-create-workflows-microsoft-foundry)
- [Add Agents to a Workflow](https://learn.microsoft.com/en-us/training/modules/build-agent-workflows-microsoft-foundry/5-add-agents-to-workflow)
- [Apply Power Fx in Workflows](https://learn.microsoft.com/en-us/training/modules/build-agent-workflows-microsoft-foundry/6-apply-power-fx)
- [Maintain Workflows in Microsoft Foundry](https://learn.microsoft.com/en-us/training/modules/build-agent-workflows-microsoft-foundry/7-maintain-workflows)
- [Use Workflows in Code](https://learn.microsoft.com/en-us/training/modules/build-agent-workflows-microsoft-foundry/8-use-workflows-in-code)

---

## 1. What Are Workflows in Microsoft Foundry?

> **Workflows** = a way to orchestrate AI-driven actions using a **visual, declarative approach**. You define a sequence of **connected nodes** describing **what should happen and when**, the platform **manages execution and state**.

**Key idea:** Instead of writing code, you **arrange nodes in a visual designer** to control how information flows and how decisions are made.

### Why Use Workflows?

| Benefit | Description |
|---|---|
| **Multi-agent coordination** | Combine agents with different responsibilities (e.g., classification, decision-making, resolution) into one cohesive process |
| **Scalable automation** | More robust than single-agent solutions for complex or ambiguous tasks |
| **Human oversight** | **Can pause execution**, request human input, or escalate decisions when confidence is low |
| **Visual reasoning** | Easy to trace execution paths and understand logic at a glance |
| **Declarative** | Define **what** should happen; the platform manages **how** it executes |

---

## 2. The 3 Workflow Patterns

> Microsoft Foundry provides 3 **predefined workflow patterns**. Choose the right pattern based on how decisions are made, how data flows, and whether human input is needed.

| Pattern | How It Works | Best For |
|---|---|---|
| **Sequential** | Fixed, step-by-step path; each node passes output to the next | Pipelines, multi-stage processes (validate → enrich → respond); predictable and easy to reason about |
| **Human-in-the-loop** | Workflow pauses, asks for user input or approval, then resumes based on response | Approvals, confirmations, or when missing context must be provided by a person |
| **Group chat** | Dynamic; control shifts between multiple agents based on context, rules, or intermediate results | Complex requests, multi-domain Q&A, customer support, **agents build on each other's outputs** |

### Pattern Decision Guide

| Scenario | Use Pattern |
|---|---|
| Fixed pipeline with predictable steps | **Sequential** |
| Need human approval before proceeding | **Human-in-the-loop** |
| Multiple specialized agents must collaborate dynamically | **Group chat** |
| Low confidence → escalate to a human | **Human-in-the-loop** |

---

## 3. Node Types in the Workflow Builder

> A **workflow** = **connected nodes**, where each node performs a specific function. Nodes are the **building blocks** that turn concepts into functional workflows.

**Important:** Workflows are **not saved automatically**, save regularly to preserve versions.

### 5 Categories of Node Types

#### 3.1 Invoke (Agent Node)

> Invokes an AI agent from your Foundry project or creates a new one.

- Used for: **classification, reasoning, recommendations, any AI-driven task**
- Can return: **free-text responses** OR **structured outputs** (e.g., JSON)
- Structured outputs are essential when **agent responses drive control flow** (routing, variable assignment)
- Can configure: tools, knowledge bases, memory, guardrails

#### 3.2 Flow (Control Nodes)

> Controls the **execution path**, lets the workflow adapt dynamically.

| Flow Node | Description |
|---|---|
| **If/Else** | Branches execution based on conditions |
| **Go To** | Jumps to another node in the workflow |
| **For Each** | Loops over a list of items, performing the same actions for each one |

#### 3.3 Data Transformation Nodes

> Manipulates data and manages **variables**, ensures information **is correctly passed** between steps.

| Data Node | Description |
|---|---|
| **Set Variable** | Assigns a value to a variable for later use |
| **Reset Variable** | Clears or reinitializes a variable |
| **Parse Value** | Extracts specific data from structured outputs or converts values to different formats |

#### 3.4 Basic Chat Nodes

> **Sends messages to users** or asks questions to **collect input**.
- Often **paired with variables to capture responses**
- Captured input can influence logic or agent decisions in later nodes

#### 3.5 End Node

> Marks the **conclusion** of the workflow.
- Optionally returns a final result or status

### Variables in Workflows

> **Variables** = **shared state** across nodes. They allow outputs from one step (agent results, user input) to inform decisions or trigger further actions in subsequent steps.

---

## 4. Adding Agents to a Workflow

> Agents are the **core reasoning components** in a workflow, they enable AI-driven decision-making, classification, and response generation.

### How to Add an Agent

- Insert an **Invoke agent** node
- Reference an **existing agent** from your Foundry project, OR create a **new agent** directly in the designer
- The Invoke agent editor lets you configure: **tools, knowledge bases, memory, guardrails**

### Structured Output from Agents

> Agents can return **structured output** (e.g., JSON schema) instead of free-text. This is critical when agent output drives **control flow** (routing, conditions, variable assignment).

- Define the output schema in the **Details tab** of the Invoke agent editor
- Structured outputs ensure predictable shape for downstream nodes

### Storing Agent Output in Variables

- Configure variable storage in the **Action settings** of the Invoke agent node
- Stored output can: influence decisions, trigger conditional branches, provide input to other agents

### Modular Agent Design

> Agents can be **reused across multiple workflows**.

**Example:** A single categorization agent invoked in many workflows to classify requests; different resolution agents handle follow-up. This **separation of concerns** makes workflows easier to maintain.

---

## 5. Power Fx in Workflows

> **Power Fx** = a **low-code, Excel-like formula language** used as the "glue" of a workflow. Enables data manipulation, condition evaluation, and flow control **without writing complex code**.

**Where Power Fx is used:**
- Wherever decisions are made (If/Else nodes)
- Wherever **variables** are set (Set Variable nodes)
- Wherever **loops** are applied (For Each nodes)

### Two Types of Variables in Power Fx

| Variable Type | Description | Example |
|---|---|---|
| **System variables** | Contextual info about the workflow/conversation | **Current activity, last message, user info** |
| **Local variables** | Data captured or created during execution | `Local.Input`, `Local.Confidence`, `Local.ItemList` |

### Power Fx Formula Reference Table

| Purpose | Formula Example | Notes |
|---|---|---|
| Convert text to uppercase | `Upper(Local.Input)` | Transforms string to all caps |
| Convert text to lowercase | `Lower(Local.Input)` | Transforms string to all lowercase |
| Get string length | `Len(Local.Input)` | Returns number of characters |
| Conditional check | `Local.Confidence > 0.8` | Returns true/false; used in If/Else nodes |
| If/Else logic | `If(Local.Confidence > 0.8, "Proceed", "Escalate")` | Returns one of two values*|
| Sum a list of numbers | `Sum([10, 20, 30])` | Adds up numbers in a simple list |
| Sum a column in a table | `Sum(Local.ItemList, Amount)` | Adds up `Amount` property of each record |
| Count items | `Count(Local.ItemList)` | Returns number of items |
| Check if blank | `IsBlank(Local.Input)` | Returns true if empty |
| Check if empty table | `IsEmpty(Local.ItemList)` | Returns true if table has no records |
| Loop over items | `ForAll(Local.ItemList, Upper(Name))` | **Applies formula** to each item |
| Concatenate text | `Concatenate(Local.FirstName, " ", Local.LastName)` | Joins multiple strings |

### Key Use Cases

- **Conditions:** Check agent **confidence score** → **continue or escalate to human**
- **Loops:** Iterate over **multiple support tickets without duplicating nodes**
- **Data shaping:** Transform or extract values before passing to next node

---

## 6. Maintaining Workflows

> Building a workflow is just the first step. Maintenance ensures they remain reliable, understandable, and adaptable.

### Dual Representations: Visual + YAML

| Representation | Best For |
|---|---|
| **Visual canvas** | Conceptual understanding, tracing execution, collaboration |
| **YAML** | Advanced configuration, **version tracking, source control integration** |

> Changes in either view are **reflected in the other**, they stay in sync.

### Versioning

- Every time a workflow is **saved**, Foundry **automatically creates a new, immutable version**
- Versions allow you to: **review prior versions, compare changes, roll back** if a modification introduces errors
- Supports collaboration: track who made changes and why

### Notes (Documentation)

> Attach **notes** to nodes or sections of the workflow in the visual canvas.

- Notes provide: **context, design decisions, variable usage** explanations
- Help future maintainers understand the workflow's purpose and logic

### Best Practices for Workflow Maintenance

| Practice | Why |
|---|---|
| Regularly review for **unused/redundant nodes** | Keeps workflows lean and fast |
| Ensure **structured agent outputs** are consistently handled | Prevents downstream errors |
| Document decisions and logic with notes | Reduces errors, accelerates updates |
| **Leverage version history** to track and validate changes | Safe experimentation |

---

## 7. Using Workflows in Code

> After designing and testing a workflow in the Foundry visual designer, you can **integrate it into applications** using the **Azure AI Projects SDK**.

### Use Cases for Code Integration

| Scenario | Benefit |
|---|---|
| **Web applications** | Embed AI-driven workflows directly in user-facing apps |
| **APIs and microservices** | Expose workflow capabilities through REST endpoints |
| **Batch processing** | Invoke workflows programmatically for **bulk operations** |
| **Testing and validation** | Automate workflow testing as part of **CI/CD** pipelines |
| **Custom interfaces** | Build specialized UIs tailored to specific workflow use cases |

### How to Invoke a Workflow in Code

**Step 1:** Connect to your Foundry project using `AIProjectClient`

**Step 2:** Create a conversation context

**Step 3:** Execute the workflow by name, passing input

```python
# Reference a workflow created in the Foundry portal
workflow_name = "triage-workflow"

# Create a conversation context for the workflow
conversation = openai_client.conversations.create()

# Execute the workflow with input
stream = openai_client.responses.create(
    conversation=conversation.id,
    extra_body={"agent": {"name": workflow_name, "type": "agent_reference"}},
    input="Users can't reset their password from the mobile app.",
    stream=True,
)
```

### The `input` Parameter

The `input` can be:
- A user question for agents to analyze and respond to
- A support ticket description for classification and routing
- A data payload that triggers processing logic
- An **empty string** that simply starts the workflow without specific input

### Processing Workflow Events (Streaming)

```python
for event in stream:
    if event.type == "response.completed":
        print("Workflow completed:")
        for message in event.response.output:
            if message.content:
                for content_item in message.content:
                    if content_item.type == 'output_text':
                        print(content_item.text)
    if (event.type == "response.output_item.done") and event.item.type == ItemType.WORKFLOW_ACTION:
        print(f"Action '{event.item.action_id}' completed with status: {event.item.status}")
```

### Event Types

| Event Type | Description |
|---|---|
| `response.completed` | Workflow finished executing and returned a final response |
| `response.output_item.done` | **An individual output item** (e.g., a workflow action) completed |

### Human-in-the-Loop in Code

For workflows with **human-in-the-loop** patterns, your application may need to handle **pauses** where the workflow waits for user input. Send additional messages to the **conversation** to provide the requested input and resume execution.

---

## 8. Component Reference Summary

| Component | What It Is | Key Role |
|---|---|---|
| **Workflow** | Connected nodes orchestrating AI-driven actions | Visual, declarative execution of business logic |
| **Node** | Individual step in a workflow | Building block for actions, decisions, data, and I/O |
| **Invoke node** | Agent node in the workflow | Calls an AI agent; returns text or structured JSON |
| **Flow node** | Control flow (If/Else, Go To, For Each) | Branches, jumps, or loops through execution |
| **Data transformation node** | Variable management (Set, Reset, Parse) | Passes and shapes data between steps |
| **Basic chat node** | User communication node | Sends messages or collects user input |
| **End node** | Terminates the workflow | Optionally returns a final result |
| **Variable** | Named storage for workflow state | Shares data across nodes; drives decisions |
| **Power Fx** | **Low-code formula language** | Conditions, loops, data manipulation without complex code |
| **System variable** | Context about the workflow/conversation | Auto-provided (e.g., last message, user info) |
| **Local variable** | Custom data **created during execution** | Stores agent outputs, user input, computed values |
| **YAML** | Text representation of **workflow definition** | Version control, advanced editing, source control |
| **AIProjectClient** | SDK client for Foundry | Authenticates and invokes workflows in code |

