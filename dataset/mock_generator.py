import cv2 # type: ignore # pyre-ignore
import numpy as np # type: ignore # pyre-ignore
import os
from pathlib import Path

# Words to generate mock signs for
WORDS = [
    "i", "go", "school", "hello", "thank_you", "name", "my", "you", "love", "please", "yes", "no", 
    "good", "morning", "help", "water", "friend", "teacher", "learn", "eat", "sleep", "happy", "sad", 
    "mother", "father",
    "beautiful", "change", "college", "computer", "day", "distance", "engineer", "fight", "finish", 
    "great", "home", "language", "laugh", "see", "sign", "sing", "sound", "stay", "study", "talk", 
    "television", "time", "walk", "wash", "work",
    "how", "what", "when", "where", "why", "who", "which", "can", "cannot", "welcome",
    "after", "again", "all", "alone", "ask", "best", "better", "busy", "but", "bye", "come", "do", "god", "keep", "more"
]

# Colors for different words
COLORS = [
    (0, 0, 255), (0, 255, 0), (255, 0, 0),
    (0, 255, 255), (255, 0, 255), (255, 255, 0), (255, 255, 255)
]

def create_mock_video(word, output_path, color):
    # Video properties
    width, height = 640, 480
    fps = 30
    duration_sec = 2
    total_frames = fps * duration_sec
    
    # Define codec and create VideoWriter
    # Using mp4v which works well for standard mp4 output via OpenCV
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    for frame_idx in range(total_frames):
        # Create a black image
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Draw a moving shape (mocking a hand gesture)
        # Move back and forth
        x = int(width/2 + np.sin(frame_idx * 0.1) * 100)
        y = int(height/2 + np.cos(frame_idx * 0.1) * 50)
        
        cv2.circle(frame, (x, y), 50, color, -1)
        
        # Put the word text on the video
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = f"SIGN: {word.upper()}"
        text_size = cv2.getTextSize(text, font, 1.5, 3)[0]
        text_x = (width - text_size[0]) // 2
        text_y = height - 50
        cv2.putText(frame, text, (text_x, text_y), font, 1.5, (255, 255, 255), 3)
        
        # Write frame
        out.write(frame)
        
    out.release()
    print(f"Created mock video: {output_path}")

def generate_dataset():
    base_dir = Path(__file__).resolve().parent
    print(f"Generating mock dataset in {base_dir}...")
    
    for i, word in enumerate(WORDS):
        output_path = base_dir / f"{word}.mp4"
        if output_path.exists():
            print(f"Skipping {word}, already exists.")
            continue
        color = COLORS[i % len(COLORS)]
        create_mock_video(word, output_path, color)
        
if __name__ == "__main__":
    generate_dataset()
