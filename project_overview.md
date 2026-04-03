# Tamil Speech to ISL Translation System — Complete Project Reference

> **Purpose of this document**: This is an exhaustive technical and conceptual reference for the project located at `d:\SRM Notes\SEM6\Minor Project V3`. It is written so that any AI assistant or developer reading it will have full, unambiguous context about what the project is, how every part works, what has been built, and what is still incomplete. Use this as a master prompt when starting a new conversation about this project.

---

## 1. Project Identity

| Field | Value |
|---|---|
| **Project Name** | Tamil Speech to ISL Translation System |
| **Type** | Academic Minor Project (SRM University, Semester 6) |
| **Version** | V3 (third major iteration) |
| **Goal** | Convert Tamil spoken language into Indian Sign Language (ISL) video sequences in real-time |
| **Stack** | Python (FastAPI) backend + Vanilla HTML/CSS/JS frontend |
| **Run Command** | `python -m uvicorn backend.main:app --reload` (from project root) |
| **Access URL** | `http://127.0.0.1:8000` |

---

## 2. Problem Statement

Hearing-impaired individuals who communicate via **Indian Sign Language (ISL)** often cannot understand Tamil spoken or broadcast content. This project bridges that gap by:

1. Accepting Tamil speech (via microphone or audio file upload)
2. Converting it to text using Google's Speech Recognition API
3. Translating that Tamil text to English
4. Converting the English sentence to **ISL grammatical order** (which is fundamentally different from English grammar)
5. Playing back a sequential video compilation of the corresponding ISL sign videos

The end result is a real-time, browser-based ISL interpreter for Tamil speakers.

---

## 3. Project File Structure

```
d:\SRM Notes\SEM6\Minor Project V3\
│
├── backend/                          ← Python FastAPI application
│   ├── main.py                       ← API server, all endpoints, pipeline controller
│   ├── requirements.txt              ← Python library dependencies
│   ├── modules/
│   │   └── nlp_processor.py          ← NLP/ISL grammar conversion logic (NLTK)
│   └── ml_pipeline/
│       ├── extract_poses.py          ← MediaPipe keypoint extraction (offline utility, not used at runtime)
│       └── models/
│           ├── hand_landmarker.task  ← MediaPipe Hand Landmarker model file (7.8 MB)
│           └── pose_landmarker.task  ← MediaPipe Pose Landmarker model file (5.8 MB)
│
├── frontend/                         ← Vanilla JS/HTML/CSS single-page app
│   ├── index.html                    ← Main UI with three panels
│   ├── style.css                     ← Dark-theme modern UI styles
│   ├── app.js                        ← Audio recording, API calls, video playback logic
│   ├── avatar.png                    ← Default 2D signer avatar sprite (idle)
│   ├── avatar_eat.png                ← Avatar sprite for word "EAT"
│   ├── avatar_father.png             ← Avatar sprite for word "FATHER"
│   ├── avatar_friend.png             ← (and many more word-specific pngs...)
│   └── [avatar_<word>.png ...]       ← ~26 word-specific avatar sprite images
│
├── ISL_Dataset/                      ← PRIMARY video dataset (151 .mp4 files)
│   ├── How.mp4, What.mp4, Where.mp4  ← Question word signs
│   ├── Who.mp4, Why.mp4, When.mp4    ← More question signs
│   ├── Hello.mp4, Good.mp4 ...       ← Common word signs
│   ├── A.mp4, B.mp4 ... Z.mp4        ← Alphabet signs (fingerspelling)
│   └── [~151 total .mp4 files]
│
├── dataset/                          ← SECONDARY/fallback video dataset (can be empty)
│   └── [word].mp4 files (optional)
│
├── run_project.bat                   ← Windows batch file to start the server
└── README.md                         ← Basic project documentation
```

---

## 4. Full Technology Stack

### Backend
| Library | Version/Notes | Purpose |
|---|---|---|
| `fastapi` | Latest | Web framework, REST API |
| `uvicorn` | Latest | ASGI server to run FastAPI |
| `SpeechRecognition` | Latest | Converts audio to text (uses Google API internally) |
| `deep-translator` | Latest | `GoogleTranslator` for Tamil → English |
| `nltk` | Latest | NLP: tokenization, stopword removal, lemmatization |
| `pydub` | Latest | Audio format conversion (WAV normalization) |
| `python-multipart` | Latest | Parses multipart form-data (file uploads) |
| `opencv-python` | Latest | Used in offline ML pipeline only |
| `numpy` | Latest | Used in offline ML pipeline only |
| `mediapipe` | (installed separately) | Used in offline pose extraction only |

