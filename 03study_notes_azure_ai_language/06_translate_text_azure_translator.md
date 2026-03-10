# Module: Translate Text with Azure Translator Service
## Session: Provisioning, Detection, Translation, Transliteration, Options, Custom Models

**Sources:**
- [Provision an Azure Translator Resource](https://learn.microsoft.com/en-us/training/modules/translate-text-with-translator-service/2-provision-translator-resource)
- [Understand Language Detection, Translation, and Transliteration](https://learn.microsoft.com/en-us/training/modules/translate-text-with-translator-service/3-understand-language-detection-translation-transliteration)
- [Specify Translation Options](https://learn.microsoft.com/en-us/training/modules/translate-text-with-translator-service/4-specify-translation-options)
- [Define Custom Translations](https://learn.microsoft.com/en-us/training/modules/translate-text-with-translator-service/5-define-custom-translations)

---

## 1. Azure Translator

> **Azure Translator** = a multilingual text translation API that provides **language detection**, **one-to-many translation**, and **script transliteration**.

### 3 Core Capabilities

| Capability | What It Does | Example |
|---|---|---|
| **Language Detection** | Identifies the language of input text | `"こんにちは"` → Japanese (`ja`) |
| **Translation** | Converts text from one language to **one or more** target languages simultaneously | Japanese → English + French |
| **Transliteration** | Converts text from its **native script** to an **alternative script** | `"こんにちは"` (Hiragana) → `"Kon'nichiwa"` (Latin) |

> Translation changes the **language**. Transliteration changes the **script: writing system** but keeps the same language sound.

---

## 2. Provisioning the Resource

> To use Azure Translator, provision one of the following in your Azure subscription:

| Option | Description |
|---|---|
| **Single-service Azure Translator resource** | Dedicated resource for translation only |
| **Foundry Tools (multi-service) resource** | Shared resource; Text Translation API is included |

### Authentication

After provisioning, you need:

| Value | Purpose |
|---|---|
| **Location/Region** | Where the resource is deployed |
| **Subscription Key** | API key for authentication |

### Authentication Header (All API Calls)

```
Ocp-Apim-Subscription-Key: <your-key>
Ocp-Apim-Subscription-Region: <your-region>
```

### API Base URL

```
https://api.cognitive.microsofttranslator.com
```

### 2 Ways to Call the API

| Method | Description |
|---|---|
| **REST interface** | Submit JSON requests directly |
| **SDK** | Language-specific SDK (Python, C#) abstracts the JSON |

---

## 3. Language Detection

> **Detect** function: submit text and receive the detected language code + confidence score.

### Endpoint

```
POST https://api.cognitive.microsofttranslator.com/detect?api-version=3.0
```

### Request Body

```json
[{ "Text": "こんにちは" }]
```

### Response

```json
[
  {
    "language": "ja",
    "score": 1.0,
    "isTranslationSupported": true,
    "isTransliterationSupported": true
  }
]
```

### Response Fields

| Field | Description |
|---|---|
| `language` | ISO language code of the detected language (e.g., `"ja"` for Japanese) |
| `score` | Confidence score (0.0–1.0) |
| `isTranslationSupported` | Whether translation is available for this language |
| `isTransliterationSupported` | Whether transliteration is available for this language |

---

## 4. Translation

> **Translate** function: specify one `from` language and **one or more `to` languages** to get multiple translations in a single call.

### Endpoint

```
POST https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=ja&to=en&to=fr
```

### Request Body

```json
[{ "Text": "こんにちは" }]
```

### Response (One-to-Many: Japanese → English + French)

```json
[
  {
    "translations": [
      { "text": "Hello", "to": "en" },
      { "text": "Bonjour", "to": "fr" }
    ]
  }
]
```

> A single API call with multiple `to` parameters returns all translations at once — no need to call separately per target language.

---

## 5. Transliteration

> **Transliterate** function: convert text from one **script** to another without changing the language. Use `fromScript` and `toScript` parameters.

### Endpoint

```
POST https://api.cognitive.microsofttranslator.com/transliterate?api-version=3.0&fromScript=Jpan&toScript=Latn
```

### Request Body

```json
[{ "Text": "こんにちは" }]
```

### Response

```json
[
  {
    "script": "Latn",
    "text": "Kon'nichiwa"
  }
]
```

### Translation vs Transliteration

| | Translation | Transliteration |
|---|---|---|
| **Changes** | The language | The script (writing system) |
| **Example** | `"こんにちは"` → `"Hello"` (English) | `"こんにちは"` → `"Kon'nichiwa"` (Latin script, still Japanese) |
| **Function** | `translate` | `transliterate` |
| **Parameters** | `from`, `to` | `fromScript`, `toScript` |

---

## 6. Translation Options

> The **Translate** function supports additional parameters to control output format and content.

### 6.1 Word Alignment (`includeAlignment`)

> Shows which characters in the source text correspond to which characters in the translation.

**Use case:** Useful for languages where word boundaries differ (e.g., English → Chinese).

```
&includeAlignment=true
```

**Response includes:**

```json
"alignment": {
    "proj": "0:4-0:1 6:13-2:3"
}
```

> `"0:4-0:1"` means source characters 0–4 map to translation characters 0–1.

---

### 6.2 Sentence Length (`includeSentenceLength`)

> Returns the character length of the source sentence and the translated sentence.

**Use case:** Useful for UI layout (e.g., knowing if a translated string will overflow a button).

```
&includeSentenceLength=true
```

**Response includes:**

```json
"sentLen": { "srcSentLen": [12], "transSentLen": [20] }
```

> `srcSentLen` = **source length**, `transSentLen` = **translated length** (in characters).

---

### 6.3 Profanity Filtering (`profanityAction`)

> Controls how profanities in the source text are handled in the translation.

| `profanityAction` Value | Behavior |
|---|---|
| `NoAction` | Profanities are translated as-is (default) |
| `Deleted` | Profanities are **omitted** from the translation |
| `Marked` | Profanities are **marked** using the method in `profanityMarker` |

**`profanityMarker` options (used with `Marked`):**

| `profanityMarker` Value | Behavior |
|---|---|
| `Asterisk` (default) | Replaces profanity characters with `*` |
| `Tag` | Wraps profanity in XML tags |

**Example response with `profanityAction=Marked&profanityMarker=Asterisk`:**

```json
[
  {
    "translations": [
      { "text": "JSON ist *** erstaunlich.", "to": "de" }
    ]
  }
]
```
---

## 7. Custom Translations

> **Custom Translator** = build a custom translation model trained on your own domain-specific vocabulary. Used when the default model produces incorrect or inconsistent translations for specialized terms.

**Use case examples:** Legal terminology, medical vocabulary, company-specific product names, HR system terms.

### 5-Step Setup Process

| Step | Action |
|---|---|
| **1** | Create a **workspace** in the Custom Translator portal, linked to your Azure Translator resource |
| **2** | Create a **project** |
| **3** | **Upload training data** files (source + target term pairs) and train the model |
| **4** | **Test** and **publish** the model |
| **5** | **Call the API** using the custom model's `category` parameter |

### How to Use a Custom Model in API Calls

After publishing, your custom model gets a unique **category ID**. Pass it in the `category` parameter:

```
POST https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=en&to=nl&category=<category-id>
```

**Required headers:**

```
Ocp-Apim-Subscription-Key: <your-key>
Content-Type: application/json; charset=UTF-8
```

**Request body:**

```json
[{ "Text": "Where can I find my employee details?" }]
```

**Response:**

```json
[
  {
    "translations": [
      { "text": "Waar vind ik mijn personeelsgegevens?", "to": "nl" }
    ]
  }
]
```

### Custom vs Default Translation

| Aspect | Default Model | Custom Model |
|---|---|---|
| **Training data** | General public text | Your own **domain-specific pairs** |
| **Best for** | General language translation | Industry or company-specific vocabulary |
| **How to activate** | No extra parameters | Add `category=<category-id>` to the request |
| **Portal** | N/A | **Custom Translator portal** |

---

## 8. API Functions Summary

| Function | Endpoint | Key Parameters | Purpose |
|---|---|---|---|
| **Detect** | `/detect` | *(none beyond api-version)* | Identify the language of text |
| **Translate** | `/translate` | `from`, `to` (multiple), `category`, `includeAlignment`, `includeSentenceLength`, `profanityAction` | Translate text to one or more languages |
| **Transliterate** | `/transliterate` | `fromScript`, `toScript` | Convert text script without changing language |
