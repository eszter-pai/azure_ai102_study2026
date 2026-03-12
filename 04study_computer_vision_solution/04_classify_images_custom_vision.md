# Module: Classify Images with Azure AI Custom Vision
## Session: Provisioning, Training, and Consuming an Image Classification Model

**Sources:**
- [Provision Azure resources for Azure AI Custom Vision](https://learn.microsoft.com/en-us/training/modules/classify-images/2-provision-azure-resources-for-custom-vision)
- [Understand image classification](https://learn.microsoft.com/en-us/training/modules/classify-images/3-understand-image-classification)
- [Use a trained image classifier (Python)](https://learn.microsoft.com/en-us/training/modules/classify-images/4-use-trained-image-classifier?pivots=python)

---

## 1. What Is Azure AI Custom Vision?

> **Azure AI Custom Vision** = a service that lets you build and train your **own** computer vision models for **image classification** or **object detection**, using your own training images.

Unlike the general Azure Vision service (which uses pre-trained models), Custom Vision lets you train on **your specific data** and use cases.

---

## 2. Two Types of Custom Vision Resources

> You need **two separate resources**: one for training, one for prediction.

| Resource | Purpose | Used By |
|---|---|---|
| **Training resource** | Train a custom model using your labeled images | **Custom Vision portal / SDK** training code |
| **Prediction resource** | Generate predictions from new images using the trained model | **Client applications at runtime** |

### Key Facts

| Fact | Detail |
|---|---|
| **Separate resources** | Training and prediction are **independent** resources with their own endpoints and keys |
| **Multiple regions** | Train in one region, deploy prediction resources in **multiple other regions** |
| **Each resource has** | Its own unique **endpoint URL** + **authentication keys** |

> This separation gives flexibility, **train** once, deploy many**.

---

## 3. Custom Vision Portal

> The **Custom Vision portal** at [customvision.ai](https://www.customvision.ai/) provides a graphical UI for the full training and testing workflow.

| What You Can Do | Description |
|---|---|
| Create projects | Image classification or object detection project |
| Upload images | Add labeled training images with **class tag** |
| Review and edit | View and fix tagged images |
| Train | Train and evaluate the model |
| Test | Test predictions interactively |
| Publish | Publish trained model to a prediction resource |

> Sign in with your **Azure credentials**: projects are linked to Custom Vision resources in your subscription.

Each project has a unique **Project ID**: used **by client code for training or prediction** tasks.

---

## 4. Custom Vision SDKs

> Use the SDK for code-driven training and prediction: useful for **DevOps automation**.

| Language | Package |
|---|---|
| **Python** | `azure-cognitiveservices-vision-customvision` (PyPI) |
| **C# (.NET)** | `Microsoft.Azure.CognitiveServices.Vision.CustomVision.Training` (NuGet) |
| **C# (.NET)** | `Microsoft.Azure.CognitiveServices.Vision.CustomVision.Prediction` (NuGet) |

> The Python package handles **both** training and prediction tasks.

---

## 5. Image Classification: Two Types

> **Image classification** = a model predicts a **class label** for an image based on its content (usually the main subject).

| Type | Description | Example |
|---|---|---|
| **Multiclass classification** | Multiple classes; each image belongs to **only one** class | Apple OR Banana OR Orange |
| **Multilabel classification** | An image can be associated with **multiple labels** simultaneously | "fruit" + "red" + "round" |

---

## 6. Training Workflow (6 Steps via Portal)

> Typical workflow uses the **Custom Vision portal** for training.

| Step | Action |
|---|---|
| **1** | Create an image classification project; associate it with a **training resource** |
| **2** | Upload images and assign **class label tags** to them |
| **3** | Review and edit tagged images |
| **4** | **Train** the model; review evaluation metrics |
| **5** | **Test** the trained model interactively |
| **6** | **Publish** the trained model to a **prediction resource** |

> The REST API / SDK can automate all the same steps, useful in CI/CD pipelines.

---

## 7. Python SDK — Using a Trained Classifier

### Package to Install

```bash
pip install azure-cognitiveservices-vision-customvision
```

### Full Prediction Code Example (Python)

```python
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

# 1. Authenticate against the prediction resource
credentials = ApiKeyCredentials(
    in_headers={"Prediction-key": "<YOUR_PREDICTION_RESOURCE_KEY>"}
)
prediction_client = CustomVisionPredictionClient(
    endpoint="<YOUR_PREDICTION_RESOURCE_ENDPOINT>",
    credentials=credentials
)

# 2. Read image and submit for classification
image_data = open("<PATH_TO_IMAGE_FILE>", "rb").read()
results = prediction_client.classify_image(
    "<YOUR_PROJECT_ID>",
    "<YOUR_PUBLISHED_MODEL_NAME>",
    image_data
)

# 3. Process and filter predictions by probability threshold
for prediction in results.predictions:
    if prediction.probability > 0.5:
        print('{} ({:.0%})'.format(prediction.tag_name, prediction.probability))
```

### Key Parameters of `classify_image()`

| Parameter | Description |
|---|---|
| `project_id` | The **Project ID** from Custom Vision portal |
| `published_name` | The **published model name** set when you published the model |
| `image_data` | Binary image data (read from file with `"rb"` mode) |

### Prediction Response Fields

| Field | Description |
|---|---|
| `results.predictions` | List of all class predictions |
| `prediction.tag_name` | The class label name (e.g., `"Apple"`) |
| `prediction.probability` | Confidence score: 0.0–1.0 (filter with `> 0.5`) |

---

## 8. Authentication for Prediction (Python)

> Uses `ApiKeyCredentials` from `msrest` — different from the `AzureKeyCredential` used in other Azure Vision services.

```python
from msrest.authentication import ApiKeyCredentials

credentials = ApiKeyCredentials(
    in_headers={"Prediction-key": "<YOUR_KEY>"}
)
```

| Auth Detail | Value |
|---|---|
| **Class** | `ApiKeyCredentials` (from `msrest`) |
| **Header name** | `"Prediction-key"` |
| **Passed to** | `CustomVisionPredictionClient(endpoint=..., credentials=...)` |

---

## 9. Custom Vision vs General Azure Vision

| Aspect | Azure Vision (pre-trained) | Azure AI Custom Vision |
|---|---|---|
| **Training data** | Microsoft's large datasets | **Your own labeled images** |
| **Model type** | Fixed pre-built models | **Custom-trained** to your classes |
| **Use case** | General image analysis | Domain-specific classification |
| **Resources needed** | 1 resource (Vision) | **2 resources** (Training + Prediction) |
| **Portal** | Azure portal / Foundry portal | [customvision.ai](https://www.customvision.ai/) |
| **Python package** | `azure-ai-vision-imageanalysis` | `azure-cognitiveservices-vision-customvision` |

---

## Quick Reference — Exam Tips

| Key Fact | Detail |
|---|---|
| **Two resource types** | **Training** resource + **Prediction** resource (separate, each with own endpoint/key) |
| **Custom Vision portal** | [customvision.ai](https://www.customvision.ai/) — full GUI workflow |
| **Project ID** | Unique per project — required in all SDK calls |
| **Published model name** | Set when publishing — required in prediction calls |
| **Python package** | `azure-cognitiveservices-vision-customvision` |
| **Prediction client class** | `CustomVisionPredictionClient` |
| **Auth class** | `ApiKeyCredentials` (from `msrest`) with header `"Prediction-key"` |
| **Prediction method** | `classify_image(project_id, published_name, image_data)` |
| **Probability threshold** | Filter with `prediction.probability > 0.5` (50%) |
| **Multiclass** | One class per image |
| **Multilabel** | Multiple labels per image |
| **Training steps** | Create project → Upload + tag → Review → Train → Test → Publish |
| **SDK useful for** | Automating training/publishing in **DevOps / CI/CD** pipelines |