### Frontend
| Technology | Purpose |
|---|---|
| HTML5 | Page structure, semantic elements |
| CSS3 (Vanilla) | All styling — dark theme, animations, grid layout |
| JavaScript (Vanilla ES6+) | All logic — recording, API calls, video sequencing |
| RecordRTC (CDN) | Cross-browser audio recording to PCM WAV |
| Google Fonts (Outfit) | Typography |
| Font Awesome 6 | Icons throughout the UI |

---

## 5. Architecture Overview

```
[User's Browser]
      │
      │  (1) Speaks Tamil OR uploads .wav/.mp3 file
      ▼
[Frontend: app.js]
      │
      │  (2) Audio captured via RecordRTC → PCM WAV blob
      │      OR file selected from disk
      │
      │  (3) POST /api/process-audio (multipart form-data)
      ▼
[Backend: FastAPI — main.py]
      │
      ├──(4) Save audio to temp .wav file
      ├──(5) pydub: Convert audio format if needed
      │
      ├──(6) SpeechRecognition → Google STT API
      │      tamil_text = "நான் பள்ளிக்கு செல்கிறேன்"
      │
      ├──(7) deep-translator → Google Translate
      │      english_text = "I am going to school"
      │
      ├──(8) nlp_processor.ISLConverter.english_to_isl()
      │      isl_words = ["I", "GO", "SCHOOL"]
      │          • Removes stopwords (the, a, am, is, are, be...)
      │          • Keeps pronouns (I, you, we, he, she...)
      │          • Lemmatizes verbs (going → go)
      │          • Uppercases all words
      │
      ├──(9) Video Mapping
      │      For each word in isl_words:
      │        - Look in /ISL_Dataset/{word}.mp4 (primary)
      │        - If not found, look in /dataset/{word}.mp4 (fallback)
      │        - If still not found, mark as missing (fingerspelling fallback)
      │
      └──(10) Returns JSON response:
             {
               "tamil_text": "நான்...",
               "english_text": "I am going to school",
               "isl_words": ["I", "GO", "SCHOOL"],
               "video_sequence": [
                 {"word": "I",      "video_url": "/api/video/i?source=isl",      "found": true},
                 {"word": "GO",     "video_url": "/api/video/go?source=isl",     "found": true},
                 {"word": "SCHOOL", "video_url": "/api/video/school?source=isl", "found": true}
               ]
             }
      │
      ▼
[Frontend: app.js — startVideoSequence()]
      │
      ├── Updates Pipeline UI (Tamil text, English text, ISL tags)
      ├── Displays latency metrics (end-to-end time, avg per word)
      └── Plays video sequence:
            • For each word:
              - If found: play .mp4 via <video> tag, wait for 'onended', then play next
              - If not found: show [Spell] <WORD> overlay for 1.5 seconds, then next
              - Simultaneously updates:
                  • ISL tag highlight (current word glows)
                  • Word overlay on video (bottom caption)
                  • 2D avatar sprite (avatar_<word>.png)
                  • Progress bar and counter (1/3, 2/3...)
```

---

## 6. Detailed Module Explanations

### 6.1 `backend/main.py` — The API Server

This is the central controller of the entire backend. It:

- **Initializes** FastAPI with CORS middleware (allows all origins for local development)
- **Mounts** the `frontend/` directory as static files at the root `/` URL, so the frontend is served directly by the same server — no separate web server needed
- **Defines two API endpoints**:

#### `POST /api/process-audio`
The main pipeline endpoint. Accepts a multipart/form-data upload with a field named `file`. Supported formats: `.wav`, `.mp3`, `.ogg`, `.flac`, `.webm`, `.m4a`.

