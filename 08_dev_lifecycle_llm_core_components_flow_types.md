# Module: Get Started with Prompt Flow in Microsoft Foundry
## Session: LLM Dev Lifecycle + Core Components + Flow Types
**Sources:**
- [Understand the LLM app development lifecycle](https://learn.microsoft.com/en-us/training/modules/get-started-prompt-flow-ai-studio/2-understand-lifecycle)
- [Understand core components and explore flow types](https://learn.microsoft.com/en-us/training/modules/get-started-prompt-flow-ai-studio/3-understand-flows)

---

## 1. What is Prompt Flow?

> **Prompt Flow** is a feature within Microsoft Foundry that lets you author **flows**:  executable **workflows for building LLM applications**. It supports **the full development lifecycle from experimentation to production**.

---

## 2. The LLM App Development Lifecycle

> Building an LLM application follows a structured 4-stage lifecycle. The process is **iterative**: you can **return to earlier stages** if the solution needs improvement.

### 2.1 The 4 Stages at a Glance

| Stage | Purpose | Key Output |
|---|---|---|
| **1. Initialization** | Define the use case and design the solution | **Objective**, sample dataset, basic prompt, flow design |
| **2. Experimentation** | Develop and test the flow against a **small** dataset | Iteratively refined flow |
| **3. Evaluation & Refinement** | Assess the flow against a **larger** dataset | Robust, reliable flow ready for production |
| **4. Production** | Deploy, optimize, and monitor the live application | Deployed endpoint + monitoring data |

> **Iterative loop:** If the flow **underperforms during Evaluation** or Production, **revert to Experimentation and refine** until satisfied.

---

### 2.2 Stage 1: Initialization

> Define everything you need before building.

**The 4 steps:**

1. Define the **objective**: what should the application do?
2. Collect a **sample dataset** : small, representative subset of expected input data
3. Build a **basic prompt**: starting point for the LLM interaction
4. Design the **flow**: **map out how inputs become outputs**

**Sample dataset guidelines:**
- Ensure **diversity** to cover **various** scenarios and **edge cases**
- Remove **privacy-sensitive information** to avoid vulnerabilities
- Keep it **small**: just enough to represent the real data

**Example:** News article classifier: decide on **output categories**, understand what **articles look like as input**, design **how the LLM produces the category label**.

---

### 2.3 Stage 2: Experimentation

> An **iterative** development loop: run, evaluate, modify, repeat.

**The 4-step loop:**

| Step | Action | Result |
|---|---|---|
| 1 | **RUN** the flow against the **sample** dataset | Output generated |
| 2 | **EVALUATE** the prompt's performance | Assessment complete |
| 3 | **Decision point** | ✓ Satisfied → proceed to **Evaluation & Refinement**<br>✗ Not satisfied → go to step 4 |
| 4 | **MODIFY** the flow (prompt or logic) | → loop back to step 1 |

---

### 2.4 Stage 3: Evaluation and Refinement

> Test against a **larger dataset** to assess real-world generalization.

- Test the flow on more data to find **bottlenecks** and **areas for optimization**
- Evaluate how well the application handles **new, unseen data**
- **Best practice:** When editing the flow, first **re-test on the small dataset** → then **re-test on the large dataset** (faster feedback loop)
- Once the flow is **robust and reliable**, move to Production

---

### 2.5 Stage 4: Production

> Deploy, optimize, and monitor the live application.

**The 3 steps in Production:**

| Step | What You Do |
|---|---|
| **Optimize** | Tune the flow for efficiency and effectiveness at scale |
| **Deploy** | Deploy the flow to an **endpoint**: calling the endpoint triggers the flow |
| **Monitor** | Collect usage data and end-user feedback to continuously improve |

> **Endpoint:** When you call the endpoint, the flow runs and generates output: same concept as model deployment endpoints (see note 05).

---

## 3. Core Components of a Flow

> A **flow** in Prompt Flow is an executable workflow with three parts:

### 3.1 Flow Structure

| Component | Description | Examples of Data Types |
|---|---|---|
| **Inputs** | Data passed into the flow | string, integer, boolean |
| **Nodes** | Tools that perform **processing, task execution, or operations** | LLM tool, Python tool, Prompt tool |
| **Outputs** | Data produced by the flow | Classified label, generated text, API result |

```
[Inputs]
    ↓
[Node 1] → [Node 2] → [Node 3]   ← nodes can chain: one node's output feeds the next
    ↓
[Outputs]
```

> A flow can have **multiple nodes**. Each node **can use the flow's global inputs or the output from any previous node** (linked together).

---

### 3.2 The 3 Node Tools

> Each node is an executable unit with a specific function. You can use **a tool multiple times** within a flow, and **combine tools** in any order.

| Tool | What It Does | Example Use |
|---|---|---|
| **LLM tool** | Creates custom prompts and calls a Large Language Model | Summarize text, classify an article, generate a response |
| **Python tool** | Executes custom Python scripts | Data transformation, API calls, custom logic |
| **Prompt tool** | Prepares and formats prompts as strings | Complex prompt construction, integration with other tools |

> Need functionality not covered by these tools? You can **create your own custom tool**.

---

## 4. The 3 Types of Flows

> You choose a flow type based on your application's purpose.

| Flow Type | Best For | Key Feature |
|---|---|---|
| **Standard flow** | General LLM-based application development | Versatile: wide range of tools available |
| **Chat flow** | Conversational applications (chatbots, assistants) | Enhanced support for chat-specific features |
| **Evaluation flow** | Assessing performance of models or other flows | Analyzes previous run results; provides feedback for improvement |

---

## 5. Quick Reference

### Lifecycle Stages Summary

| Stage | One-Line Summary |
|---|---|
| **Initialization** | Define what to build and collect sample data |
| **Experimentation** | Build and iteratively test on small data |
| **Evaluation & Refinement** | Validate on large data; fix bottlenecks |
| **Production** | Deploy to endpoint, optimize, monitor |

### Flow Type Decision Guide

| Scenario | Flow Type |
|---|---|
| Building a general text processing or classification app | **Standard flow** |
| Building a chatbot or conversational assistant | **Chat flow** |
| Measuring how well a model or flow performs | **Evaluation flow** |

### Exam Tips

| Concept | Key Point |
|---|---|
| **Prompt Flow** | Feature in Microsoft Foundry for authoring executable workflows (flows) |
| **Flow = Inputs + Nodes + Outputs** | The three structural components of every flow |
| **LLM tool** | Calls a language model with a custom prompt |
| **Python tool** | Runs custom Python code as a node |
| **Prompt tool** | Formats/prepares a prompt string for other tools |
| **Standard flow** | General purpose: most common |
| **Chat flow** | Conversational apps: has chat-specific support |
| **Evaluation flow** | Measures performance of other flows/models |
| **Lifecycle is iterative** | You can always return to Experimentation from Evaluation or Production |
| **Production = endpoint** | **Deploying a flow** means **calling an endpoint** triggers it to run |
| **Sample dataset** | Small, diverse, privacy-safe: used during Initialization and Experimentation |
| **Hub-based project required** | **Prompt Flow development requires a Hub-based project** |
