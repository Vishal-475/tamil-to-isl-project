from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import speech_recognition as sr
from deep_translator import GoogleTranslator
import os
import shutil
import tempfile
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import split_on_silence
import imageio_ffmpeg

AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe()

from backend.modules.nlp_processor import ISLConverter

app = FastAPI(title="Tamil Speech to ISL")

# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
recognizer = sr.Recognizer()
translator = GoogleTranslator(source='ta', target='en')
isl_converter = ISLConverter()

# Config paths
BASE_DIR = Path(__file__).resolve().parent.parent
ISL_DATASET_DIR = BASE_DIR / "ISL_Dataset"
DATASET_DIR = BASE_DIR / "dataset"
FRONTEND_DIR = BASE_DIR / "frontend"

print(f"Dataset Dir: {DATASET_DIR}")
print(f"Frontend Dir: {FRONTEND_DIR}")

# We will mount static files at the end to avoid catching API routes early.


@app.post("/api/process-audio")
async def process_audio(file: UploadFile = File(...)):
    """
    Main pipeline endpoint:
    1. Speech to Text (Tamil)
    2. Translate to English
    3. NLP conversion to ISL grammar
    4. Map to Dataset videos
    """
    if not file.filename.endswith((".wav", ".mp3", ".ogg", ".flac", ".webm", ".m4a")):
         raise HTTPException(status_code=400, detail="Unsupported audio format")

    try:
        # Create a temporary file to store the uploaded audio
        original_suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=original_suffix) as temp_audio:
            shutil.copyfileobj(file.file, temp_audio)
            temp_audio_path = temp_audio.name

        wav_audio_path = temp_audio_path + "_converted.wav"

        try:
            # Convert audio to pure 16kHz mono WAV using ffmpeg directly
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            import subprocess
            subprocess.run([
                ffmpeg_exe, 
                "-y", 
                "-i", temp_audio_path, 
                "-ac", "1", 
                "-ar", "16000", 
                wav_audio_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Use the converted file for recognition
            target_audio_path = wav_audio_path
        except Exception as e:
            print(f"Format conversion error: {e}")
            target_audio_path = temp_audio_path # Fallback to original

        try:
            # We will use pydub to load the target audio natively
            full_audio = AudioSegment.from_file(target_audio_path)
            
            # Split the audio on silence into chunks to bypass API payload limits
            chunks = split_on_silence(
                full_audio,
                min_silence_len=500, # split on silences > 0.5 sec
                silence_thresh=full_audio.dBFS - 16, # considering anything 16 dB below avg as silence
                keep_silence=250 # retain some silence to avoid clipping words
            )
            
            # Fallback for audios with absolutely no silence
            if not chunks:
               chunks = [full_audio]
            
            tamil_text_results = []
            
            for i, chunk in enumerate(chunks):
                # Generate a temporary file path safely for Windows
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    chunk_file_path = tmp_file.name
                    
                # Now that it's closed by the "with" block, we can export the chunk
                chunk.export(chunk_file_path, format="wav")
                
                try:
                    with sr.AudioFile(chunk_file_path) as source:
                        audio_data = recognizer.record(source)
                        
                    chunk_text = recognizer.recognize_google(audio_data, language="ta-IN")
                    tamil_text_results.append(chunk_text)
                    print(f"Chunk {i} recognized: {chunk_text}")
                except sr.UnknownValueError:
                    print(f"Chunk {i}: Silence or incomprehensible speech. Skipping.")
                except sr.RequestError as e:
                    print(f"Chunk {i}: API Error - {e}")
                finally:
                    # Clean up chunk to save disk space
                    if os.path.exists(chunk_file_path):
                        os.remove(chunk_file_path)
            
            if not tamil_text_results:
                raise HTTPException(status_code=400, detail="Speech could not be understood or audio contains no speech.")
                
            tamil_text = " ".join(tamil_text_results)
            print(f"Fully Recognized Tamil: {tamil_text}")
            
        except HTTPException as he:
            raise he
        except Exception as e:
             raise HTTPException(status_code=400, detail=f"Error processing audio content: {e}. Please use a standard audio format.")

        # 2. Translation (Tamil -> English)
        english_text = translator.translate(tamil_text)
        print(f"Translated English: {english_text}")

        # 3. ISL Grammar Conversion
        isl_words = isl_converter.english_to_isl(english_text)
        print(f"ISL Words: {isl_words}")

        # 4. Map to Videos
        mapped_videos = []
        for word in isl_words:
            word_clean = word.lower()
            
            # 1. Try to find a matching video in the custom ISL_Dataset folder first
            primary_path = ISL_DATASET_DIR / f"{word_clean}.mp4"
            # 2. If not found in custom, fallback to dummy dataset folder
            fallback_path = DATASET_DIR / f"{word_clean}.mp4"
            
            if primary_path.exists():
                mapped_videos.append({"word": word.upper(), "video_url": f"/api/video/{word_clean}?source=isl", "found": True})
            elif fallback_path.exists():
                mapped_videos.append({"word": word.upper(), "video_url": f"/api/video/{word_clean}?source=dummy", "found": True})
            else:
                mapped_videos.append({"word": word.upper(), "video_url": None, "found": False})

        # Cleanup temp files
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        if 'wav_audio_path' in locals() and os.path.exists(wav_audio_path):
            os.remove(wav_audio_path)

        return JSONResponse(content={
            "tamil_text": tamil_text,
            "english_text": english_text,
            "isl_words": [w["word"] for w in mapped_videos],
            "video_sequence": mapped_videos
        })

    except HTTPException as he:
        # Forward HTTP Exceptions directly
        raise he
    except Exception as e:
        print(f"Pipeline Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: str({e})")


@app.get("/api/video/{word}")
async def get_video(word: str, source: str = "dummy"):
    """
    Serves the dataset video for a given ISL word.
    Resolves source parameter to determine which folder to serve from.
    """
    word_clean = word.lower()
    
    if source == "isl":
        video_path = ISL_DATASET_DIR / f"{word_clean}.mp4"
    else:
        video_path = DATASET_DIR / f"{word_clean}.mp4"
        
    if video_path.exists():
         return FileResponse(path=str(video_path), media_type="video/mp4")
    else:
         raise HTTPException(status_code=404, detail="Video not found in dataset")


@app.get("/api/avatar/{word}")
async def get_avatar(word: str):
    """
    Serves the 2D avatar image for a given ISL word.
    """
    word_clean = word.lower()
    avatar_path = DATASET_DIR / "2d_avatars" / f"avatar_{word_clean}.png"
    
    if avatar_path.exists():
         return FileResponse(path=str(avatar_path), media_type="image/png")
    else:
         raise HTTPException(status_code=404, detail="Avatar not found in dataset")


# Mount static files for frontend (serves index.html and assets)
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