Steps:
1. Saves the uploaded audio to a temp file
2. Attempts pydub format conversion to normalize to pure WAV (if ffmpeg is available; otherwise it proceeds with the raw bytes and SpeechRecognition handles it)
3. Passes audio to `sr.Recognizer().recognize_google(audio_data, language="ta-IN")` — this makes a remote call to Google's Speech-to-Text API
4. Translates Tamil text to English using `GoogleTranslator(source='ta', target='en').translate(text)`
5. Passes English to `ISLConverter.english_to_isl()` for grammar conversion
6. Maps each ISL word to a video file path in `ISL_Dataset/` or `dataset/`
7. Returns the full JSON response
8. Cleans up the temp file

#### `GET /api/video/{word}?source=isl|dummy`
Serves the actual `.mp4` video file for a given word. The `source` query param determines which folder to look in:
- `source=isl` → `ISL_Dataset/{word}.mp4`
- `source=dummy` → `dataset/{word}.mp4`

---

### 6.2 `backend/modules/nlp_processor.py` — The ISL Grammar Engine

This is the **NLP heart** of the project. The `ISLConverter` class converts English sentences to ISL-compatible word sequences.

#### How ISL Grammar Differs from English
ISL (Indian Sign Language) follows a **Topic-Comment** or **Subject-Object-Verb (SOV)** structure, unlike English's **Subject-Verb-Object (SVO)**. More importantly:
- ISL **drops** articles (a, an, the)
- ISL **drops** auxiliary/linking verbs (am, is, are, was, were, be, been)
- ISL **drops** prepositions much of the time (to, from, at)
- ISL uses the **root form** of verbs (go, not going; eat, not eating)
- ISL uses **question signs** (WHAT, WHERE, HOW, WHO, WHY, WHEN) — these are actual signs that exist in ISL!

#### Current Implementation (`ISLConverter`)

```python
self.stop_words = set(stopwords.words('english'))
self.stop_words.update(['am', 'is', 'are', 'was', 'were', 'be', 'being', 'been', 'to', 'the', 'a', 'an'])
```

For each word in the English sentence:
1. Skip punctuation
2. Skip stop words UNLESS the word is a pronoun (I, we, you, he, she, they, it)
3. Lemmatize the word as a verb (going → go, eating → eat, runs → run)
4. Uppercase it and add to the result list

**Example transformations:**
- `"I am going to school"` → `["I", "GO", "SCHOOL"]`
- `"She is eating food"` → `["SHE", "EAT", "FOOD"]`
- `"Where are you going?"` → `["WHERE", "YOU", "GO"]` *(this should work, but see Known Issues)*

> [!IMPORTANT]
> **Known Issue with Questions**: NLTK's default English stopword list includes words like "where", "what", "how", "who", "why", "when". The current `nlp_processor.py` does NOT explicitly preserve these question words from being filtered out by the stopword removal step. This means sentences like "Where are you going?" may produce `["YOU", "GO"]` instead of `["WHERE", "YOU", "GO"]`. The ISL_Dataset DOES have video files for all these question words (How.mp4, What.mp4, Where.mp4, Who.mp4, Why.mp4, When.mp4, Which.mp4, Whose.mp4), but they are never triggered because the words get filtered. This is a bug that needs to be fixed.

---

### 6.3 `backend/ml_pipeline/extract_poses.py` — Offline ML Pipeline (Not Used at Runtime)

This is a **standalone utility script** for research/future development. It is NOT called during the live application flow.

**What it does**: Given a folder of `.mp4` ISL videos, it uses MediaPipe's Pose Landmarker and Hand Landmarker to extract keypoint data from every frame and stores it as `.json` files.

**Landmark format**:
- Pose: 33 landmarks × 4 values (x, y, z, visibility) = 132 floats
- Left hand: 21 landmarks × 3 values = 63 floats
- Right hand: 21 landmarks × 3 values = 63 floats
- Total per frame: 258 floats

**Purpose**: This data would be used in a future iteration to train a gesture recognition model or to drive a 3D avatar instead of playing pre-recorded videos. The model files (`hand_landmarker.task`, `pose_landmarker.task`) are already present in `backend/ml_pipeline/models/`.

---

### 6.4 `frontend/index.html` — The UI Structure

Three-panel layout:

