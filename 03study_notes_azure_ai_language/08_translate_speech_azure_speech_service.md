# Module: Translate Speech with the Azure Speech Service
## Session: Provisioning, Speech-to-Text Translation, Synthesizing Translated Speech

**Sources:**
- [Provision an Azure Resource for Speech Translation](https://learn.microsoft.com/en-us/training/modules/translate-speech-speech-service/2-speech-service)
- [Translate Speech to Text](https://learn.microsoft.com/en-us/training/modules/translate-speech-speech-service/3-translate-speech-text)
- [Synthesize Translations](https://learn.microsoft.com/en-us/training/modules/translate-speech-speech-service/4-synthesize-translation)

---

## 1. What Is Speech Translation?

> **Speech Translation** = an Azure Speech service capability that performs **real-time, end-to-end translation** of spoken audio, from spoken input in one language to text (or audio) output in another language.

### Two Translation Modes

| Mode | Input | Output | Use Case |
|---|---|---|---|
| **Speech-to-Text Translation** | Spoken audio | Translated text | Subtitles, transcripts in another language |
| **Speech-to-Speech Translation** | Spoken audio | Translated spoken audio | Real-time voice interpreter, multilingual voice apps |

---

## 2. Provisioning the Resource

> Same as the Azure Speech service, provision one of the following:

| Option | Description |
|---|---|
| **Dedicated Azure Speech resource** | Single-service resource for speech only |
| **Foundry Tools (multi-service) resource** | Shared resource; speech translation is included |

### What You Need After Provisioning

| Value | Purpose |
|---|---|
| **Location/Region** | Where the resource is deployed (e.g., `eastus`) |
| **Key** | One of the subscription keys for authentication |

> Both values are on the **Keys and Endpoint** page in the Azure portal.

---

## 3. Speech-to-Text Translation: SDK Pattern

> The pattern is similar to speech recognition (from module 07), but uses **`SpeechTranslationConfig`** instead of `SpeechConfig`, and **`TranslationRecognizer`** instead of `SpeechRecognizer`.

### 6-Step SDK Pattern

| Step | Action |
|---|---|
| **1** | Create a **`SpeechTranslationConfig`** object with your resource key and location |
| **2** | Set the **speech recognition language** (source — the language being spoken) and one or more **target languages** (languages to translate into) on the `SpeechTranslationConfig` |
| **3** | (Optional) Create an **`AudioConfig`** to define the audio input source, default is system microphone; can specify an audio file |
| **4** | Create a **`TranslationRecognizer`** object using `SpeechTranslationConfig` + `AudioConfig` |
| **5** | Call a method on `TranslationRecognizer` — e.g., **`RecognizeOnceAsync()`** to asynchronously translate a single spoken utterance |
| **6** | Process the **`SpeechRecognitionResult`** response |

### SpeechRecognitionResult Properties (Translation)

| Property | Description |
|---|---|
| `Text` | Transcription of the speech in the **original (source) language** |
| `Translations` | **Dictionary** of translated texts — key = ISO language code (e.g., `"en"`, `"fr"`), value = translated text |
| `Reason` | **Outcome of the translation** attempt |
| `Duration` | Duration of the audio |
| `OffsetInTicks` | Offset position in the audio stream |
| `ResultId` | Unique ID for the result |
| `Properties` | Additional metadata |

> `Translations` is the key difference vs regular speech recognition — it returns **multiple language translations** in a single call.

### Reason Values

| `Reason` Value | Meaning |
|---|---|
| `RecognizedSpeech` | Success: `Text` has the transcription, `Translations` has translated text |
| `NoMatch` | Audio parsed but no speech recognized |
| `Canceled` | Error occurred |

---

## 4. Speech-to-Text vs Speech Translation: SDK Object Comparison

| Aspect | Speech to Text (Module 07) | Speech Translation |
|---|---|---|
| **Config object** | `SpeechConfig` | `SpeechTranslationConfig` |
| **Language config** | Recognition language only | Recognition language + **one or more target languages** |
| **Audio input** | `AudioConfig` | `AudioConfig` |
| **Client object** | `SpeechRecognizer` | `TranslationRecognizer` |
| **Key method** | `RecognizeOnceAsync()` | `RecognizeOnceAsync()` |
| **Result object** | `SpeechRecognitionResult` | `SpeechRecognitionResult` |
| **Result includes** | `Text` | `Text` + **`Translations` dictionary** |

---

## 5. Synthesizing Translated Speech (Speech-to-Speech)

> After translating speech to text, you can **synthesize the translated text back into spoken audio**, creating a full **speech-to-speech translation** pipeline.

There are **two approaches**: event-based and manual

---

### 5.1 Event-Based Synthesis

> Best for **1:1 translation**: one source language into **one** target language.

**How it works:**

1. Specify the desired **voice** for the translated speech in `TranslationConfig`
2. Create an **event handler** on the `TranslationRecognizer`'s **`Synthesizing` event**
3. In the event handler, call **`Result.GetAudio()`** to retrieve the **byte stream** of translated audio

| Detail | Value |
|---|---|
| **Best for** | Single target language (1:1) |
| **Trigger** | `Synthesizing` **event** on `TranslationRecognizer` |
| **Get audio** | `Result.GetAudio()` → byte stream |
| **Voice config** | Set on `TranslationConfig` before recognizing |

---

### 5.2 Manual Synthesis

> Best for **1:many translation**: one source language into **multiple** target languages.

**How it works:**

1. **Use `TranslationRecognizer` to translate spoken input** → text in one or more target languages (stored in `Translations` dictionary)
2. Iterate through the `Translations` dictionary
3. For each language, use a **`SpeechSynthesizer`** to synthesize an audio stream

| Detail | Value |
|---|---|
| **Best for** | Multiple target languages (1:many) |
| **Requires** | `TranslationRecognizer` + `SpeechSynthesizer` (two separate operations) |
| **Input** | `Translations` dictionary from translation result |
| **Output** | One audio stream synthesized per target language |

---

### Event-Based vs Manual Synthesis

| Aspect | Event-Based Synthesis | Manual Synthesis |
|---|---|---|
| **Target languages** | **1 (one-to-one)** | **1 or more (one-to-many)** |
| **Approach** | Event handler on `Synthesizing` event | Iterate `Translations` dict + `SpeechSynthesizer` |
| **Audio retrieval** | `Result.GetAudio()` | `SpeechSynthesizer.SpeakTextAsync()` per language |
| **Complexity** | Simpler for single language | More flexible for multi-language |
| **Requires event handler?** | Yes | No |

---

## 6. Full Speech Translation Pipeline

```
Spoken Input (source language)
    ↓
SpeechTranslationConfig (key + region + source language + target languages)
    ↓
AudioConfig (microphone or audio file)
    ↓
TranslationRecognizer
    ↓
RecognizeOnceAsync()
    ↓
SpeechRecognitionResult
    ├── Text           → original transcription (source language)
    └── Translations   → { "en": "Hello", "fr": "Bonjour", ... }
              ↓
    [Optional: Synthesize to audio]
    ├── Event-based (1 language) → Synthesizing event → GetAudio()
    └── Manual (N languages)    → SpeechSynthesizer per language
```