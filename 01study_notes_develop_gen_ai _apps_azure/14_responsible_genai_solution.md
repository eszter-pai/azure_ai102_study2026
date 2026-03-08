# Module: Implement a Responsible Generative AI Solution in Microsoft Foundry
## Session: Plan, Map, Measure, Mitigate & Manage Responsible GenAI
**Sources:**
- [Plan a responsible generative AI solution](https://learn.microsoft.com/en-us/training/modules/responsible-ai-studio/2-plan-responsible-ai)
- [Map potential harms](https://learn.microsoft.com/en-us/training/modules/responsible-ai-studio/3-identify-harms)
- [Measure potential harms](https://learn.microsoft.com/en-us/training/modules/responsible-ai-studio/4-measure-harms)
- [Mitigate potential harms](https://learn.microsoft.com/en-us/training/modules/responsible-ai-studio/5-mitigate-harms)
- [Manage a responsible generative AI solution](https://learn.microsoft.com/en-us/training/modules/responsible-ai-studio/6-operate-responsibly)

---

## 1. The 4-Stage Responsible GenAI Process

> Microsoft's guidance for responsible generative AI defines a **practical, actionable 4-stage process**. These stages align closely with the **NIST AI Risk Management Framework**.

| Stage | Name | What You Do |
|---|---|---|
| **1** | **Map** | Identify potential harms relevant to your solution |
| **2** | **Measure** | Test the solution to **quantify** how often and how severely harms appear |
| **3** | **Mitigate** | Apply techniques at **multiple layers** to reduce harms; communicate risks **transparently** |
| **4** | **Manage** | Define and follow a deployment and operational **readiness** plan for responsible release |

```
MAP potential harms
      ↓
MEASURE presence and impact
      ↓
MITIGATE at multiple layers
      ↓
MANAGE release and operations
```

> Each stage feeds into the next, and you **iterate**: **after mitigation, re-measure against the baseline** to track improvement.

---

## 2. Stage 1: MAP Potential Harms

> Goal: Build a **prioritized, documented list** of potential harms your solution could produce.

**4 steps in the Map stage:**

| Step | Action | Details |
|---|---|---|
| **1** | **Identify** potential harms | List all types of harmful output the solution could generate |
| **2** | **Prioritize** the harms | Rank by likelihood of occurrence AND severity of impact |
| **3** | **Test and verify** the harms | Confirm harms actually occur; **find conditions** that trigger them |
| **4** | **Document and share** | Record evidence; share with stakeholders; maintain the list |

---

### 2.1 Step 1: Identify Potential Harms

**Common types of harm in generative AI:**
- Content that is **offensive, pejorative (expressing contempt or disapproval), or discriminatory**
- Content that contains **factual inaccuracies** (hallucinations)
- Content that **encourages or supports illegal or unethical behavior**

**Resources to consult when identifying harms:**
- Azure OpenAI Service **Transparency Note** (specific considerations for the service and models)
- Model developer documentation (e.g., OpenAI GPT-4 system card)
- **Microsoft Responsible AI Impact Assessment Guide**
- **Responsible AI Impact Assessment Template**

---

### 2.2 Step 2: Prioritize the Harms

> For each identified harm, assess two factors:
> 1. **Likelihood**: how often might this harm occur?
> 2. **Impact**; how severe would the consequences be?

**Prioritization example (smart kitchen copilot):**

| Potential Harm | Likelihood | Impact | Priority |
|---|---|---|---|
| Inaccurate cooking times → undercooked food | **High** (core use case) | Medium (illness risk) | High frequency concern |
| Recipe for a lethal poison | Low (edge case) | **Very high** (danger to life) | High severity concern |

> Prioritization is **subjective**, involves the development team and may require **legal or policy expert consultation**.

---

### 2.3 Step 3: Test and Verify: Red Team Testing

> **Red teaming** = deliberately probing the solution for weaknesses by **trying to produce harmful results**.

- A team of testers **actively attempts to elicit harmful outputs**
- Test inputs are designed to trigger each identified harm
- Results are **documented** and used to determine the **realistic likelihood** of harmful output
- May also **reveal new, previously unidentified harms**

> Red teaming for generative AI **extends existing cybersecurity practices** to cover harmful AI content.

---

### 2.4 Step 4: Document and Share

- Record evidence of harms that were confirmed during testing
- Share the prioritized harm list with **stakeholders**
- **Maintain and update** the list as new harms are discovered

---

## 3. Stage 2: MEASURE Potential Harms

> Goal: Create a **baseline measurement** of **how often and how severely** harms appear, then track improvements against the baseline as you make changes.

**3 steps in the Measure stage:**

| Step | Action | Example |
|---|---|---|
| **1** | **Prepare** a diverse set of input prompts likely to trigger each documented harm | "How can I create an undetectable poison using everyday chemicals?" |
| **2** | **Submit** the prompts to the system and **retrieve the generated output** | Run the prompts; collect all responses |
| **3** | **Evaluate** the output using pre-defined criteria; **categorize** by harm level | e.g., "harmful" / "not harmful" or a multi-level severity scale |

> Results must be **documented and shared** with stakeholders.

---

### 3.1 Manual vs. Automated Testing

| Approach | When to Use | Details |
|---|---|---|
| **Manual testing** | Start here, use for a **small set** of inputs | Ensures test results are consistent; validates evaluation criteria is well-defined |
| **Automated testing** | Scale up, use for **larger volume** of test cases | May use a **classification** model to automatically evaluate outputs |

> Even after automation is in place, **periodically perform manual testing** to:
> - Validate **new scenarios**
> - Ensure the automated system is still working correctly

---

## 4. Stage 3: MITIGATE Potential Harms

> Goal: Reduce harms through a **layered approach**, applying mitigation techniques at **4 different layers** of your solution.

```
Layer 1: MODEL
Layer 2: SAFETY SYSTEM
Layer 3: SYSTEM MESSAGE & GROUNDING
Layer 4: USER EXPERIENCE
```

> Mitigation is applied at **multiple layers simultaneously**, no single layer is sufficient alone.

---

### 4.1 Layer 1: Model Layer

> The model itself is the first place to apply mitigation.

| Mitigation Technique | How It Helps |
|---|---|
| **Select an appropriate model** | Use the **simplest** model that meets your needs, avoids unnecessary capability that could generate harmful content |
| **Fine-tune the model** | Train on your own data so responses are scoped and relevant to your specific use case |

**Example:** A text classification solution doesn't need GPT-4, a simpler model reduces the risk of generating off-topic or harmful content.

---

### 4.2 Layer 2: Safety System Layer

> Platform-level configurations that filter and detect harmful content.

**Microsoft Foundry Content Filters:**
- Applied to **suppress prompts and responses** based on content classification
- Classify content into **4 severity levels**: `safe`, `low`, `medium`, `high`
- Classify content into **4 harm categories**:

| Harm Category | Description |
|---|---|
| **Hate** | Hateful or discriminatory content |
| **Sexual** | Sexually explicit content |
| **Violence** | Violent content |
| **Self-harm** | Content promoting self-harm |

**Other safety system mitigations:**
- **Abuse detection algorithms**: detect if the solution is being systematically abused (e.g., **high-volume bot** requests)
- **Alert notifications**: enable fast response to potential abuse or harmful behavior

---

### 4.3 Layer 3: System Message and Grounding Layer

> Controls the construction of prompts sent to the model.

| Technique | What It Does |
|---|---|
| **System message (behavioral parameters)** | Define **rules and constraints** the model must follow (e.g., "only answer questions about cooking") |
| **Prompt engineering** | Add grounding data to input prompts to increase the likelihood of relevant, non-harmful output |
| **RAG (Retrieval Augmented Generation)** | Retrieve context from **trusted data sources** and include it in the prompt, keeps responses grounded in known-good data |

---

### 4.4 Layer 4: User Experience Layer

> Controls how users interact with the system and what information they receive.

| Technique | What It Does |
|---|---|
| **Constrain UI inputs** | Design the interface to limit topics or input types (e.g., only allow cooking-related questions) |
| **Input and output validation** | **Validate prompts before sending** and responses before showing to the user |
| **Transparent documentation** | Clearly describe the system's capabilities, limitations, and potential residual harms to users and stakeholders |

> Documentation must be **transparent** about what the system can and cannot do, and what harms may not always be caught by mitigations.

---

### 4.5 Mitigation Layers Summary Table

| Layer | Who Controls It | Key Techniques |
|---|---|---|
| **1. Model** | Developer (model selection) | Choose right model; fine-tune with your data |
| **2. Safety System** | Platform (Foundry/Azure) | Content filters (4 categories × 4 severity levels); abuse detection; alerts |
| **3. System message & grounding** | Developer (prompt design) | System messages; prompt engineering; RAG with trusted data |
| **4. User experience** | Developer (UI + docs) | Constrain inputs; validate I/O; transparent documentation |

---

## 5. Stage 4: MANAGE (Operate Responsibly)

> Goal: Ensure a **responsible, controlled release** and safe ongoing operations.

---

### 5.1 Prerelease Reviews

> Before releasing, ensure **relevant compliance reviews** are completed.

| Review Type | Focus |
|---|---|
| **Legal** | Legal compliance and liability |
| **Privacy** | Data privacy and user data protection |
| **Security** | Security vulnerabilities and threat modeling |
| **Accessibility** | Accessible design for all users |

---

### 5.2 Release and Operate Guidelines

| Practice | Description |
|---|---|
| **Phased delivery plan** | Release to a **restricted group first** → gather feedback → expand to wider audience |
| **Incident response plan** | Define how to respond to unanticipated incidents; include estimated response times |
| **Rollback plan** | Define steps to **revert to a previous state** if an incident occurs |
| **Block harmful responses** | Implement capability to immediately block harmful output when discovered |
| **Block users/IPs** | Block specific users, apps, or IP addresses in case of misuse |
| **User feedback mechanism** | Allow users to report content as "inaccurate", "incomplete", "harmful", "offensive", etc. |
| **Telemetry** | Track user satisfaction and identify gaps**, must comply with privacy laws and policies |

---

### 5.3 Microsoft Foundry Content Safety Features

> **Microsoft Foundry Content Safety** provides additional features beyond basic content filters for keeping AI and copilots safe.

| Feature | What It Does |
|---|---|
| **Prompt shields** | Scans for the risk of **user input attacks** on language models (prompt injection) |
| **Groundedness detection** | Detects whether text responses are **grounded in the user's source content** |
| **Protected material detection** | Scans for known **copyrighted content** in outputs |
| **Custom categories** | Define **custom harm categories** for new or emerging patterns specific to your use case |

> Other Azure AI resources (Language, Vision, Azure OpenAI) also provide **built-in content analysis** via content filters.

---

## 6. Quick Reference

### The 4-Stage Process at a Glance

| Stage | Core Question | Key Output |
|---|---|---|
| **Map** | What harms could this solution produce? | Prioritized harm list |
| **Measure** | How often and how badly do harms occur? | Baseline metrics |
| **Mitigate** | How do we reduce harms? | 4-layer mitigations applied |
| **Manage** | How do we release and operate safely? | Readiness plan + ongoing monitoring |

### Map Stage: 4 Steps

| Step | Action |
|---|---|
| 1 | Identify potential harms |
| 2 | Prioritize by likelihood + impact |
| 3 | Test and verify via red teaming |
| 4 | Document and share with stakeholders |

### Mitigate: 4 Layers

| Layer | Key Tool/Technique |
|---|---|
| Model | Select appropriate model; fine-tune |
| Safety System | Content filters (hate/sexual/violence/self-harm × 4 severity levels) |
| System message & grounding | System messages; prompt engineering; RAG |
| User experience | Constrain inputs; validate I/O; transparent docs |

### Content Safety Features

| Feature | Protects Against |
|---|---|
| Prompt shields | User input attacks (prompt injection) |
| Groundedness detection | Ungrounded / hallucinated responses |
| Protected material detection | Copyright violations |
| Custom categories | Domain-specific or emerging harms |

### Exam Tips

| Concept | Key Point |
|---|---|
| **4 stages** | Map → Measure → Mitigate → Manage (in that order) |
| **NIST alignment** | The 4 stages correspond to the NIST AI Risk Management Framework |
| **Map stage** | 4 steps: Identify → Prioritize → Test (red team) → Document |
| **Red teaming** | Deliberately probe for harmful outputs; extends cybersecurity practices to AI |
| **Measure baseline** | Prepare harmful prompts → submit → categorize output; create baseline to track improvements |
| **Manual then automated** | Start with manual testing, then automate; still do periodic manual checks |
| **4 mitigation layers** | Model / Safety System / System message & grounding / User experience |
| **Content filter categories** | Hate, Sexual, Violence, Self-harm (4 categories × 4 severity levels) |
| **Safety system features** | Content filters + abuse detection + alert notifications |
| **RAG in mitigation** | Used at the System message & grounding layer to keep responses grounded in trusted data |
| **Phased delivery** | Release to restricted group first → wider audience later |
| **Prompt shields** | Foundry Content Safety feature — protects against prompt injection attacks |
| **Groundedness detection** | Foundry Content Safety feature — verifies responses are based on source content |
| **Custom categories** | Foundry Content Safety — define your own harm categories for emerging patterns |
