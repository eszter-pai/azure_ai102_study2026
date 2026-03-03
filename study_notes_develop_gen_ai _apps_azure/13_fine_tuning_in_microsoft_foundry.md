# Module: Fine-tune a language model with Microsoft Foundry  
## Session: When to fine-tune, prepare data to fine-tune, explore fine-tuning in Microsoft Foundry portal  

**Sources:**
- [Understand when to fine-tune a language model](https://learn.microsoft.com/en-us/training/modules/finetune-model-copilot-ai-studio/2-understand-finetune)
- [Prepare your data to fine-tune a chat completion model](https://learn.microsoft.com/en-us/training/modules/finetune-model-copilot-ai-studio/3-prepare-data)  
- [Explore fine-tuning language models in Microsoft Foundry portal](https://learn.microsoft.com/en-us/training/modules/finetune-model-copilot-ai-studio/4-finetune-model)

---

# 1. When to Fine-Tune

> Fine-tuning is the process of taking a pretrained foundation model and training it further on your own dataset to specialize its behavior.

---

## 1.1 What Fine-Tuning Changes

- Adjusts **model weights**
- Specializes model behavior
- Makes outputs: more consistent, domain-aware, structured, aligned with a specific tone
- make the behavior **permanent** for that deployment.

---

## 1.2 When You SHOULD Fine-Tune

Use fine-tuning when you need:

| Scenario | Why Fine-Tune? |
|-----------|---------------|
| Strict structured output (JSON, schema) | Model learns the exact format |
| Consistent brand voice | Tone becomes embedded |
| Domain-specific terminology | Learns industry language |
| **Repetitive** task patterns | Learns task structure |
| Reduced prompt length | Behavior no longer needs long instructions |

---

## 1.3 When You SHOULD NOT Fine-Tune

| Scenario | Better Approach |
|----------|----------------|
| Need up-to-date knowledge | RAG |
| Need answers grounded in **private** docs | RAG |
| Small formatting change | Prompt engineering |
| Very small dataset | Prompt engineering |
| Frequently changing data | RAG |

> Fine-tuning = behavior customization  
> RAG = knowledge augmentation  

---

# 2. Preparing Data for Fine-Tuning

> **Data quality** is the MOST important factor for successful fine-tuning.

---

## 2.1 Required Data Format

- JSONL format
- no personal or sensitive info
- includes diverse set of samples

### Example JSONL Entry

```json
{"messages": 
[{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, 
{"role": "user", "content": "Is Xbox better than PlayStation?"},
{"role": "assistant", "content": "I apologize, but I cannot provide personal opinions. My primary job is to assist you with any issues related to your Xbox device. Do you have any Xbox-related issues that need addressing?"}]}
```
- can also do: multi-turn convo on a single line
- 'weight': 0 to ignore the message, 1 to inlcude in training 
```json
{"messages": 
[{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."},
{"role": "user", "content": "What's the capital of France?"}, 
{"role": "assistant", "content": "Paris", "weight": 0}, 
{"role": "user", "content": "Can you be more sarcastic?"}, 
{"role": "assistant", "content": "Paris, as if everyone doesn't know that already.", 
"weight": 1}]}
```
---

# 3. Fine-Tuning in Microsoft Foundry Portal

> In Microsoft Foundry, fine-tuning is performed through the Model Catalog and a guided configuration workflow.

---

## 3.1 Select a Base Model

- Navigate to **Model Catalog**
- Filter by **Fine-tuning task** (e.g., chat completion)
- Ensure:
  - Model supports fine-tuning
  - Model is available in your AI hub region
  - You have sufficient quota

### Evaluate Before Selecting

- Model capabilities (does it fit your task?)
- Language support
- Known limitations and biases
- Review linked model card

---

## 3.2 Configure the Fine-Tuning Job

Steps in the portal:

1. Select base model  
2. Upload/select training dataset (JSONL)  
3. (Optional) Upload validation dataset  
4. Configure advanced settings  
5. Submit job  

After submission:
- A training job is created
- You can monitor job status in the portal

---

## 3.3 Advanced Training Parameters (Exam Important)

### `batch_size`

- Number of training examples per training step
- **Larger batch** size:
  - Better for **large datasets**
  - **Fewer parameter updates**
  - **Lower variance**

---

### `learning_rate_multiplier`

- Multiplies original pretraining learning rate
- Recommended experimentation range:
  - **0.02 – 0.2**
- **Smaller values**:
  - **Reduce risk of overfitting**

---

### `n_epochs`

- **Number of full passes** through training dataset
- More epochs:
  - More learning
  - **Higher overfitting risk**

---

### `seed`

- Controls **reproducibility**
- Same seed + same parameters → usually same result
- If not specified → auto-generated

---

## 3.4 Validation Dataset

If provided:

- Used to **evaluate performance during training**
- Helps detect overfitting
- **Not used to update model weights**

---

## 3.5 Monitor Training

During training you can:

- View job status
- Review configuration parameters
- Inspect validation performance (if provided)

---

## 3.6 Deploy the Fine-Tuned Model

After training completes:

1. Deploy the fine-tuned model
2. Test via inference endpoint
3. Integrate into application (e.g., chat app)

> Deployment is required before using the model in production.