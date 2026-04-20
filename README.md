# Tamil Speech to ISL Translation  System

A real-time translation system that takes Tamil speech (via microphone or file upload), translates it into English, converts the English text into an Indian Sign Language (ISL) grammatical structure, and dynamically plays back a sequence of corresponding sign language videos.

This project uses a FastAPI backend for text processing and audio handling, and a lightweight Vanilla JS frontend for video playback and UI.

## Features
- **Real-Time  Recording**: Record Tamil speech directly from the browser.
- **Audio Uploads**: Upload standard `.wav` or `.mp3` files for translation.
- **Full NLP Pipeline**: Tamil Speech $\to$ Tamil Text $\to$ English Translation $\to$ ISL format conversion.
- **Dynamic Video Stitching**: Maps processed ISL words directly to a local dataset folder and plays them smoothly in sequence.
- **Fingerspelling Fallback**: If a dataset video is missing for a generated word, the system automatically falls back to displaying the text explicitly.

## Project Structure
```
project_root/
│
├── backend/
│   ├── modules/
│   │   └── nlp_processor.py    # NLTK-based ISL grammar conversion rules
│   ├── main.py                 # FastAPI application and endpoint definitions
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── index.html              # Main UI structure
│   ├── style.css               # Styling (dark theme, modern aesthetic)
│   └── app.js                  # Audio recording and video sequencing logic
│
└── dataset/
    └── mock_generator.py       # Script to generate dummy signs for testing
```

## Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.9+ installed and pip available.

### 2. Install Dependencies
Open a terminal in the project root and navigate to the backend folder to install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

*Note: For Windows, ensure you have basic C++ build tools installed if `pyaudio` or `SpeechRecognition` gives any issues, although this project uses fundamental fallback mechanics where possible.*

### 3. Generate Mock Dataset
To demonstrate the functionality, generate the local dummy video dataset by running:
```bash
python dataset/mock_generator.py
```
This will generate files like `i.mp4`, `go.mp4`, `school.mp4` in the `dataset/` directory.

### 4. Start the Application
From the project root directory, run the FastAPI server:
```bash
uvicorn backend.main:app --reload
```

### 5. Access the Web App
Open your browser and navigate to:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

## How it Works
1. When you click **Start Recording**, the browser captures your mic in WebM/WAV format.
2. The UI sends this file to the `/api/process-audio` endpoint.
3. **Backend Phase 1**: Extracts Tamil text using SpeechRecognition.
4. **Backend Phase 2**: Translates Tamil text to English using GoogleTranslator.
5. **Backend Phase 3**: Drops English stopwords, lemmatizes verbs, and converts to uppercase ISL structure (e.g., "I am going to school" $\to$ `[I, GO, SCHOOL]`).
6. **Backend Phase 4**: Searches the `/dataset/` fold to find `.mp4` matching the words and returns URLs.
7. **Frontend**: Receives the response and updates the UI tags. The video player automatically loads the sequence URLs and uses `onended` events to chain the gesture clips seamlessly. 

## Dataset Customization
Simply place your actual `.mp4` files inside the `dataset/` directory named exactly as the lower-case English root word (e.g. `school.mp4`, `hello.mp4`). The backend maps automatically ignoring case.
