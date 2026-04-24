# Eraser.io Diagram Code

To create beautiful, professional diagrams for your report using [Eraser.io](https://app.eraser.io/), create a new file in Eraser and paste the following code blocks into the code editor on the left pane.

---

### 1. System Architecture Diagram

This diagram shows the three-tier architecture (Presentation, Application, Data) and the Cloud services. Copy and paste the code exactly as is:

```text
// Tamil Speech to ISL System Architecture

Presentation Tier [icon: monitor] {
  RecordRTC (Audio Capture)
  HTML/CSS/JS Interface
  Video Player
  2D Avatar Render
}

Application Tier (FastAPI) [icon: server] {
  /api/process-audio
  /api/video/{word}
  audio_processor (FFmpeg/pydub)
  nlp_processor (ISLConverter)
}

Data Tier [icon: database] {
  ISL_Dataset (Primary MP4s) 
  dataset (Fallback MP4s) 
  2d_avatars (PNG Images) 
}

Cloud Services [icon: cloud] {
  Google Speech-to-Text API
  Google Translate API
}

// Connections
Presentation Tier > Application Tier: HTTP Requests (Fetch API) 
Application Tier > Cloud Services: Secure API Calls
Application Tier > Data Tier: File System Read/Write
Application Tier > Presentation Tier: JSON, Video & Image Streams
```

---

### 2. Pipeline Data Flow Diagram

This flowchart outlines the chronological data processing pipeline from the time the user speaks to the time the video plays.

```text
// Translation Pipeline Data Flow

User Speaks Tamil [color: green, icon: mic]
RecordRTC captures 16kHz WAV [color: green]
POST to /api/process-audio [icon: send]

User Speaks Tamil > RecordRTC captures 16kHz WAV
RecordRTC captures 16kHz WAV > POST to /api/process-audio

// Backend audio processing
Audio Conversion (FFmpeg) [color: blue, icon: file-audio]
Audio Chunking (pydub) [color: blue]

POST to /api/process-audio > Audio Conversion (FFmpeg)
Audio Conversion (FFmpeg) > Audio Chunking (pydub)

// Translation Phase
Google STT (ta-IN) [color: purple, icon: google]
Tamil Text Concatenation [color: purple]
Google Translate (ta to en) [color: purple, icon: languages]

Audio Chunking (pydub) > Google STT (ta-IN)
Google STT (ta-IN) > Tamil Text Concatenation
Tamil Text Concatenation > Google Translate (ta to en)

// NLP Phase
NLTK Tokenize [color: red, icon: type]
Remove Stopwords (Keep Pronouns) [color: red]
WordNet Lemmatizer (Verbs) [color: red]

Google Translate (ta to en) > NLTK Tokenize
NLTK Tokenize > Remove Stopwords (Keep Pronouns)
Remove Stopwords (Keep Pronouns) > WordNet Lemmatizer (Verbs)

// Video Mapping
Directory Lookup [icon: search]
JSON Response [icon: file-json]

WordNet Lemmatizer (Verbs) > Directory Lookup
Directory Lookup > JSON Response

// Frontend Rendering
playNextVideo (Recursive) [color: yellow, icon: play]
Update 2D Avatar Image [color: yellow]
Play Sign Video (onended hook) [color: yellow]

JSON Response > playNextVideo (Recursive)
playNextVideo (Recursive) > Update 2D Avatar Image
playNextVideo (Recursive) > Play Sign Video (onended hook)
```

---

### 3. NLP Process Sequence Diagram

If you want a diagram specifically showing just the NLTK logic (great for the Implementation Details section), use this Sequence Diagram syntax:

```text
// NLP Transformation Sequence

English Sentence > Tokenizer: "Where are you going?"
Tokenizer > Stopwords Filter: ["where", "are", "you", "going", "?"]
Stopwords Filter > Stopwords Filter: Removes "are", "?"
Stopwords Filter > Lemmatizer: ["where", "you", "going"]
Lemmatizer > Lemmatizer: Converts "going" to "go"
Lemmatizer > Uppercase Formatter: ["where", "you", "go"]
Uppercase Formatter > Output: ["WHERE", "YOU", "GO"]
```

### How to use this:
1. Go to **[Eraser.io](https://app.eraser.io/)** and open a new workspace.
2. In the top toolbar, click the **"Code"** button (or press `\`) to open the split code pane on the left.
3. Paste the snippets above one at a time. The diagram will automatically generate on the right canvas.
4. Click **Export** in the top right corner to download it as a high-quality PNG or SVG for your Word document.
