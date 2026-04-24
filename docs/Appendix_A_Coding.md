
# APPENDIX A: CODING

This appendix presents the key code snippets from the Tamil Speech to ISL Translation System, demonstrating the core functionality of each module.

---

## A.1 FastAPI Application Setup and Configuration

The backend initializes FastAPI with CORS middleware and creates singleton instances of the speech recognizer, translator, and ISL converter that are reused across all requests.

**File: backend/main.py**

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import speech_recognition as sr
from deep_translator import GoogleTranslator
from pydub import AudioSegment
from pydub.silence import split_on_silence
import imageio_ffmpeg

AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe()
from backend.modules.nlp_processor import ISLConverter

app = FastAPI(title="Tamil Speech to ISL")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

recognizer = sr.Recognizer()
translator = GoogleTranslator(source='ta', target='en')
isl_converter = ISLConverter()

BASE_DIR = Path(__file__).resolve().parent.parent
ISL_DATASET_DIR = BASE_DIR / "ISL_Dataset"
DATASET_DIR = BASE_DIR / "dataset"
FRONTEND_DIR = BASE_DIR / "frontend"
```

---

## A.2 Main Pipeline Endpoint — Audio Processing and Chunking

The /api/process-audio endpoint receives audio, converts it to 16kHz mono WAV using FFmpeg, and splits it on silence boundaries using pydub for handling long recordings.

**File: backend/main.py**

```python
@app.post("/api/process-audio")
async def process_audio(file: UploadFile = File(...)):
    if not file.filename.endswith((".wav", ".mp3", ".ogg", ".flac", ".webm", ".m4a")):
        raise HTTPException(status_code=400, detail="Unsupported audio format")

    # Save uploaded audio to temp file
    original_suffix = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=original_suffix) as temp_audio:
        shutil.copyfileobj(file.file, temp_audio)
        temp_audio_path = temp_audio.name

    # Convert to 16kHz mono WAV using FFmpeg
    wav_audio_path = temp_audio_path + "_converted.wav"
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ffmpeg_exe, "-y", "-i", temp_audio_path,
        "-ac", "1", "-ar", "16000", wav_audio_path],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Split audio on silence for handling long recordings
    full_audio = AudioSegment.from_file(wav_audio_path)
    chunks = split_on_silence(full_audio,
        min_silence_len=500,
        silence_thresh=full_audio.dBFS - 16,
        keep_silence=250)
    if not chunks:
        chunks = [full_audio]
```

---

## A.3 Speech Recognition — Per-Chunk Tamil STT

Each audio chunk is processed independently through Google's Speech-to-Text API with Tamil language support (ta-IN). Chunk-level errors are handled gracefully without terminating the pipeline.

**File: backend/main.py**

```python
    tamil_text_results = []
    for i, chunk in enumerate(chunks):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            chunk_file_path = tmp_file.name
        chunk.export(chunk_file_path, format="wav")

        try:
            with sr.AudioFile(chunk_file_path) as source:
                audio_data = recognizer.record(source)
            chunk_text = recognizer.recognize_google(audio_data, language="ta-IN")
            tamil_text_results.append(chunk_text)
        except sr.UnknownValueError:
            print(f"Chunk {i}: Silence or incomprehensible speech. Skipping.")
        except sr.RequestError as e:
            print(f"Chunk {i}: API Error - {e}")
        finally:
            if os.path.exists(chunk_file_path):
                os.remove(chunk_file_path)

    tamil_text = " ".join(tamil_text_results)
```

---

## A.4 Translation and ISL Conversion Pipeline

After speech recognition, the Tamil text is translated to English and then converted to ISL-compatible words through the NLP module.

**File: backend/main.py**

```python
    # Tamil to English Translation
    english_text = translator.translate(tamil_text)

    # English to ISL Grammar Conversion
    isl_words = isl_converter.english_to_isl(english_text)

    # Return complete pipeline response
    return JSONResponse(content={
        "tamil_text": tamil_text,
        "english_text": english_text,
        "isl_words": [w["word"] for w in mapped_videos],
        "video_sequence": mapped_videos
    })
```

---

## A.5 NLP Processing — ISL Grammar Conversion (Complete Module)

The ISLConverter class transforms English sentences into ISL word sequences through tokenization, stopword removal (preserving pronouns), and verb lemmatization.

**File: backend/modules/nlp_processor.py**

```python
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

class ISLConverter:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.update(['am', 'is', 'are', 'was', 'were',
                                'be', 'being', 'been', 'to', 'the', 'a', 'an'])

    def english_to_isl(self, text: str) -> list[str]:
        """
        Converts English text into ISL-compatible word list.
        E.g. "I am going to school" -> ["I", "GO", "SCHOOL"]
        """
        if not text:
            return []
        words = word_tokenize(text.lower())
        isl_words = []
        for word in words:
            if not word.isalnum():                          # Remove punctuation
                continue
            if word in self.stop_words and \
               word not in ['i', 'we', 'you', 'he', 'she', 'they', 'it']:
                continue                                    # Remove stopwords, keep pronouns
            root_word = self.lemmatizer.lemmatize(word, pos='v')  # Lemmatize as verb
            isl_words.append(root_word.upper())
        return isl_words