| Panel | Column | Rows | Content |
|---|---|---|---|
| **Input Panel** | Left | Top | Record button, Upload button, waveform animation, loader, error display |
| **Processing Panel** | Left | Bottom | Three pipeline steps: Tamil Text → English Translation → ISL Grammar tags |
| **Output Panel** | Right | Full height | Video player + Avatar side-by-side, word overlay, video controls, latency metrics |

Key HTML elements (referenced in `app.js`):
- `#recordBtn` — Start/Stop recording button
- `#audioUpload` — File input (hidden, triggered by label)
- `#recordingStatus` — Animated waveform shown while recording
- `#uploadStatus` — Shows filename and "Process File" button
- `#processingLoader` — Spinning loader shown during API call
- `#errorMsg` / `#errorText` — Error display
- `#tamilOutput` — Shows recognized Tamil text
- `#englishOutput` — Shows translated English text
- `#islOutput` — Container for ISL word tags (spans)
- `#islVideoPlayer` — The `<video>` element for sign videos
- `#videoPlaceholder` — Default empty state for video area
- `#currentWordOverlay` — Word caption shown at bottom of video
- `#avatarContainer` / `#avatarImage` — 2D avatar sprite display
- `#videoControls` — Replay button + progress bar + counter
- `#missingWordWarning` — Yellow banner when fingerspelling fallback triggers
- `#latencyDisplay`, `#e2eLatencyValue`, `#avgLatencyValue` — Latency metrics

---

### 6.5 `frontend/app.js` — All Client-Side Logic

#### Audio Recording Flow
1. User clicks **Start Recording**
2. `navigator.mediaDevices.getUserMedia({ audio: true })` requests mic access
3. **RecordRTC** (loaded from CDN) captures audio as PCM WAV at 16kHz mono — chosen specifically because it does NOT require FFmpeg on the server, unlike WebM which Chrome natively produces
4. User clicks **Stop Recording**
5. `recordRTC.getBlob()` returns a WAV Blob
6. A `File` object is created from the blob and passed to `processAudioFile()`
7. `sequenceStartTime = performance.now()` is set to begin latency measurement

#### Upload Flow
1. User clicks **Upload Audio** label
2. File picker opens, accepts `.wav` and `.mp3`
3. On selection, filename is displayed and the file is stored in `audioBlob`
4. User clicks **Process File** button
5. Same `processAudioFile()` is called

#### API Call (`processAudioFile`)
1. Builds a `FormData` with the file appended as `'file'`
2. `fetch('/api/process-audio', { method: 'POST', body: formData })`
3. Shows loader, hides other status elements
4. On success: calls `updatePipelineUI(data)` and `startVideoSequence(data.video_sequence)`
5. On failure: calls `showError(message)`

#### Video Playback (`playNextVideo`)
Recursive function that plays one word at a time:
- If video is found: set `videoPlayer.src`, call `.play()`, on `onended` event call itself again with `currentVideoIndex++`
- If video is not found: show `[Spell] WORD` overlay, wait 1500ms via `setTimeout`, then call itself again
- Simultaneously updates: ISL tag highlight (`.active` class), word overlay text, avatar sprite src (`avatar_<word>.png`), progress bar width, counter text
- On completion (index ≥ sequence length): pauses player, removes active states

#### Latency Measurement
- `sequenceStartTime` is set to `performance.now()` when recording stops or "Process File" is clicked
- When `startVideoSequence()` is called (i.e., API response received and video starts), `endTime = performance.now()` is captured
- `e2eLatency = (endTime - sequenceStartTime) / 1000` (seconds)
- `cumulativeE2eLatency` and `cumulativeWordCount` accumulate across sessions for session-average tracking
- Displayed in the latency metrics panel below the video output

---

### 6.6 `frontend/style.css` — The Design System

Dark, premium glassmorphism-inspired design.

**CSS Custom Properties (Design Tokens):**
```css
--bg-dark: #121212;       /* Page background */
--bg-panel: #1e1e1e;      /* Panel cards */
--bg-highlight: #2c2c2c;  /* Nested containers */
--accent: #00d2ff;        /* Cyan accent color */
--accent-glow: rgba(0, 210, 255, 0.4);
--text-main: #f5f5f5;
--text-muted: #a0a0a0;
--success: #00e676;       /* Green for upload button */
--danger: #ff5252;        /* Red for recording state */
```

