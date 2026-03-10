# Module: Create Custom Text Classification Solutions
## Session: Classification Types, Evaluation Metrics, Project Lifecycle, Training, Deployment

**Sources:**
- [Understand Types of Classification Projects](https://learn.microsoft.com/en-us/training/modules/custom-text-classification/2-understand-types-of-classification-projects)
- [Understand How to Build Projects](https://learn.microsoft.com/en-us/training/modules/custom-text-classification/3-understand-how-to-build-projects)

---

## 1. What Is Custom Text Classification?

> **Custom Text Classification** = a **learned** feature of Azure Language that lets you train a model to **classify text documents into custom categories** you define, using your own labeled training data.

- Unlike pre-configured features (no training), custom text classification **requires labeling + training**
- Trained via **Language Studio** or **REST API**
- Deployed to a **REST endpoint** for client apps to query

---

## 2. Single-Label and Multi-Label Classification 

### Comparison Table

| Aspect | Single-Label Classification | Multi-Label Classification |
|---|---|---|
| **Labels per document** | Exactly **one** class per document | **One or more** classes per document |
| **API `projectKind`** | `customSingleLabelClassification` | `customMultiLabelClassification` |
| **Task kind (classify)** | `CustomSingleLabelClassification` | `CustomMultiLabelClassification` |
| **Use case example** | Classify a news article as *Politics*, *Sports*, or *Tech* | Tag a movie as *Action* AND *Comedy* |
| **Labeling strictness** | Each file gets exactly one label | Each file can have multiple labels |
---

## 3. Evaluation Metrics

> After training, the model is evaluated using three standard classification metrics: **Recall**, **Precision**, and **F1 Score**. These measure how well the model identifies correct labels.

### The 4 Outcomes (Spam Filter Example)

Think of a spam filter that looks at emails and decides: **spam** or **not spam**.

| | Model says: SPAM | Model says: NOT SPAM |
|---|---|---|
| **Actually SPAM** | **TP** — True Positive ✓ | **FN** — False Negative ✗ |
| **Actually NOT SPAM** | **FP** — False Positive ✗ | **TN** — True Negative ✓ |

| Term | Definition | Impact |
|---|---|---|
| **TP (True Positive)** | Model said spam, it **was** spam — correct catch | Good ✓ |
| **TN (True Negative)** | Model said not spam, it **wasn't** — correct pass | Good ✓ |
| **FP (False Positive)** | Model said spam, but it **wasn't** — false alarm (legit email → spam folder) | Hurts Precision |
| **FN (False Negative)** | Model said not spam, but it **was** — missed it (spam → inbox) | Hurts Recall |

### The 3 Metrics

| Metric | Formula | Plain English |
|---|---|---|
| **Precision** | `TP / (TP + FP)` | "When you cry wolf, are you right?" — of everything labeled spam, what % was actually spam? |
| **Recall** | `TP / (TP + FN)` | "Did you catch all the wolves?" — of all actual spam, what % did the model catch? |
| **F1 Score** | `2 × (Precision × Recall) / (Precision + Recall)` | Balances both — only high when **both** Precision and Recall are high |

### The Trade-Off

| Model behavior | Recall | Precision | Problem |
|---|---|---|---|
| Flags **everything** as spam | High (catches all spam) | Low | Too many false alarms |
| Only flags when **100% sure** | Low | High (never wrong) | Misses lots of spam |
| **Ideal model** | High | High | Catches spam AND doesn't flag legit emails |

> **F1 Score** is the go-to single metric. it punishes both extremes and is only high when the model is both accurate **and** thorough.

---

## 4. Project Lifecycle: 7 Steps

> Building a custom text classification model follows an **iterative 7-step lifecycle**.

```
1. Define labels
      ↓
2. Tag data (label documents)
      ↓
3. Train model
      ↓
4. View model performance (evaluate metrics)
      ↓
5. Improve model (add/fix training data)
      ↓
6. Deploy model
      ↓
7. Classify new documents
      ↓ (repeat from step 2 as needed)
```

### Step Details

| Step | Action | Where |
|---|---|---|
| **1. Define labels** | Decide the category names your model will classify into | Language Studio / project setup |
| **2. Tag data** | Assign labels to your text documents | Language Studio (manual labeling UI) |
| **3. Train** | Model learns from labeled data | Language Studio / REST API (async) |
| **4. View performance** | Review Recall, Precision, F1 for each class | Language Studio evaluation panel |
| **5. Improve** | Add more training examples, fix mislabeled data | Language Studio |
| **6. Deploy** | Publish trained model to an endpoint | Language Studio / REST API |
| **7. Classify** | Submit new text to the endpoint; receive predicted labels | REST API from client apps |

---

## 5. Training and Testing Dataset Split


### Recommended Split

| Set | Recommended Proportion | Purpose |
|---|---|---|
| **Training set** | **80%** of labeled data | Model learns from this data |
| **Testing set** | **20%** of labeled data | Model is evaluated on this data (unseen during training) |

### Two Split Methods

| Method | Description | When to Use |
|---|---|---|
| **Automatic split** | Azure randomly assigns 80% training / 20% testing | Default; quick to set up |
| **Manual split** | You explicitly assign each document to training or testing | When you need precise control over which documents are in each set |

> Using the **same data for training and testing** would give misleadingly high scores

---

## 6. Deployment

> After training, you deploy the model to a **public endpoint** for client apps to consume.

### Key Deployment Facts

| Fact | Detail |
|---|---|
| **Max deployments per project** | **10** |
| **Multiple deployments** | You can **deploy multiple versions of a model** simultaneously |
| **Deployment name** | Each deployment has a **unique name referenced in API calls** |
| **Purpose** | Allows A/B testing between model versions or maintaining separate environments (dev/staging/prod) |

---

## 7. REST API: Training (Asynchronous)

> Training is submitted via a **POST** request and is **asynchronous**. you submit the job, then poll for status.

### Step 1: Submit Training Job (POST)

```http
POST {ENDPOINT}/language/authoring/analyze-text/projects/{PROJECT-NAME}/:train?api-version={VERSION}
```

```json
{
  "modelLabel": "myModel",
  "trainingConfigVersion": "latest",
  "evaluationOptions": {
    "kind": "percentage",
    "testingSplitPercentage": 20,
    "trainingSplitPercentage": 80
  }
}
```

### Step 2: Check Training Status (GET)

```http
GET {operation-location-url}
```

> The `operation-location` URL is returned in the **response header** of the POST request.

### Status Values

| Status | Meaning |
|---|---|
| `running` | Training is still in progress |
| `succeeded` | Training completed successfully |
| `failed` | Training failed; inspect error details |

---

## 8. REST API: Classifying Text

> Once deployed, submit text for classification using the **analyze-conversations endpoint** (asynchronous).

### Classification Request Body

**Single-label:**
```json
{
  "displayName": "Classification task",
  "analysisInput": {
    "documents": [
      { "id": "1", "language": "en", "text": "Text to classify goes here." }
    ]
  },
  "tasks": [
    {
      "kind": "CustomSingleLabelClassification",
      "taskName": "MyClassificationTask",
      "parameters": {
        "projectName": "{PROJECT-NAME}",
        "deploymentName": "{DEPLOYMENT-NAME}"
      }
    }
  ]
}
```

**Multi-label**: only difference is the `kind` value:
```json
"kind": "CustomMultiLabelClassification"
```

### Classification Response

```json
{
  "tasks": {
    "items": [
      {
        "results": {
          "documents": [
            {
              "id": "1",
              "classifications": [
                { "category": "Sports", "confidenceScore": 0.92 },
                { "category": "Politics", "confidenceScore": 0.05 }
              ],
              "warnings": []
            }
          ]
        }
      }
    ]
  }
}
```

### Response Fields

| Field | Description |
|---|---|
| `category` | Predicted class label |
| `confidenceScore` | 0–1 confidence; higher = more confident this label applies |

> For **single-label**, the category with the highest `confidenceScore` is the prediction. For **multi-label**, multiple categories may be returned.

---

## 9. Single-Label vs Multi-Label — API Summary

| Aspect | Single-Label | Multi-Label |
|---|---|---|
| **`projectKind` (create project)** | `customSingleLabelClassification` | `customMultiLabelClassification` |
| **`kind` (classify task)** | `CustomSingleLabelClassification` | `CustomMultiLabelClassification` |
| **Labels returned per document** | 1 (highest confidence) | 1 or more |
| **Labeling requirement** | Exactly 1 label per training document | 1+ labels per training document |

