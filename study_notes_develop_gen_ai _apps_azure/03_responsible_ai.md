# Module: Plan and prepare to develop AI solution on Azure
## Session: Responsible AI
**Source:** [Responsible AI](https://learn.microsoft.com/en-us/training/modules/prepare-azure-ai-development/6-responsible-ai)

---

## 1. Why Responsible AI Matters

> Software engineers must consider the impact of their software on users and society, especially when AI is involved, because:

- AI systems often make decisions based on **probabilistic models** trained on data
- The **human-like nature** of AI builds user trust, which raises the stakes when it gets things wrong
- Incorrect predictions or misuse can cause **harm to individuals or groups**
- AI systems can introduce or amplify **bias, unfairness, and discrimination**

**Developer responsibility:** Apply due consideration to mitigate risks and ensure fairness, reliability, and adequate protection from harm.

---

## 2. Microsoft's 6 Principles of Responsible AI

| # | Principle | Core Idea |
|---|---|---|
| 1 | **Fairness** | AI must treat all people equally, without bias |
| 2 | **Reliability & Safety** | AI must work correctly and safely, **especially in high-stakes scenarios** |
| 3 | **Privacy & Security** | AI must protect personal data and secure systems |
| 4 | **Inclusiveness** | AI must **empower and benefit everyone** in society |
| 5 | **Transparency** | AI must be understandable and its limitations communicated |
| 6 | **Accountability** | People must be responsible for AI systems and their outcomes |

---

### 2.1 Fairness

> AI systems should **treat all people fairly**.

- **Problem:** A loan approval ML model might unintentionally discriminate based on gender or ethnicity
- **Risk:** Unfair advantage or disadvantage to specific groups
- **Actions to take:**
  - **Review training data** to ensure it is **representative** of all potentially affected subjects
  - Evaluate predictive performance **per subgroup** throughout the development lifecycle
  - Use software tools to **evaluate, quantify, and mitigate unfairness** in models
  - Consider fairness **from the very beginning**

> Note: Fairness tooling alone is not sufficient — it requires deliberate design choices.

---

### 2.2 Reliability and Safety

> AI systems should **perform reliably and safely**.

- **Problem:** An AI system for autonomous vehicles or medical diagnosis could risk human life if unreliable
- **Actions to take:**
  - Subject AI software to **rigorous testing and deployment management** before release
  - Account for the **probabilistic nature** of ML models
  - Apply appropriate **confidence score thresholds** when evaluating predictions

---

### 2.3 Privacy and Security

> AI systems should be **secure and respect privacy**.

- **Problem:** ML models are trained on large volumes of data, often containing **personal details**
- Risk exists both during training **and** in production (new data used for predictions)
- **Actions to take:**
  - Implement **appropriate safeguards** to protect data and customer content
  - Ensure personal data used in training stays private
  - Protect live prediction data **from unauthorized access**

---

### 2.4 Inclusiveness

> AI systems should **empower everyone** and engage all people.

- AI should benefit **all parts of society** regardless of:
  - Physical ability
  - Gender
  - Sexual orientation
  - Ethnicity
  - Other factors
- **Actions to take:**
  - Include **input from a diverse group of people** in design, development, and testing

---

### 2.5 Transparency

> AI systems should be **understandable**.

- Users must be made aware of:
  - The **purpose** of the system
  - **How it works**
  - **Limitations** and factors that may affect accuracy
- **What to share with users:**
  - **Number of cases** used to train the model
  - **Which features** have the most influence over predictions
  - **Confidence scores** for predictions
  - How personal data is **used, retained**, and who has **access** to it (e.g., facial recognition systems)

---

### 2.6 Accountability

> **People should be accountable** for AI systems.

- Even autonomous-seeming AI systems ultimately **have humans responsible** for them
- Accountability belongs to:
  - **Developers** who trained and validated the models
  - **Designers** who defined the decision logic
- **Actions to take:**
  - Work within a framework of **governance and organizational principles**
  - Ensure solutions meet **responsible and legal standards**
  - Standards must be **clearly defined** before development begins

---

## 3. Quick Reference

### The 6 Principles at a Glance

| Principle | Key Question to Ask | Example Risk if Ignored |
|---|---|---|
| **Fairness** | Does the model treat all groups equally? | Loan model denies applications based on ethnicity |
| **Reliability & Safety** | Has it been **rigorously** tested? | Autonomous vehicle AI **fails in an edge case** |
| **Privacy & Security** | Is personal data protected? | Training data leaks sensitive medical records |
| **Inclusiveness** | Does it work for everyone? | App only works well for one demographic group |
| **Transparency** | Do users understand how it works? | Users don't know AI is making decisions about them |
| **Accountability** | Is someone responsible for outcomes? | No one owns the consequences of a bad AI decision |

### Exam Tip — Matching Scenarios to Principles

| Scenario | Principle |
|---|---|
| A credit model penalizes a protected demographic | **Fairness** |
| An AI medical system gives wrong drug dosages | **Reliability & Safety** |
| User images are stored without consent | **Privacy & Security** |
| An app doesn't support screen readers | **Inclusiveness** |
| Users don't know an AI is making decisions | **Transparency** |
| No one is defined as responsible when AI causes harm | **Accountability** |