**Layout**: CSS Grid — 2-column on desktop, single column on ≤1024px screens.

**Key Animations**:
- `pulse` — Recording button pulses in red while active
- `bounce` — Waveform bars animate while recording
- `spin` — Processing spinner
- `fadeIn` — Smooth reveal animation for latency metrics and status containers
- `signingBody` — Avatar scales slightly while a word is being signed

---

## 7. The ISL Dataset

**Primary Dataset Location**: `ISL_Dataset/` — 151 `.mp4` files

The dataset covers:
- **Alphabet**: A–Z (26 files) — used for fingerspelling
- **Numbers**: 0–9 (10 files)
- **Question Words**: How, What, When, Where, Which, Who, Whose, Why (8 files — ALL exist but may not be used due to the NLP bug)
- **Common Words**: Hello, Goodbye (Bye), Thank You, Please, Sorry, Help, Good, Happy, Sad, Yes, No, Welcome, etc.
- **Action Words**: Go, Come, Eat, Learn, Study, Work, Walk, Talk, Laugh, Sign, Sing, etc.
- **Pronouns**: I, Me, My, We, Our, You, Your, He, His, She, Her, They, It, Us, Yourself, Self
- **Common Nouns**: School, College, Name, Home, Day, Time, Computer, Teacher, Engineer, God, etc.
- **Connectors/Misc**: And, But, So, Not, Do Not, Does Not, Can, Cannot, More, Next, Right, Wrong, etc.

**Video Format**: Each file is a short (1–3 second) `.mp4` clip of a human demonstrating the ISL sign for that word. The filename must exactly match the lowercase English word (e.g., `hello.mp4`, `thank you.mp4`).

**Video Lookup Logic**: The backend does a case-insensitive match by lowercasing the ISL word and checking for `{word}.mp4`. Multi-word tokens (like "thank you") would need a composite filename.

---

## 8. How to Run the Project

### Prerequisites
- Python 3.9+
- `pip install -r backend/requirements.txt`
- Internet connection (needed for Google STT and Google Translate APIs)
- Microphone (optional, for live recording)

### Start Server
```powershell
# From the project root directory:
python -m uvicorn backend.main:app --reload
```

### Open in Browser
```
http://127.0.0.1:8000
```

The server serves both the API (`/api/*`) and the frontend (`/`) from the same process.

---

## 9. Known Bugs and Pending Issues

### 🐛 Bug 1: Question Words Filtered Out (CRITICAL)
**What**: Words like "where", "what", "how", "who", "why", "when" are in NLTK's English stopword list. The current `nlp_processor.py` does not explicitly whitelist/preserve them. This means a Tamil question like "நீங்கள் எங்கே போகிறீர்கள்?" ("Where are you going?") translates to English "Where are you going?" but the ISL conversion drops "where" and produces only `["YOU", "GO"]` — missing the crucial question sign.

**Fix needed in `backend/modules/nlp_processor.py`**: Add question words to the preserved words list, similar to how pronouns are preserved. The ISL dataset already has all the question word videos (`Where.mp4`, `What.mp4`, `How.mp4`, `Who.mp4`, `Why.mp4`, `When.mp4`, `Which.mp4`, `Whose.mp4`).

**Fix**: In `__init__`, define a set of preserved words:
```python
self.preserved_words = {
    'i', 'we', 'you', 'he', 'she', 'they', 'it',  # pronouns
    'what', 'where', 'when', 'who', 'why', 'how', 'which', 'whose'  # question words
}
```
Then in `english_to_isl()`, the stop word check should be:
```python
if word in self.stop_words and word not in self.preserved_words:
    continue
```

### 🐛 Bug 2: ISL Word Order (Grammar)
**What**: The current NLP processor does NOT reorder words to match ISL's SOV grammar. It processes words in English order (SVO). For example, "I love you" stays as `["I", "LOVE", "YOU"]` which happens to be fine, but "I am going to school" becomes `["I", "GO", "SCHOOL"]` which is acceptable but not truly ISL-ordered.

**True ISL order**: `SCHOOL I GO` (topic-comment structure). This reordering is complex and would require POS tagging and constituency parsing.