```

---

## A.6 Video Mapping — Dual-Directory Dataset Lookup

Each ISL word is matched against video files in two directories (primary ISL_Dataset, fallback dataset). Unmatched words are marked for fingerspelling fallback.

**File: backend/main.py**

```python
    mapped_videos = []
    for word in isl_words:
        word_clean = word.lower()
        primary_path = ISL_DATASET_DIR / f"{word_clean}.mp4"
        fallback_path = DATASET_DIR / f"{word_clean}.mp4"

        if primary_path.exists():
            mapped_videos.append({
                "word": word.upper(),
                "video_url": f"/api/video/{word_clean}?source=isl",
                "found": True
            })
        elif fallback_path.exists():
            mapped_videos.append({
                "word": word.upper(),
                "video_url": f"/api/video/{word_clean}?source=dummy",
                "found": True
            })
        else:
            mapped_videos.append({
                "word": word.upper(), "video_url": None, "found": False
            })
```

---

## A.7 Frontend — Audio Recording with RecordRTC

The browser captures Tamil speech as PCM WAV audio at 16kHz mono using RecordRTC. On stop, the blob is automatically submitted for processing.

**File: frontend/app.js**

```javascript
async function startRecording() {
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });

    recordRTC = RecordRTC(mediaStream, {
        type: 'audio',
        mimeType: 'audio/wav',
        recorderType: StereoAudioRecorder,
        desiredSampRate: 16000,
        numberOfAudioChannels: 1    // Mono for speech recognition
    });
    recordRTC.startRecording();
    isRecording = true;
}

function stopRecording() {
    recordRTC.stopRecording(function () {
        audioBlob = recordRTC.getBlob();

        // Release microphone
        mediaStream.getTracks().forEach(track => track.stop());
        mediaStream = null;

        sequenceStartTime = performance.now();  // Start latency timer

        const file = new File([audioBlob], "recorded_audio.wav",
                              { type: 'audio/wav' });
        processAudioFile(file);
    });
}
```

---

## A.8 Frontend — API Call and Response Handling

The audio file is sent to the backend as multipart form-data via the Fetch API. On success, the pipeline UI is updated and video playback begins.

**File: frontend/app.js**

```javascript
async function processAudioFile(file) {
    processingLoader.classList.remove('hidden');
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/process-audio', {
            method: 'POST',
            body: formData
        });
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Server error");
        }
        const data = await response.json();
        updatePipelineUI(data);
        startVideoSequence(data.video_sequence);
    } catch (err) {
        showError(err.message);
    } finally {
        processingLoader.classList.add('hidden');
    }
}
```

---

## A.9 Frontend — Sequential Video Playback with onended

The playNextVideo function recursively plays ISL sign videos using the HTML5 video element's onended event. Missing words trigger a fingerspelling fallback displayed for 1.5 seconds.

**File: frontend/app.js**

```javascript
function playNextVideo() {
    if (currentVideoIndex >= videoSequence.length) {
        videoPlayer.pause();
        progressFill.style.width = '100%';
        return;  // Sequence complete
    }

    const currentItem = videoSequence[currentVideoIndex];

    // Update UI: highlight ISL tag, progress bar, word overlay
    sequenceCounter.textContent =
        `${currentVideoIndex + 1} / ${videoSequence.length}`;
    progressFill.style.width =
        `${((currentVideoIndex + 1) / videoSequence.length) * 100}%`;

    if (currentItem.found && currentItem.video_url) {
        // Play sign video
        currentWordOverlay.textContent = currentItem.word;
        avatarImage.src = `/api/avatar/${currentItem.word.toLowerCase()}`;

        videoPlayer.src = currentItem.video_url;
        videoPlayer.load();
        videoPlayer.play();

        // Chain to next video when current one ends
        videoPlayer.onended = () => {
            currentVideoIndex++;
            playNextVideo();
        };
    } else {
        // Fingerspelling fallback: show word for 1.5 seconds
        currentWordOverlay.textContent = `[Spell] ${currentItem.word}`;
        setTimeout(() => {
            currentVideoIndex++;
            playNextVideo();
        }, 1500);
    }
}
```

---

## A.10 Video and Avatar Serving Endpoints

These endpoints serve individual sign video files and 2D avatar pose images from the dataset directories.

**File: backend/main.py**

```python
@app.get("/api/video/{word}")
async def get_video(word: str, source: str = "dummy"):
    word_clean = word.lower()
    if source == "isl":
        video_path = ISL_DATASET_DIR / f"{word_clean}.mp4"
    else:
        video_path = DATASET_DIR / f"{word_clean}.mp4"
    if video_path.exists():
        return FileResponse(path=str(video_path), media_type="video/mp4")
    raise HTTPException(status_code=404, detail="Video not found")


@app.get("/api/avatar/{word}")
async def get_avatar(word: str):
    word_clean = word.lower()
    avatar_path = DATASET_DIR / "2d_avatars" / f"avatar_{word_clean}.png"
    if avatar_path.exists():
        return FileResponse(path=str(avatar_path), media_type="image/png")
    raise HTTPException(status_code=404, detail="Avatar not found")


# Mount frontend static files (must be last to avoid route shadowing)
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True),
          name="frontend")
```

