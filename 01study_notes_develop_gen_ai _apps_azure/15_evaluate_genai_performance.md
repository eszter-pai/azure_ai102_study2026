# Module: Evaluate GenAI Performance in Microsoft Foundry
## Session: Assess Models, Manual Evaluations & Automated Evaluations
**Sources:**
- [Assess the model performance](https://learn.microsoft.com/en-us/training/modules/evaluate-models-azure-ai-studio/2-assess-models)
- [Manually evaluate the performance of a model](https://learn.microsoft.com/en-us/training/modules/evaluate-models-azure-ai-studio/3-manual-evaluations)
- [Automated evaluations](https://learn.microsoft.com/en-us/training/modules/evaluate-models-azure-ai-studio/3b-automated-evaluations)

---

## 1. What Can Be Evaluated?

> Evaluation applies at **two levels**: an individual language model, or a complete chat flow (application).

| Level | What Is Evaluated | When to Use |
|---|---|---|
| **Individual model** | Input → model → output; optionally compared to expected output | **Early** development; comparing models before choosing one |
| **Complete chat flow** | The entire flow including all nodes (multiple models + Python code) | **Later** development; validating the full application works end-to-end |

> You typically **start by evaluating an individual model**, then eventually evaluate the complete chat flow.

---

## 2. The 4 Approaches to Evaluation

| Approach | What It Uses | Best For |
|---|---|---|
| **Model benchmarks** | Publicly available metrics **across models and datasets** | Comparing models before deployment |
| **Manual evaluations** | Human raters | Catching nuanced issues automated metrics miss (context, user satisfaction) |
| **AI-assisted metrics** | AI models to evaluate output quality and safety | Scalable quality + safety assessment |
| **NLP metrics** | Statistical overlap between generated and ground truth text | Quantifying text similarity and accuracy |

---

## 3. Model Benchmarks

> **Model benchmarks** are **publicly available metrics** that let you compare how a model performs relative to other models, before deploying it.

Available in the **Microsoft Foundry portal**, you can browse benchmark scores for all models in the catalog.

| Benchmark Metric | What It Measures |
|---|---|
| **Accuracy** | Compares generated text to the correct answer; score is 1 if exact match, 0 otherwise |
| **Coherence** | Whether the model output flows smoothly, reads naturally, and resembles **human-like** language |
| **Fluency** | How well the generated text follows **grammatical** rules, syntactic structures, and vocabulary usage |
| **GPT Similarity** | Quantifies the **semantic similarity between the ground truth and the model's prediction** |

> Use benchmarks to **narrow down model choices** before committing to deployment and testing.

---

## 4. AI-Assisted Metrics

> These metrics use AI models themselves to evaluate output, scaling evaluation beyond what humans can do manually.

| Category | Metrics Included | What It Assesses |
|---|---|---|
| **Generation quality metrics** | Coherence, relevance, creativity, style adherence | The overall quality of the generated text |
| **Risk and safety metrics** | Violence, hate, sexual content, self-harm | Whether the model generates harmful or biased content |

---

## 5. NLP Metrics

> **Natural Language Processing (NLP) metrics** measure statistical overlap between the model's generated text and the expected (ground truth) response. All require **ground truth** to compare against.

| Metric | Full Name | What It Measures |
|---|---|---|
| **F1-score** | F1 Score | Ratio of **shared words between generated and ground truth answers**, balances precision and recall |
| **BLEU** | Bilingual Evaluation Understudy | **Overlap of n-grams**; originally for machine translation |
| **METEOR** | Metric for Evaluation of Translation with Explicit Ordering | Improved **translation metric**; **considers synonyms and word order** |
| **ROUGE** | Recall-Oriented Understudy for Gisting Evaluation | Recall-focused overlap; commonly used for **summarization** tasks |

> All NLP metrics quantify the **level of overlap** between the model-generated response and the ground truth (expected response).

> **Ground truth** = a predefined expected/correct response used as the reference to compare against.

### F1-Score Formula

> F1 is the **harmonic mean of Precision and Recall** — it balances both in a single score.


```
Precision = (shared words) / (total words in generated answer)
Recall    = (shared words) / (total words in ground truth answer)

F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**Example:**
- Ground truth: *"The cat sat on the mat"* (6 words)
- Generated:    *"The cat sat on a chair"* (6 words)
- Shared words: *"The", "cat", "sat", "on"* → 4 shared words

```
Precision = 4/6 = 0.667
Recall    = 4/6 = 0.667
F1        = 2 × (0.667 × 0.667) / (0.667 + 0.667) = 0.667
```

> F1 = **0** means no overlap at all; F1 = **1** means perfect match with ground truth.

---

## 6. Manual Evaluations (Human Testing)

> Manual evaluations use **human raters** to assess model outputs. They provide insight into aspects automated metrics can miss, such as **context relevance, tone, and user satisfaction**.

Manual evaluation is valuable at **all stages** of development: (early dev: rapid iteration and experiment. production: ongoing quality assurance)


---

### 6.1 Step 1: Prepare Test Prompts

> Build a **diverse set of test prompts** before starting evaluation.

The test prompts should cover:
- **Common user questions** 
- **Edge cases**: unusual or tricky inputs
- **Potential failure points**: inputs likely to expose weaknesses

---

### 6.2 Step 2: Test in the Chat Playground

> The **Chat Playground** in the Microsoft Foundry portal lets you interactively test an individual model. (best for early dev)


---

### 6.3 Step 3: Manual Evaluations Feature (Dataset)

> When you need to evaluate **multiple prompts at once**, use the **Manual Evaluations** feature in the portal (more efficient than the chat playground for batch testing).

| Feature | Detail |
|---|---|
| **Input** | Upload a **dataset** with multiple questions (and optionally expected responses) |
| **Rating** | Rate each response with **thumbs up or thumbs down** |
| **Outcome** | Identify patterns: which prompts/scenarios perform poorly |

**Based on results, you can improve by changing:**
- The **input prompt** wording
- The **system message**
- The **model** (try a different one)
- The model's **parameters** (e.g., temperature, max tokens)

---

### 6.4 Chat Playground vs. Manual Evaluations

| | **Chat Playground** | **Manual Evaluations Feature** |
|---|---|---|
| **Scale** | One prompt at a time | Multiple prompts (dataset) at once |
| **Speed** | Slower: interactive | Faster: batch evaluation |
| **Best for** | Quick exploration; early prompt tuning | Systematic evaluation across test dataset |
| **Rating** | Subjective observation | Thumbs up / thumbs down rating |

---

## 7. Automated Evaluations

> **Automated evaluations** in the Foundry portal assess quality and content safety performance of **models, datasets, or prompt flows** at scale, without requiring human raters for each response.

---

### 7.1 Evaluation Data

> You need a **dataset of prompts and responses** to run automated evaluations. Optionally, include **expected responses (ground truth)** for NLP metrics.

**Three ways to get evaluation data:**

| Method | How |
|---|---|
| **Compile manually** | Write prompts and expected responses yourself |
| **Use existing app output** | Collect prompts and responses **from a running application** |
| **AI-generated test data** | **Use an AI model to generate a set of prompts and responses on a specific subject**; then **edit** to reflect desired outputs and use as ground truth |

> AI-generated test data is a useful **quick-start approach**: generate, edit, then evaluate.

---

### 7.2 Automated Evaluation Metrics (Evaluators)

> You select which **evaluators** to use — each calculates a different set of metrics.

| Evaluator Category | Metrics | Requires Ground Truth? |
|---|---|---|
| **AI Quality** | Coherence, Relevance (AI-assessed); F1 score, BLEU, METEOR, ROUGE (NLP, ground truth required) | Yes for NLP metrics; No for AI-assessed metrics |
| **Risk and Safety** | Violence, Hate, Sexual content, Self-harm | No |

---

### 7.3 Manual vs. Automated Evaluations

| | **Manual** | **Automated** |
|---|---|---|
| **Who evaluates** | Human raters | AI models / statistical algorithms |
| **Scale** | Limited: slow and costly at scale | Scalable: handles large datasets |
| **What it catches** | Nuanced issues: context, tone, satisfaction | Quantifiable metrics; safety issues |
| **When to use** | Early development; ongoing spot-checks | Systematic evaluation; large test sets |
| **Requires ground truth** | Optional | Required for NLP metrics |

---

## 8. Quick Reference

### All Evaluation Metrics at a Glance

| Metric | Category | What It Measures |
|---|---|---|
| **Accuracy** | Benchmark | Exact match vs. ground truth (1 or 0) |
| **Coherence** | Benchmark / AI Quality | Smooth, natural, human-like text flow |
| **Fluency** | Benchmark / AI Quality | Grammatical correctness and vocabulary usage |
| **GPT Similarity** | Benchmark | Semantic similarity to ground truth |
| **Relevance** | AI Quality | How pertinent the response is to the input |
| **F1-score** | NLP | Shared-word ratio between generated and ground truth |
| **BLEU** | NLP | N-gram overlap (originally for translation) |
| **METEOR** | NLP | Translation quality with synonym and ordering awareness |
| **ROUGE** | NLP | Recall-focused overlap (commonly for summarization) |
| **Violence / Hate / Sexual / Self-harm** | Risk & Safety | Content safety classification |

### Two Manual Evaluation Tools in Foundry

| Tool | Best For |
|---|---|
| **Chat Playground** | Quick, interactive, early-stage testing of one model |
| **Manual Evaluations feature** | Batch testing of multiple prompts with dataset upload + thumbs rating |
