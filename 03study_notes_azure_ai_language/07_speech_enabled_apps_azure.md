# Module: Create Speech-Enabled Apps with Microsoft Foundry
## Session: Provisioning, Speech-to-Text, Text-to-Speech, Audio Formats, Voices, SSML

**Sources:**
- [Provision an Azure Resource for Speech](https://learn.microsoft.com/en-us/training/modules/create-speech-enabled-apps/2-create-speech-service)
- [Use the Azure Speech to Text API](https://learn.microsoft.com/en-us/training/modules/create-speech-enabled-apps/3-speech-to-text)
- [Use the Text to Speech API](https://learn.microsoft.com/en-us/training/modules/create-speech-enabled-apps/4-text-to-speech)
- [Configure Audio Format and Voices](https://learn.microsoft.com/en-us/training/modules/create-speech-enabled-apps/5-audio-format-voices)
- [Use Speech Synthesis Markup Language](https://learn.microsoft.com/en-us/training/modules/create-speech-enabled-apps/6-speech-synthesis-markup)

---

## 1. What Is Azure Speech?

> **Azure Speech** = an Azure AI service that provides **speech-to-text** (audio → text) and **text-to-speech** (text → audio) capabilities, plus customization via SSML and custom speech models.

### 2 Core Directions

| Direction | Feature | What It Does |
|---|---|---|
| **Audio → Text** | Speech to Text | Transcribes spoken audio into written text |
| **Text → Audio** | Text to Speech | Converts written text into spoken audio |

---

## 2. Provisioning the Resource

> To use Azure Speech, provision one of the following:

| Option | Description |
|---|---|
| **Dedicated Azure Speech resource** | Single-service resource for speech only |
| **Microsoft Foundry (multi-service) resource** | Shared resource; Speech is included |

### What You Need After Provisioning

| Value | Purpose |
|---|---|
| **Location/Region** | Where the resource is deployed (e.g., `eastus`) |
| **Key** | One of the subscription keys for authentication |

> Both values are found on the **Keys and Endpoint** page in the Azure portal.

### SpeechConfig (The Starting Point)

> Almost all Azure Speech SDK interactions begin with creating a **SpeechConfig object** that encapsulates the connection to your resource.

```python
import azure.cognitiveservices.speech as speech_sdk

speech_config = speech_sdk.SpeechConfig(your_project_key, 'eastus')
```

**Install the SDK:**
```
pip install azure-cognitiveservices-speech
```

---

## 3. Speech to Text

> **Speech to Text** = transcribes audio input into written text. Supports real-time, batch, and custom models.

### 4 Speech Recognition Features

| Feature | Description |
|---|---|
| **Real-time transcription** | Instant transcription with intermediate results for **live audio** |
| **Fast transcription** | Fastest synchronous output for **predictable latency** scenarios |
| **Batch transcription** | Efficient processing for **large volumes of prerecorded audio** |
| **Custom speech** | Models with enhanced accuracy for **specific domains and conditions** |

### 5-Step SDK Pattern (Speech to Text)

| Step | Action |
|---|---|
| **1** | Create a **`SpeechConfig`** object with your resource key and location |
| **2** | (Optional) Create an **`AudioConfig`** to define the audio source, default is system microphone; can specify an audio file |
| **3** | Create a **`SpeechRecognizer`** object using `SpeechConfig` + `AudioConfig` |
| **4** | Call a method on `SpeechRecognizer` — e.g., **`RecognizeOnceAsync()`** to transcribe a single utterance |
| **5** | Process the **`SpeechRecognitionResult`** response |

### SpeechRecognitionResult Properties

| Property | Description |
|---|---|
| `Text` | The transcribed text (on success) |
| `Reason` | Outcome of the recognition attempt |
| `Duration` | Duration of the audio |
| `OffsetInTicks` | Offset position in the audio stream |
| `ResultId` | Unique ID for the result |
| `Properties` | Additional metadata (e.g., cancellation reason) |

### Reason Values

| `Reason` Value | Meaning |
|---|---|
| `RecognizedSpeech` | Success: `Text` contains the transcription |
| `NoMatch` | Audio parsed but **no speech recognized** |
| `Canceled` | Error occurred: check `Properties["CancellationReason"]` |

---

## 4. Text to Speech

> **Text to Speech** = converts written text into spoken audio output.

### 2 REST API Options

| API | Use Case |
|---|---|
| **Text to speech API** | Primary API for interactive speech synthesis |
| **Batch synthesis API** | Converts **large volumes of text** to audio (e.g., generating an audiobook) |

### 5-Step SDK Pattern (Text to Speech)

| Step | Action |
|---|---|
| **1** | Create a **`SpeechConfig`** object with your resource key and location |
| **2** | (Optional) Create an **`AudioConfig`** to define the output — default is system speaker; can specify an audio file or `null` to return an audio stream directly |
| **3** | Create a **`SpeechSynthesizer`** object using `SpeechConfig` + `AudioConfig` |
| **4** | Call a method on `SpeechSynthesizer` — e.g., **`SpeakTextAsync()`** to convert text to speech |
| **5** | Process the **`SpeechSynthesisResult`** response |

### SpeechSynthesisResult Properties

| Property | Description |
|---|---|
| `AudioData` | The synthesized audio stream |
| `Reason` | Outcome of synthesis |
| `ResultId` | Unique ID for the result |
| `Properties` | Additional metadata |

### Reason Value (Text to Speech)

| `Reason` Value | Meaning |
|---|---|
| `SynthesizingAudioCompleted` | Success. `AudioData` contains the audio stream |

### Speech to Text vs Text to Speech — SDK Object Comparison

| Aspect | Speech to Text | Text to Speech |
|---|---|---|
| **Config object** | `SpeechConfig` | `SpeechConfig` |
| **I/O config object** | `AudioConfig` (input source) | `AudioConfig` (output device) |
| **Client object** | `SpeechRecognizer` | `SpeechSynthesizer` |
| **Key method** | `RecognizeOnceAsync()` | `SpeakTextAsync()` |
| **Result object** | `SpeechRecognitionResult` | `SpeechSynthesisResult` |
| **Success Reason** | `RecognizedSpeech` | `SynthesizingAudioCompleted` |

---

## 5. Audio Format and Voices

### Audio Output Formats

> When synthesizing speech, you can configure the **audio output format** on the `SpeechConfig` object. Choose based on your needs:

| Consideration | Examples |
|---|---|
| **Audio file type** | WAV, MP3, OGG |
| **Sample rate** | 8 kHz, 16 kHz, 24 kHz, 48 kHz |
| **Bit depth** | 16-bit, 24-bit |

**Set format in Python:**

```python
speech_config.set_speech_synthesis_output_format(
    SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm
)
```

> `Riff24Khz16BitMonoPcm` = WAV file, 24 kHz sample rate, 16-bit, mono channel.

### Voices

> Azure Speech provides multiple **voices** to personalize your app. Voice names follow the pattern: **`{locale}-{PersonName}`**

| Example Voice Name | Locale | Person |
|---|---|---|
| `en-GB-George` | English (UK) | George |
| `en-US-AriaNeural` | English (US) | Aria (Neural) |
| `en-US-GuyNeural` | English (US) | Guy (Neural) |

**Set voice in Python:**

```python
speech_config.speech_synthesis_voice_name = "en-GB-George"
```

> **Neural voices** offer more **natural-sounding** output and support advanced features like **speaking styles**.

---

## 6. Speech Synthesis Markup Language (SSML)

> **SSML** = an **XML-based syntax** that gives fine-grained control over how synthesized speech sounds, going far beyond plain text input.

### What SSML Can Control

| Capability | Description |
|---|---|
| **Speaking style** | Set emotional tone: `"excited"`, `"cheerful"`, `"sad"` (neural voices only) |
| **Pauses / silence** | Insert `<break>` tags with `strength` or `time` attributes |
| **Phonemes** | Specify exact phonetic pronunciation (e.g., "SQL" → "sequel") |
| **Prosody** | Adjust pitch, timbre (voice tone), and speaking rate |
| **Say-as rules** | Format strings as dates, times, phone numbers, currency, etc. |
| **Audio insertion** | Insert recorded audio clips or background sounds |
| **Multiple voices** | Use different voices within the same SSML block |

### SSML Example

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
                     xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="en-US-AriaNeural">
        <mstts:express-as style="cheerful">
          I say tomato
        </mstts:express-as>
    </voice>
    <voice name="en-US-GuyNeural">
        I say <phoneme alphabet="sapi" ph="t ao m ae t ow"> tomato </phoneme>.
        <break strength="weak"/>Lets call the whole thing off!
    </voice>
</speak>
```

### SSML Key Elements

| Element / Attribute | Purpose |
|---|---|
| `<speak>` | Root element; wraps all SSML content |
| `<voice name="...">` | Selects the voice to use for this block |
| `<mstts:express-as style="...">` | Sets a speaking style (e.g., `cheerful`, `excited`) — neural voices only |
| `<phoneme alphabet="..." ph="...">` | Specifies phonetic pronunciation of a word |
| `<break strength="...">` | Inserts a pause (`none`, `x-weak`, `weak`, `medium`, `strong`, `x-strong`) |
| `xml:lang` | Language of the spoken content |

### How to Submit SSML

```python
speech_synthesizer.speak_ssml('<speak>...</speak>')
```

### Plain Text vs SSML

| Method | Use When |
|---|---|
| **`SpeakTextAsync("text")`** | Simple speech synthesis with no style control |
| **`speak_ssml("<speak>...</speak>")`** | Need control over style, pauses, pronunciation, prosody, or multiple voices |

---

## 7. Full SDK Object Flow

```
SpeechConfig (key + region)
    ↓
AudioConfig (input source OR output device)
    ↓
SpeechRecognizer (STT) / SpeechSynthesizer (TTS)
    ↓
RecognizeOnceAsync() / SpeakTextAsync() / speak_ssml()
    ↓
SpeechRecognitionResult / SpeechSynthesisResult
```

