# Module: Choose and deploy models from the model catalog in Microsoft Foundry portal
## Session: Deploy a Model to an Endpoint
**Source:** [Deploy a model to an endpoint](https://learn.microsoft.com/en-us/training/modules/explore-models-azure-ai-studio/3-deploy-model)

---

## 1. Why Deploy a Model?

> To use a language model in an application, you must **deploy it to an endpoint**.

**How it works in a chat application:**

```
[User asks a question]
        ↓
[API request sent to endpoint URL]
        ↓
[Endpoint routes request to the deployed model]
        ↓
[Model processes input and generates output]
        ↓
[API response returned to the app]
        ↓
[Response visualized to the user]
```

**Key terms:**

| Term | Definition |
|---|---|
| **Endpoint** | A specific URL where a deployed model or service can be accessed |
| **API** (Application Programming Interface) | The communication channel between your app and the deployed model |
| **Model deployment** | Each deployment has its own unique endpoint |

---

## 2. Deployment Options in Microsoft Foundry

> When deploying a language model in Microsoft Foundry, you choose from **three deployment types**. The options available depend on the model you want to deploy.

### 2.1 Deployment Types: standard, serverless, managed compute

| | **Standard Deployment** | **Serverless Compute** | **Managed Compute** |
|---|---|---|---|
| **Supported models** | **Microsoft Foundry models** (Azure OpenAI + Models-as-a-service) | **Foundry Models** with pay-as-you-go billing | **Open and custom** models |
| **Hosting service** | Microsoft Foundry resource | AI Project resource in a **hub** | AI Project resource in a **hub** |
| **Billing basis** | Token-based | Token-based | **Compute-based** |
| **Project type needed** | Foundry project or Hub project | Hub project only | Hub project only |
| **Recommended?** | **recommended for most scenarios** | Specific models only | Custom/open models |

---

### 2.2 Standard Deployment

- Models are hosted **within the Microsoft Foundry project resource**
- Supports **Microsoft Foundry models**, including:
  - **Azure OpenAI models**
  - **Models-as-a-service** models
- Billed by **tokens** (pay for what you use)
- **Recommended for most scenarios**

---

### 2.3 Serverless Compute

- Models are hosted on **Microsoft-managed dedicated serverless endpoints**
- Requires a **Microsoft Foundry hub project**
- Supports **Foundry Models with pay-as-you-go billing**
- Billed by **tokens**
- No infrastructure to manage: Microsoft handles it

---

### 2.4 Managed Compute

- Models are hosted in **managed virtual machine images**
- Requires a **Microsoft Foundry hub project**
- Supports **open and custom models** (e.g., open-source models you fine-tuned)
- Billed by **compute** (the VM runs whether or not you're using it)
- Gives you **more control over the hosting environment**

---

## 3. Quick Reference

### Deployment Type Decision Guide

| Scenario | Deployment Type |
|---|---|
| Most standard generative AI apps using Azure OpenAI | **Standard deployment** |
| Using a **pay-as-you-go Foundry model** with **no infra management** | **Serverless compute** |
| Deploying a custom or open-source (e.g., fine-tuned) model | **Managed compute** |

### Billing Comparison

| Deployment Type | Billing Model | Cost Pattern |
|---|---|---|
| Standard | Per token | Pay only for requests made |
| Serverless compute | Per token | Pay only for requests made |
| Managed compute | Per compute (VM) | Pay continuously **while VM is running** |

### Exam Tips

| Concept | Key Point |
|---|---|
| **Endpoint** | URL used to access a deployed model; each deployment has its own endpoint |
| **Standard deployment** | Recommended default; uses Foundry project resource; token-based |
| **Serverless compute** | Hub project required; Microsoft-managed; token-based; for Foundry pay-as-you-go models |
| **Managed compute** | Hub project required; VM-based; compute-billed; for open/custom models |
| **Hub project required** | Both serverless and managed compute deployments need a hub project |
