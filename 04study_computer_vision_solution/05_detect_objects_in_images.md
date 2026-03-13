# Module: Detect Objects in Images
## Session: Object Detection with Azure AI Custom Vision, Training and Prediction

**Sources:**
- [Use Azure AI Custom Vision for object detection](https://learn.microsoft.com/en-us/training/modules/detect-objects-images/2-understand-object-detection)
- [Train an object detector](https://learn.microsoft.com/en-us/training/modules/detect-objects-images/3-train-object-detector)
- [Develop an object detection client application (Python)](https://learn.microsoft.com/en-us/training/modules/detect-objects-images/4-use-trained-detector?pivots=python)

---

## 1. Object Detection vs Image Classification

| Aspect | Image Classification | Object Detection |
|---|---|---|
| **Question answered** | "What is in this image?" | "What is in this image, and **where** is it?" |
| **Output** | Class label (one or more tags) | Class label **+** **bounding box** for each object |
| **Multiple objects** | Whole-image label only | Each object labeled separately with its own region |
| **Labeling** | Tags apply to the **whole image** | Tags apply to a **region** (bounding box) per object |

---

## 2. Two Components of an Object Detection Prediction

> Every detected object returns **two pieces of information**.

| Component | Description | Example |
|---|---|---|
| **Class label** | What object was detected | `"apple"`, `"banana"`, `"orange"` |
| **Bounding box** | Where in the image the object is located | `left: 0.1, top: 0.5, width: 0.5, height: 0.25` |

---

## 3. Resources Required (Same as Image Classification)

> Object detection also needs **two separate Custom Vision resources**.

| Resource | Purpose |
|---|---|
| **Training resource** | Train the model using your labeled images |
| **Prediction resource** | Generate predictions in client applications |

| Fact | Detail |
|---|---|
| **Separate resources** | Each has its own endpoint + authentication keys |
| **Flexible deployment** | Train in one region; deploy prediction in multiple regions |
| **Portal** | [customvision.ai](https://www.customvision.ai/) |
| **Project ID** | Unique per project, required in SDK calls |

---

## 4. Bounding Box Coordinate Format

> Bounding box values are **proportional** (relative to image size) — not pixel values.

| Value | Meaning | Example (0.1) |
|---|---|---|
| `left` | **X** position of the box's **left edge** from the left of the image | 1/10 from the left edge |
| `top` | **Y** position of the box's **top edge** from the top of the image | 1/2 (halfway down) |
| `width` | Width of the box **as a fraction** of the total image width | Half the image width |
| `height` | Height of the box **as a fraction** of the total image height | Quarter of image height |

### Example

```
Left: 0.1   → starts 10% from the left
Top:  0.5   → starts 50% from the top
Width: 0.5  → spans 50% of the image width
Height: 0.25 → spans 25% of the image height
```

> If using a **third-party labeling tool**, you may need to **convert its output to this proportional format** before uploading to Custom Vision.

---

## 5. Image Labeling for Object Detection

> The key difference from classification: each label has a **tag + a bounding box region** (not just a tag).

### Labeling Options

| Method | Description | Best For |
|---|---|---|
| **Custom Vision portal** (recommended) | Interactive GUI (graphic user interface): auto-suggests regions; drag to adjust | Most users |
| **Smart labeler** | After initial training, suggests **both regions and class names** | Speeds up subsequent labeling |
| **Third-party / custom tool** | Full control; can assign tasks to **multiple team members** | Large teams / specialized workflows |

### Smart Labeler Workflow

1. Upload and manually label a first batch of images
2. Train an initial model
3. Use the **smart labeler** on new images: it suggests regions + class labels automatically

---

## 6. Training Workflow (Same Pattern as Classification)

| Step | Action |
|---|---|
| **1** | Create an object detection project; associate with a **training resource** |
| **2** | Upload images and label each object with a **tag + bounding box region** |
| **3** | Review and edit labeled regions |
| **4** | **Train** the model; review evaluation metrics |
| **5** | **Test** the trained model |
| **6** | **Publish** the trained model to a **prediction resource** |

---

## 7. Python SDK: Using a Trained Object Detector

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

# 2. Read image and submit for object detection
image_data = open("<PATH_TO_IMAGE_FILE>", "rb").read()
results = prediction_client.detect_image(
    "<YOUR_PROJECT_ID>",
    "<YOUR_PUBLISHED_MODEL_NAME>",
    image_data
)

# 3. Process predictions — filter by probability threshold
for prediction in results.predictions:
    if prediction.probability > 0.5:
        left   = prediction.bounding_box.left
        top    = prediction.bounding_box.top
        height = prediction.bounding_box.height
        width  = prediction.bounding_box.width
        print(f"{prediction.tag_name} ({prediction.probability:.0%})")
        print(f"  Left:{left}, Top:{top}, Height:{height}, Width:{width}")
```

### Key Differences: `detect_image()` vs `classify_image()`

| Aspect | Image Classification | Object Detection |
|---|---|---|
| **Method** | `classify_image()` | **`detect_image()`** |
| **Extra response fields** | `tag_name`, `probability` | `tag_name`, `probability` + **`bounding_box`** |

### Bounding Box Fields in the Response

| Field | Description |
|---|---|
| `prediction.bounding_box.left` | Left edge (proportional, 0.0–1.0) |
| `prediction.bounding_box.top` | Top edge (proportional, 0.0–1.0) |
| `prediction.bounding_box.width` | Width (proportional, 0.0–1.0) |
| `prediction.bounding_box.height` | Height (proportional, 0.0–1.0) |

### Prediction Response Fields

| Field | Description |
|---|---|
| `prediction.tag_name` | Detected object class label |
| `prediction.probability` | Confidence score: 0.0–1.0 |
| `prediction.bounding_box` | Object's location as proportional coordinates |

---

## 8. Authentication (Same as Image Classification)

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

---

## 9. Object Detection vs Classification (SDK Comparison)

| Aspect | Image Classification | Object Detection |
|---|---|---|
| **Predict method** | `classify_image(project_id, model_name, data)` | `detect_image(project_id, model_name, data)` |
| **Returns** | `tag_name` + `probability` | `tag_name` + `probability` + `bounding_box` |
| **Bounding box** | Not returned | `left`, `top`, `width`, `height` (proportional) |
| **Labeling** | Tag per whole image | Tag + region per object |
| **Smart labeler** | Not applicable | Suggests regions + class names after initial training |

---

## Quick Reference — Exam Tips

| Key Fact | Detail |
|---|---|
| **Two prediction components** | Class label + **bounding box** (location) |
| **Two resources needed** | Training resource + Prediction resource |
| **Bounding box values** | **Proportional** (0.0–1.0), not pixels: `left`, `top`, `width`, `height` |
| **Python package** | `azure-cognitiveservices-vision-customvision` (same as classification) |
| **Prediction method** | `detect_image()` (vs `classify_image()` for classification) |
| **Auth class** | `ApiKeyCredentials` from `msrest` with header `"Prediction-key"` |
| **Probability threshold** | Filter with `prediction.probability > 0.5` |
| **Labeling difference** | Object detection labels = tag **+ bounding box region** (not just tag) |
| **Smart labeler** | Suggests regions + class names after an initial model is trained |
| **Third-party labeling tools** | Must convert output to **proportional** format for the Custom Vision API |
| **Project ID** | Required in all prediction SDK calls |
| **Portal URL** | [customvision.ai](https://www.customvision.ai/) |
