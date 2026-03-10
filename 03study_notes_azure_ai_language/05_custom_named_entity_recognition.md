# Module: Custom Named Entity Recognition
## Session: Custom NER vs Built-in, Labeling Data, Training, Evaluation Metrics, Confusion Matrix

**Sources:**
- [Understand Custom Named Entity Recognition](https://learn.microsoft.com/en-us/training/modules/custom-name-entity-recognition/2-understand-custom-named)
- [Label Your Data](https://learn.microsoft.com/en-us/training/modules/custom-name-entity-recognition/3-tag-your-data)
- [Train and Evaluate Your Model](https://learn.microsoft.com/en-us/training/modules/custom-name-entity-recognition/4-train-evaluate-your-model)

---

## 1. What Is Custom NER?

> **Custom NER** = an Azure Language feature that lets you train a model to **identify and extract user-defined entities** from unstructured text, entities specific to your domain that the built-in service doesn't cover.

- Part of **Azure Language** in Foundry Tools
- Requires: **define entities → label data → train → deploy → extract**
- Used for: legal documents, bank statements, audit policies, catalog search, knowledge mining

---

## 2. Custom NER vs Built-in NER

> Both extract named entities from text, but they solve **different problems**.

| Aspect | Built-in NER | Custom NER |
|---|---|---|
| **Training required** | No,  pre-configured | Yes,  label + train |
| **Entity types** | General types (**Person, Location, DateTime, URL**, etc.) | **You define** the entity types |
| **Configuration** | Minimal | Full project setup in Language Studio |
| **Use case** | Find locations, names, URLs in generic text | Extract specific domain entities (e.g., loan amount, account number, contract clause) |
| **API endpoint** | `{ENDPOINT}/language/analyze-text/jobs` | Custom endpoint via project + deployment name |
| **Task kind** | Built-in NER call | `CustomEntityRecognition` |

### When to Use Custom NER

| Scenario | Use Custom NER? |
|---|---|
| Extract city names from travel reviews | use built-in NER (Location) |
| Extract loan amount and account number from bank statements | **Yes** |
| Extract contract clause types from legal documents | **Yes** |
| Find URLs in support tickets | built-in NER (URL) |

---

## 3. Built-in NER: Response Example

```json
"entities": [
    {
        "text": "Seattle",
        "category": "Location",
        "subcategory": "GPE",
        "offset": 45,
        "length": 7,
        "confidenceScore": 0.99
    },
    {
        "text": "next week",
        "category": "DateTime",
        "subcategory": "DateRange",
        "offset": 104,
        "length": 9,
        "confidenceScore": 0.8
    }
]
```

---

## 4. Project Lifecycle: 7 Steps

> Building a custom NER model follows an **iterative 7-step lifecycle** (same pattern as custom text classification).

```
1. Define entities
      ↓
2. Tag (label) data
      ↓
3. Train model
      ↓
4. View model performance
      ↓
5. Improve model
      ↓
6. Deploy model
      ↓
7. Extract entities (query endpoint)
      ↓ (repeat from step 2 as needed)
```

### Step Details

| Step | Action | Notes |
|---|---|---|
| **1. Define entities** | Name and describe the entities you want to extract | Make them as **clear and distinct** as possible |
| **2. Tag data** | Label text spans in your documents with the correct entity | Must be **consistent, precise, and complete** |
| **3. Train** | Model learns from labeled data | Async via Language Studio or REST API |
| **4. View** | Review Precision / Recall / F1 scores **per entity** | Use the **View model details** page in Language Studio |
| **5. Improve** | Add more examples, fix mislabeled data | Focus on entities with low scores |
| **6. Deploy** | Publish model to a named deployment endpoint | Max 10 deployments per project |
| **7. Extract** | Submit text via REST API; receive extracted entities | Uses `CustomEntityRecognition` task kind |

---

## 5. Data Quality Guidelines

> The quality of your training data directly determines the quality of your model.

| Principle | Rule |
|---|---|
| **Diversity** | Use data from **as many sources as possible**, like different formats, styles, and number of entities per document |
| **Distribution** | Match the **real-world distribution** of document types expected in production |
| **Accuracy** | Use data **as close to real-world data as possible** — fake/synthetic data may not generalize |

### Entity Design Tips

| Tip | Why It Matters |
|---|---|
| Define entities **as distinctly as possible** | Ambiguous entities confuse the model |
| Avoid overly broad entities (e.g., "Contact info") | Break into specific sub-types: Phone, Email, Social media |
| Avoid placing two ambiguous entity spans next to each other | The model struggles to differentiate adjacent entities |
| Add **more examples for ambiguous entity pairs** | More training examples help the model learn the difference |

---

## 6. Labeling Data: 3 Core Principles

> Labeling (tagging) is done in **Language Studio**, select the text span and assign the entity type.

| Principle | Rule |
|---|---|
| **Consistency** | Label the same entity type the same way across **all documents**, no conflicting labels |
| **Precision** | Label **only the exact text** that is the entity|
| **Completeness** | Label **every instance** of the entity in every document |

### How Labels Are Stored

- Language Studio saves labels as an **auto-generated JSON file** in your **Azure Storage container**
- You can also **import** a pre-made label file (e.g., migrating labels from another project)

### Label File Format (JSON)

```json
{
  "projectFileVersion": "{DATE}",
  "stringIndexType": "Utf16CodeUnit",
  "metadata": {
    "projectKind": "CustomEntityRecognition",
    "storageInputContainerName": "{CONTAINER-NAME}",
    "projectName": "{PROJECT-NAME}",
    "multilingual": false,
    "language": "en-us"
  },
  "assets": {
    "projectKind": "CustomEntityRecognition",
    "entities": [
      { "category": "Entity1" },
      { "category": "Entity2" }
    ],
    "documents": [
      {
        "location": "{DOCUMENT-NAME}",
        "language": "{LANGUAGE-CODE}",
        "dataset": "{DATASET}",
        "entities": [
          {
            "regionOffset": 0,
            "regionLength": 500,
            "labels": [
              { "category": "Entity1", "offset": 25, "length": 10 },
              { "category": "Entity2", "offset": 120, "length": 8 }
            ]
          }
        ]
      }
    ]
  }
}
```

### Label File Key Fields

| Field | Description |
|---|---|
| `projectKind` | Always `CustomEntityRecognition` for custom NER |
| `entities` | List of all entity types defined for the project |
| `documents` | Array of labeled documents |
| `location` | File path within the storage container |
| `dataset` | Which split the file belongs to (training or testing) |
| `regionOffset` | Inclusive character position where the text region starts |
| `regionLength` | Length (in characters) of the region used in training |
| `labels` | Array of labeled entity spans within the region |
| `offset` | Character position where the entity starts |
| `length` | Number of characters in the entity |

---

## 7. Evaluation Metrics

> After training, view scores in the **View model details** page. Scores are available **per entity** and for the **model as a whole**.

### The 3 Metrics

| Metric | Formula | What It Measures |
|---|---|---|
| **Precision** | `TP / (TP + FP)` | Of all entities the model **extracted**, how many were **correct**? |
| **Recall** | `TP / (TP + FN)` | Of all **actual** entities in the document, how many did the model **find**? |
| **F1 Score** | `2 × (Precision × Recall) / (Precision + Recall)` | Single score balancing both Precision and Recall |

### Interpreting Score Combinations

| Precision | Recall | Meaning | What to Do |
|---|---|---|---|
| **Low** | **Low** | Model struggles to find entities AND mislabels what it finds | Major issues, add more diverse training data |
| **Low** | **High** | Model finds entities well but **labels them as the wrong type** | Fix **entity definitions**; add more distinguishing examples |
| **High** | **Low** | Model labels correctly **when it finds entities**, but **misses many** | **Add more training examples for missed entities** |
| **High** | **High** | Model finds entities AND labels them correctly | Ideal |

---

## 8. Confusion Matrix

> The **Confusion Matrix** tab (same "View model details" page) provides a visual table of all entities and how each one performed.

- Shows which entities were **correctly identified**, **missed**, or **confused with another entity type**
- Helps you pinpoint **exactly which entities** need more training data or clearer definitions
- Useful for **spotting patterns: e.g., "Entity A keeps getting labeled as Entity B"**

---

## 9. REST API: Extract Entities

> Extraction is submitted via a **POST** request (asynchronous).

### Request Body

```json
{
    "displayName": "MyExtractionTask",
    "analysisInput": {
        "documents": [
            { "id": "doc1", "text": "Text of first document goes here." },
            { "id": "doc2", "text": "Text of second document goes here." }
        ]
    },
    "tasks": [
        {
            "kind": "CustomEntityRecognition",
            "taskName": "MyRecognitionTaskName",
            "parameters": {
                "projectName": "{PROJECT-NAME}",
                "deploymentName": "{DEPLOYMENT-NAME}"
            }
        }
    ]
}
```

### Key Request Fields

| Field | Description |
|---|---|
| `kind` | Always `CustomEntityRecognition` for custom NER |
| `projectName` | Name of your custom NER project |
| `deploymentName` | Name of the specific deployment to use |

---

## 10. Project Limits

| Limit | Value |
|---|---|
| **Minimum training files** | 10 |
| **Maximum training files** | 100,000 |
| **Max deployments per project** | 10 |
| **Max projects per resource** | 500 |
| **Max trained models per project** | 50 |
| **Max entity types per project** | 200 |
| **Max characters per entity** | 500 |
| **Max storage accounts per project** | 1 |
| **Authoring API rate limit** | 10 POST / 100 GET per minute |
| **Analyze API rate limit** | 20 GET or POST |

