# Module: Detect, Analyze, and Recognize Faces
## Session: Face Service Capabilities, Detection, Verification, Identification, and Responsible AI

**Sources:**
- [Plan a face detection, analysis, or recognition solution](https://learn.microsoft.com/en-us/training/modules/detect-analyze-recognize-faces/2-understand-capabilities-of-face-service)
- [Detect and analyze faces (Python)](https://learn.microsoft.com/en-us/training/modules/detect-analyze-recognize-faces/3-detect-analyze-faces?pivots=python)
- [Verify and identify faces](https://learn.microsoft.com/en-us/training/modules/detect-analyze-recognize-faces/4-compare-match-detected-faces)
- [Responsible AI considerations for face-based solutions](https://learn.microsoft.com/en-us/training/modules/detect-analyze-recognize-faces/5-understand-considerations-for-face-analysis)

---

## 1. What Is the Azure Face Service?

> **Azure Vision Face API** = a service providing comprehensive facial **detection**, **analysis**, and **recognition** using pre-trained models.

---

## 2. Six Core Capabilities of the Face Service

| # | Capability | What It Returns |
|---|---|---|
| **1** | **Face detection** | Face ID + **bounding box** coordinates for each detected face |
| **2** | **Face attribute analysis** | Head pose, glasses, mask, blur, exposure, noise, occlusion, accessories, quality |
| **3** | **Facial landmark location** | **Coordinates** for key points: eye corners, pupils, tip of nose, etc. |
| **4** | **Face comparison** | **Similarity** (similar features) + **Verification** (same person across images) |
| **5** | **Facial recognition** | Train a model on specific individuals; identify them in new images |
| **6** | **Facial liveness** | Detect if input video is a real stream or a spoof (anti-spoofing, spoof = tricking a system by presenting something fake) |

> **Limited Access:** Face comparison, verification, and recognition require approval via **Microsoft's Limited Access policy**.

---

## 3. Face Attribute Types

> Returned via `FaceAttributeTypeDetection01.*` (or Detection02/Recognition models).

| Attribute | Values / Notes |
|---|---|
| **Head pose** | `pitch`, `roll`, `yaw` (3D orientation in degrees) |
| **Glasses** | `No glasses`, `Reading glasses`, `Sunglasses`, `Swimming Goggles` |
| **Mask** | Presence of a face mask |
| **Blur** | `low`, `medium`, `high` |
| **Exposure** | `under exposure`, `good exposure`, `over exposure` |
| **Noise** | Visual noise level in the image |
| **Occlusion** | Whether **forehead, eyes, or mouth are obscured** |
| **Accessories** | Glasses, headwear, mask |
| **QualityForRecognition** | `low`, `medium`, `high`: image quality for recognition tasks |

---

## 4. Detection and Recognition Models

> You must explicitly select both a **detection model** and a **recognition model** when calling the API.

| Model Type | Purpose | Selection Tip |
|---|---|---|
| **Detection model** | **Locates** **faces** in the image | Newer models = better on **small** images; **may have fewer attribute options** |
| **Recognition model** |**Matches/identifies faces** across images | Choose based on recognition accuracy requirements |

> Always choose the model version that matches your **accuracy vs. breadth of attributes** trade-off.

---

## 5. Resource Provisioning

> Two resource types support the Face API.

| Resource | How Deployed |
|---|---|
| **Face** (single-service) | Standalone Face resource |
| **Foundry Tools** (multi-service) | Standalone, or as part of a Microsoft Foundry project |

**Authentication options:**
- Key-based (`AzureKeyCredential`)
- Microsoft Entra ID token authentication

---

## 6. Python SDK: Connecting to the Face Service

### Package to Install

```bash
pip install azure-ai-vision-face
```

### Create a FaceClient

```python
from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import *
from azure.core.credentials import AzureKeyCredential

face_client = FaceClient(
    endpoint="<YOUR_RESOURCE_ENDPOINT>",
    credential=AzureKeyCredential("<YOUR_RESOURCE_KEY>")
)
```

---

## 7. Detecting and Analyzing Faces (Python)

> Call `face_client.detect()` with the features, detection model, recognition model, and image data.

```python
# Specify which face attributes to return
features = [
    FaceAttributeTypeDetection01.HEAD_POSE,
    FaceAttributeTypeDetection01.OCCLUSION,
    FaceAttributeTypeDetection01.ACCESSORIES
]

# Detect faces in an image file
with open("<IMAGE_FILE_PATH>", mode="rb") as image_data:
    detected_faces = face_client.detect(
        image_content=image_data.read(),
        detection_model=FaceDetectionModel.DETECTION01,
        recognition_model=FaceRecognitionModel.RECOGNITION01,
        return_face_id=True,           # Cache face ID for 24 hours
        return_face_attributes=features,
    )
```

### Key Parameters of `face_client.detect()`

| Parameter | Description |
|---|---|
| `image_content` | **Binary** image data (read from file) |
| `detection_model` | Which detection model version to use (`DETECTION01`, etc.) |
| `recognition_model` | Which recognition model version to use (`RECOGNITION01`, etc.) |
| `return_face_id` | Whether to return and cache the face ID (valid for **24 hours**) |
| `return_face_attributes` | List of `FaceAttributeTypeDetection01.*` attributes to include |

---

## 8. The Detection Response (JSON)

> Returns an array — one object per detected face.

```json
[
    {
        "faceRectangle": {"top": 174, "left": 247, "width": 246, "height": 246},
        "faceAttributes": {
            "headPose": {"pitch": 3.7, "roll": -7.7, "yaw": -20.9},
            "accessories": [
                {"type": "glasses", "confidence": 1.0}
            ],
            "occlusion": {
                "foreheadOccluded": false,
                "eyeOccluded": false,
                "mouthOccluded": false
            }
        }
    }
]
```

### Response Fields Explained

| Field | Description |
|---|---|
| `faceRectangle` | Bounding box: `top`, `left`, `width`, `height` (pixels) |
| `faceAttributes.headPose` | `pitch`, `roll`, `yaw` in **degrees** |
| `faceAttributes.accessories[]` | Array of `{type, confidence}` objects |
| `faceAttributes.occlusion` | Boolean flags: `foreheadOccluded`, `eyeOccluded`, `mouthOccluded` |

---

## 9. Face Comparison and Verification

> Compare detected faces for **similarity** or **verify** they are the same person.

### How Face IDs Work

| Fact | Detail |
|---|---|
| **Assigned when** | A face is detected via `detect()` with `return_face_id=True` |
| **Format** | GUID: contains **no personal identity information** |
| **Cache duration** | **24 hours** |
| **Persisted faces** | When added to a Person Group for training, IDs no longer expire |

### Two Comparison Modes

| Mode | Purpose | Example Use Case |
|---|---|---|
| **Similarity** | Finds faces that share **similar facial features** | Find photos of look-alikes |
| **Verification** | Confirms same person **appears in two images** | Confirm person entered and exited a secured space |

> Verification is **anonymous**, confirms identity without knowing who the person is.

---

## 10. Facial Recognition: Training a Model

> For identifying **specific named individuals**, train a recognition model using a **Person Group**.

### 4-Step Training Process

| Step | Action |
|---|---|
| **1. Create a Person Group** | Define a set of individuals (e.g., `employees`) |
| **2. Add Persons** | Add each individual as a `Person` in the group |
| **3. Add Faces** | Add detected face images to each Person: **multiple poses recommended** |
| **4. Train the model** | Train the model; stored in your Face / Foundry Tools resource |

> Added faces become **persisted faces**: their IDs do not expire after 24 hours.

### What the Trained Model Can Do

| Task | Description |
|---|---|
| **Identify** | Recognize who a person is in a new image |
| **Verify** | Confirm a detected face matches a known persisted face |
| **Find similar** | Find new faces that resemble a known, persisted face |

---

## 11. Responsible AI for Face-Based Solutions

> Facial data is **biometric** and **personally identifiable**,extra care is required.

| Principle | Consideration |
|---|---|
| **Data privacy and security** | Facial data is **sensitive and private**: protect training data and inference results |
| **Transparency** | Inform users **how** their facial data is used and **who** has access |
| **Fairness and inclusiveness** | Ensure the system cannot be used to **discriminate** or **unfairly target** individuals based on appearance |

> See: [Data and privacy for Face](https://learn.microsoft.com/en-us/legal/cognitive-services/face/data-privacy-security)

---

## 12. Key Classes and Enums (Python SDK)

| Class / Enum | Purpose |
|---|---|
| `FaceClient` | Main client: connects to Face resource |
| `AzureKeyCredential` | Key-based authentication |
| `FaceAttributeTypeDetection01` | Enum of **attributes for Detection01 model** |
| `FaceDetectionModel` | Enum of **detection model versions** (`DETECTION01`, etc.) |
| `FaceRecognitionModel` | Enum of **recognition model versions** (`RECOGNITION01`, etc.) |

---

## Quick Reference: Exam Tips

| Key Fact | Detail |
|---|---|
| **6 Face service capabilities** | Detection, Attribute analysis, Landmark location, Comparison, Recognition, Liveness |
| **Limited Access required for** | Comparison, verification, and **recognition** features |
| **Face ID cache duration** | **24 hours** (unless added to a Person Group → then persisted) |
| **Python package** | `azure-ai-vision-face` |
| **Client class** | `FaceClient` |
| **Detect method** | `face_client.detect(image_content=..., detection_model=..., recognition_model=..., ...)` |
| **Bounding box fields** | `top`, `left`, `width`, `height` |
| **Head pose fields** | `pitch`, `roll`, `yaw` |
| **Training steps** | Person Group → Person → Add Faces (multiple poses) → Train |
| **Persisted faces** | Faces added to a Person Group: IDs do **not** expire |
| **Verification is anonymous** | Confirms same person without knowing their identity |
| **Responsible AI concerns** | Privacy/security, transparency, fairness/inclusiveness |
| **QualityForRecognition** | `low` / `medium` / `high`: image quality for recognition |
