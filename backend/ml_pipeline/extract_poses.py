import os
import cv2
import json
import urllib.request
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from pathlib import Path

# Paths mapping to your project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASET_DIR = BASE_DIR / "dataset"
OUT_DIR = DATASET_DIR / "poses"
os.makedirs(OUT_DIR, exist_ok=True)

MODEL_DIR = Path(__file__).resolve().parent / "models"
os.makedirs(MODEL_DIR, exist_ok=True)

POSE_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task"
HAND_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
POSE_MODEL_PATH = MODEL_DIR / "pose_landmarker.task"
HAND_MODEL_PATH = MODEL_DIR / "hand_landmarker.task"

def download_models():
    if not POSE_MODEL_PATH.exists():
        print("Downloading Pose Landmarker Model...")
        urllib.request.urlretrieve(POSE_MODEL_URL, POSE_MODEL_PATH)
    if not HAND_MODEL_PATH.exists():
        print("Downloading Hand Landmarker Model...")
        urllib.request.urlretrieve(HAND_MODEL_URL, HAND_MODEL_PATH)

def extract_landmarks(pose_result, hand_result):
    # Pose: 33 landmarks -> 132 elements (x,y,z,visibility)
    if pose_result and pose_result.pose_landmarks:
        pose = np.array([[l.x, l.y, l.z, l.visibility] for l in pose_result.pose_landmarks[0]]).flatten()
    else:
        pose = np.zeros(33 * 4)

    # Hand: 21 landmarks -> up to 2 hands (Left, Right)
    lh = np.zeros(21 * 3)
    rh = np.zeros(21 * 3)
    
    if hand_result and hand_result.hand_landmarks:
        for i, handedness in enumerate(hand_result.handedness):
            label = handedness[0].category_name # "Left" or "Right"
            landmarks = np.array([[l.x, l.y, l.z] for l in hand_result.hand_landmarks[i]]).flatten()
            if label == "Left": lh = landmarks
            elif label == "Right": rh = landmarks
            
    return np.concatenate([pose, lh, rh]).tolist()

def process_video(video_path, out_file):
    print(f"Processing Video: {video_path.name}")
    
    # Initialize Landmarkers
    base_options_pose = python.BaseOptions(model_asset_path=str(POSE_MODEL_PATH))
    options_pose = vision.PoseLandmarkerOptions(base_options=base_options_pose, running_mode=vision.RunningMode.IMAGE)
    
    base_options_hand = python.BaseOptions(model_asset_path=str(HAND_MODEL_PATH))
    options_hand = vision.HandLandmarkerOptions(base_options=base_options_hand, running_mode=vision.RunningMode.IMAGE, num_hands=2)

    frames_data = []
    
    with vision.PoseLandmarker.create_from_options(options_pose) as pose_landmarker, \
         vision.HandLandmarker.create_from_options(options_hand) as hand_landmarker:
         
        cap = cv2.VideoCapture(str(video_path))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
            
            # Predict
            pose_res = pose_landmarker.detect(mp_image)
            hand_res = hand_landmarker.detect(mp_image)
            
            keypoints = extract_landmarks(pose_res, hand_res)
            frames_data.append(keypoints)
            
        cap.release()
        
    with open(out_file, 'w') as f:
        json.dump(frames_data, f)
    print(f"-> Saved {len(frames_data)} frames of math data to {out_file.name}\n")

if __name__ == "__main__":
    print("=====================================")
    print("    ISL Pose Extraction Pipeline     ")
    print("=====================================\n")
    download_models()
    
    print(f"Scanning for videos in {DATASET_DIR}...")
    video_files = list(DATASET_DIR.glob("*.mp4"))
    if not video_files:
        print("No videos found! Please add real videos of humans signing.")
    else:
        for video_file in video_files:
            process_video(video_file, OUT_DIR / f"{video_file.stem}.json")
        print("Pose extraction completely finished!")
