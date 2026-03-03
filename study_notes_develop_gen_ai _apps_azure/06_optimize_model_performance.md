# Module: Choose and deploy models from the model catalog in Microsoft Foundry portal
## Session: Optimize Model Performance
**Source:** [Optimize model performance](https://learn.microsoft.com/en-us/training/modules/explore-models-azure-ai-studio/4-improve-model)

---

## 1. Overview — How to Improve Model Output

Two main layers of optimization:

| Layer | Technique | When to Use |
|---|---|---|
| **Prompt-level** | Prompt engineering | First step — always start here |
| **Model/data-level** | RAG or Fine-tuning | When prompt engineering alone is not enough |

> **Rule of thumb:** Start with prompt engineering → add RAG if context is the issue → add fine-tuning if consistency of style/format is the issue.

---

## 2. Prompt Engineering

- Requires prompts that are **relevant, specific, unambiguous, and well-structured**
- As a developer, best practice is to add instructions via a **system prompt**: sets behavior without exposing instructions to the end user

---

### 2.1 The 5 Prompt Patterns

| # | Pattern | What It Does | Example Use Case |
|---|---|---|---|
| 1 | **Persona** | Instructs the model to take a specific role/perspective | "Act as a seasoned marketing professional..." |
| 2 | **Better question suggestions** | Asks the model to suggest clarifying questions to improve the query | "What other info do you need to help me?" |
| 3 | **Output format / template** | Provides a structure the model must follow | "Format with: Date, Location, Teams, Score, Notable Events" |
| 4 | **Reflection / reasoning** | Asks the model to explain its reasoning step by step | "Explain the reasoning behind your answer" |
| 5 | **Context** | Provides specific context the model should focus on (or ignore) | "I'm visiting Edinburgh for the Six Nations rugby matches" |

---

### 2.2 Pattern Details

#### Pattern 1 — Persona

**Example:**
```
System: "You're a seasoned marketing professional that writes advertising copy
         for an audience of technical customers."
```

---

#### Pattern 2 — Better Question Suggestions
- Ask the model to suggest clarifying questions before or alongside its answer
- Helps you get more accurate, targeted responses in fewer interactions

**Example prompt addition:**
```
"What other information do you need to help me plan a great meal for my guests?"
```

---

#### Pattern 3 — Output Format / Template
- Specify the exact structure you want in the response
- Can use **one-shot** (one example) or **few-shot** (multiple examples) approach — provide sample outputs to show the model the desired pattern

**Example prompt addition:**
```
"Format the result to show: match date, location, teams, final score, notable events."
```

---

#### Pattern 4 — Reflection / Reasoning (Chain-of-Thought)
- Ask the model to explain how it arrived at its answer
- Technique name: **Chain-of-thought** — makes the model think step by step
- Useful for: **math, data analysis, troubleshooting, strategy**

**Example system prompt addition:**
```
"You always explain your answers."
```

---

#### Pattern 5 — Add Context
- Tell the model what to focus on or what to ignore
- Can connect the model to data sources it should retrieve context from before answering
- The foundation of the **RAG pattern** (see Section 3)

---

### 2.3 System Prompt vs. User Prompt

| Type | Who Sets It | Purpose |
|---|---|---|
| **System prompt** | Developer | Sets overall model behavior, persona, rules — hidden from end user |
| **User prompt** | End user | The actual question or request sent to the model |

> Best results come from combining a **strong system prompt** with guided user prompts that follow the patterns above.

---

## 3. Model Optimization Strategies (Beyond Prompt Engineering)

| Strategy | What It Does | Best For | Cost/Complexity |
|---|---|---|---|
| **RAG** (Retrieval Augmented Generation) | Retrieves **grounding context** from a data source before generating a response | Maximizing **response accuracy** — when model lacks contextual knowledge | Medium |
| **Fine-tuning** | **Extends model training** using example prompts and responses | Maximizing **consistency of behavior** — style, format, or tone | Higher |

---

### 3.1 RAG — Retrieval Augmented Generation


**When to use RAG:**
- The model needs to answer questions based on a **specific knowledge domain**
- The model needs information about **events after its training cutoff date**
- You want answers based on **your own company's documents** (e.g., expense policy)

**How it works:**
```
[User prompt]
      ↓
[Retrieve relevant context from data source]
      ↓
[Combine context + prompt]
      ↓
[Model generates grounded response]
```

---

### 3.2 Fine-Tuning



**When to use fine-tuning:**
- You need **consistent response style or format** that prompt engineering alone can't enforce
- The model's behavior is **inconsistent** despite a strong system prompt
- You have a dataset of ideal prompt→response pairs to train on

**How it works:**
- Train a base model on your dataset of example prompts + responses
- The resulting fine-tuned model produces responses consistent with those examples

---

### 3.3 Optimization Strategy Decision Guide

```
Is the model producing inaccurate or irrelevant answers?
    → Problem is CONTEXT → Use RAG

Is the model producing inconsistent style, format, or tone?
    → Problem is BEHAVIOR → Use Fine-tuning

Are responses generally good but need refinement?
    → Start with Prompt Engineering

Need maximum accuracy AND consistency?
    → Combine: Prompt Engineering + RAG + Fine-tuning
```

---

## 4. Quick Reference

### All Optimization Techniques at a Glance

| Technique | Type | Goal | Complexity |
|---|---|---|---|
| **Prompt engineering** | Prompt-level | Improve response quality via better prompts | Low |
| **System prompt** | Prompt-level | Set model behavior and persona for all interactions | Low |
| **One-shot / few-shot** | Prompt-level | Show model desired output pattern via examples | Low |
| **Chain-of-thought** | Prompt-level | Make model explain reasoning step by step | Low |
| **RAG** | Data-level | Ground model responses in external/custom data | Medium |
| **Fine-tuning** | Model-level | Train model on examples to enforce consistent style | High |

