# Module: Get Started with AI Agent Development on Azure
## Session: Introduction to AI Agents, Concepts, Capabilities & Security
**Sources:**
- [Introduction](https://learn.microsoft.com/en-us/training/modules/ai-agent-fundamentals/1-introduction)
- [What are AI agents?](https://learn.microsoft.com/en-us/training/modules/ai-agent-fundamentals/2-what-are-agents)

---

## 1. What Is an AI Agent?

> An **AI agent** is a smart application that uses a **language model** to understand what a user needs and then **takes action** to help, autonomously.

**Key difference between a chatbot and an AI agent:**

| | **Chatbot** | **AI Agent** |
|---|---|---|
| **Primary function** | Answer questions via conversation | Understand AND **take action** |
| **Memory** | Often stateless | **Remembers the conversation** |
| **Autonomy** | only responds | **can do things independently** |
| **Examples** | FAQ bots, customer service chat | Expense filing, travel booking, process automation (execute tasks, call functions, access data, and complete workflows automatically.) |


---

## 2. The 3 Core Components of an AI Agent

> Every AI agent is built from three essential components:

```
[AI Agent]
    ├── [Language Model]   ← understands intent + generates responses
    ├── [Instructions]     ← defines the agent's purpose, scope, and behavior rules
    └── [Tools]            ← functions/APIs the agent can call to take action
```

| Component | What It Does |
|---|---|
| **Language model** | Processes prompts, reasons about them, and generates intelligent responses |
| **Instructions** | Defines what the agent is for, what it can/cannot do, and how it should behave |
| **Tools** | Programmatic **functions, APIs, or data sources the agent** can invoke to complete tasks |

---

## 3. Single-Agent Scenario: Expense Management Agent

> A single agent handles tasks **within one domain**. Example: an **expense management agent** that helps employees **with expense claims**.

### 3.1 Three Essential Capabilities

| Capability | What It Does | In the Expense Agent Example |
|---|---|---|
| **Knowledge integration & reasoning** | Combines **a generative model with domain documentation** to answer questions accurately | Uses corporate expenses policy documentation to answer "what can I claim?" |
| **Task automation through functions** | Executes programmatic functions to complete tasks automatically | Submits monthly recurring expense claims (e.g., cellphone bills) automatically |
| **Intelligent decision-making** | Applies **business rules** to route or process actions correctly | Routes expense claims to the appropriate approver based on claim amount |

---

### 3.2 Expense Agent

| Step | What Happens |
|---|---|
| **1. User question** | Employee asks about expense limits or submits a claim request |
| **2. Accept as prompt** | The agent receives the input as a prompt to process |
| **3. Ground the prompt** | Knowledge store (policy docs) provides factual context(prevents hallucination) |
| **4. Generate response** | Grounded prompt sent to language model → accurate, policy-based answer |
| **5. Submit claim** | Agent programmatically generates and submits the expense claim for processing |

---

## 4. Multi-Agent Scenario: Travel Booking + Expense Agent

> **Multi-agent solutions** involve multiple agents that **coordinate work between themselves**, each specializing in a different domain.

### 4.1 Travel Agent Capabilities

| Capability | What It Does |
|---|---|
| **Service integration** | Books flights and hotels through external travel service APIs |
| **Cross-agent communication** | Initiates expense claims through the expense agent with appropriate receipts |
| **End-to-end automation** | Completes **the full travel booking** AND **expense submission workflow** without manual intervention |

---

### 4.2 Multi-Agent Process (4-Step Flow)

```
1. User gives trip details to the TRAVEL BOOKING AGENT
         ↓
2. Travel agent AUTOMATES the booking of flights + hotel reservations
         ↓
3. Travel agent INITIATES an expense claim for travel costs (via the EXPENSE AGENT)
         ↓
4. Expense agent SUBMITS the expense claim for processing
```
---

## 5. Security Risks of AI Agents

> As agents become more autonomous and integrated into enterprise systems, they introduce **new security risks** beyond traditional application threats. Because agents can access sensitive data, make decisions, and act independently, **security must be designed in from the start**.

| Risk Area | What's Happening | Example |
|---|---|---|
| **Data leakage & privacy exposure** | Agent accesses sensitive data but lacks controls to prevent external exposure | Agent shares confidential salary data in a customer chat |
| **Prompt injection & manipulation** | **Malicious user crafts input** that overrides the agent's intended behavior | User tricks agent into revealing a database password |
| **Unauthorized access & privilege escalation** | Weak access controls allow the agent **to perform actions beyond its intended scope** | Support agent starts deleting customer records it shouldn't have access to |
| **Data poisoning** | Someone corrupts the agent's training or contextual data → unsafe outputs | Agent **recommends fraudulent products** after training data is corrupted |
| **Supply chain vulnerabilities** | **External plugins or APIs** introduce **security vulnerabilities** | Third-party plugin sends organizational data to an unknown server |
| **Over-reliance on autonomous actions** | Agent executes high-stakes actions **without validation or human oversight** | Agent automatically processes a refund without verifying the request |
| **Inadequate auditability & logging** | Missing logs make it impossible to **trace agent actions or detect misuse** | Cannot determine who accessed what data or when |
| **Model inversion & output leakage** | Attacker exploits model outputs to **infer sensitive data from training or prompts** | Attacker extracts customer data by repeatedly querying the agent |

---

## 6. Security Best Practices for AI Agents

> Adopt a **security-by-design** approach from day one to deploy agents safely.

| Practice | What It Means |
|---|---|
| **Control access tightly** | Enforce **RBAC (Role-Based Access Control)** and **least privilege**: agents only access what they absolutely need |
| **Validate all inputs** | Add **prompt filtering and validation** layers to catch and block injection attacks before they reach the agent |
| **Add human oversight for critical actions** | Gate sensitive operations behind **human-in-the-loop approvals**, don't let agents make high-stakes decisions alone |
| **Track everything** | Maintain **comprehensive logging and traceability** for all agent actions, know who did what, when, and why |
| **Monitor your supply chain** | Audit **third-party dependencies** and integrations regularly, external plugins and APIs can be attack vectors |
| **Keep your models healthy** | Continuously retrain and validate models to detect **data drift** or **poisoning attempts**, agent quality degrades without maintenance |

---

## 7. Quick Reference

### 3 Core Agent Components

| Component | Role |
|---|---|
| Language model | Understands + generates |
| Instructions | Defines purpose + constraints |
| Tools | Enables taking action |

### Single vs. Multi-Agent

| | Single-Agent | Multi-Agent |
|---|---|---|
| **Scope** | One domain | Multiple domains |
| **Coordination** | Self-contained | Agents communicate with each other |
| **Example** | Expense agent (handles policy Q&A + claim submission) | Travel agent + Expense agent (full booking + filing workflow) |

### Exam Tips

| Concept | Key Point |
|---|---|
| **AI agent definition** | Smart app using a language model to understand + **take action** autonomously |
| **Agent vs chatbot** | Agents remember conversation and can **actually do things** — not just chat |
| **3 agent components** | Language model + Instructions + Tools |
| **Tools** | Programmatic functions/APIs the agent invokes to take action |
| **Grounding in agents** | Agent uses a knowledge store to ground prompts — ensures factual, policy-based responses (same RAG pattern as note 10) |
| **Multi-agent** | Multiple specialized agents that coordinate — each handles its own domain |
| **Cross-agent communication** | Agents can initiate requests to other agents (e.g., travel agent → expense agent) |
| **Security-by-design** | Must be built in from the start — not added later |
| **Least privilege** | Agents should only access what they absolutely need — minimize blast radius |
| **Human-in-the-loop** | High-stakes agent actions should require human approval |
| **Prompt injection** | Malicious input that overrides agent's intended behavior — mitigated by input validation |
| **Data poisoning** | Corrupting training/context data → unsafe outputs — mitigated by model monitoring |
| **Logging & traceability** | Required for auditability — track all agent actions |