### 🐛 Bug 3: Audio Format Without FFmpeg
**What**: The system was designed to work even without FFmpeg installed. If pydub's format conversion fails (no FFmpeg), it falls through to raw SpeechRecognition. However, browser-recorded audio via RecordRTC is already in PCM WAV format (thanks to `StereoAudioRecorder`), so this is rarely a problem.

### ⚠️ Missing Feature: 3D/Animated Avatar
The project currently uses **static PNG sprites** for the avatar. Each word has one single pose image (`avatar_<word>.png`). There is no actual signing animation. The MediaPipe pose extraction pipeline (`extract_poses.py`) is built but never integrated into the live system.

### ⚠️ Missing Feature: Offline Mode
Both Speech Recognition and Translation require internet access (Google APIs). The project has no offline fallback.

### ⚠️ Missing Feature: Tamil Input Keyboard
Users cannot type Tamil text directly — only spoken audio is accepted.

---

## 10. Data Flow — Step-by-Step Example

**User says** (in Tamil): *"நீங்கள் எங்கே போகிறீர்கள்?"*
*(English: "Where are you going?")*

| Step | What Happens | Result |
|---|---|---|
| 1 | User speaks into mic, clicks Stop | WAV blob created |
| 2 | `processAudioFile()` POSTs blob to `/api/process-audio` | HTTP request sent |
| 3 | Backend writes to temp WAV file | temp file saved |
| 4 | Google STT processes audio | `tamil_text = "நீங்கள் எங்கே போகிறீர்கள்"` |
| 5 | GoogleTranslator translates | `english_text = "Where are you going?"` |
| 6 | ISLConverter tokenizes | `["where", "you", "go", "?"]` |
| 7 | Stopword filter runs | **BUG**: "where" filtered → `["you", "go"]` ← *wrong* |
| 7 (fixed) | Stopword filter with fix | `["where", "you", "go"]` ← *correct* |
| 8 | Lemmatized + uppercased | `["WHERE", "YOU", "GO"]` |
| 9 | Video lookup | `Where.mp4` ✅, `You.mp4` ✅, `Go.mp4` ✅ |
| 10 | JSON response returned | `video_sequence` with 3 items |
| 11 | Frontend plays videos in order | WHERE sign → YOU sign → GO sign |
| 12 | Latency calculated | e.g., `2.4s end-to-end, 0.8s/word` |

---

## 11. Summary of All Source Files

| File | Language | Purpose | Called At |
|---|---|---|---|
| `backend/main.py` | Python | FastAPI server, all endpoints, pipeline orchestration | Runtime (always) |
| `backend/modules/nlp_processor.py` | Python | ISL grammar conversion (NLTK) | Runtime (per request) |
| `backend/ml_pipeline/extract_poses.py` | Python | Offline MediaPipe pose extraction utility | Offline only (manual run) |
| `backend/requirements.txt` | Text | Python pip dependencies | Setup time |
| `frontend/index.html` | HTML | UI structure, three-panel layout | Browser page load |
| `frontend/style.css` | CSS | Dark theme, animations, responsive grid | Browser page load |
| `frontend/app.js` | JavaScript | Recording, upload, API call, video playback, latency | Browser runtime |
| `frontend/avatar*.png` | PNG | Static 2D avatar sprite images for each word | During video sequence |
| `ISL_Dataset/*.mp4` | MP4 | Pre-recorded ISL sign videos (151 files) | Streamed during playback |
| `run_project.bat` | Batch | Windows shortcut to start uvicorn server | Manual execution |
| `README.md` | Markdown | Project documentation | Reference |

---

## 12. Future Development Roadmap

1. **Fix question word bug** in `nlp_processor.py` (high priority)
2. **Implement proper ISL word reordering** using POS tagging (spaCy)
3. **Integrate MediaPipe pose data** to drive an animated 3D avatar instead of static images
4. **Add text input mode** so users can type Tamil/English directly
5. **Add offline STT** (e.g., Vosk or Whisper) to remove Google API dependency
6. **Expand ISL dataset** with more words and better quality videos
7. **Add confidence score display** showing STT confidence percentage
8. **Support sentence-level ISL** (not just word-by-word) for more natural signing

---

*This document was generated on 2026-03-27 from a full source code audit of the project. All file paths, function names, variable names, and logic descriptions are exact and current as of that date.*
