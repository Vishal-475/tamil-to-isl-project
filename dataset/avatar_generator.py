import cv2
import numpy as np
import os
import hashlib
from pathlib import Path

# Expanded vocabulary of ~160 words common in basic communication and stories
WORDS = [
    # Original
    "i", "go", "school", "hello", "thank_you", "name", "my", "you", "love", "please", "yes", "no", 
    "good", "morning", "help", "water", "friend", "teacher", "learn", "eat", "sleep", "happy", "sad", 
    "mother", "father", "beautiful", "change", "college", "computer", "day", "distance", "engineer", 
    "fight", "finish", "great", "home", "language", "laugh", "see", "sign", "sing", "sound", "stay", 
    "study", "talk", "television", "time", "walk", "wash", "work", "how", "what", "when", "where", 
    "why", "who", "which", "can", "cannot", "welcome", "after", "again", "all", "alone", "ask", 
    "best", "better", "busy", "but", "bye", "come", "do", "god", "keep", "more",
    
    # New additions for story and general conversation (bringing total > 150)
    "elias", "oldest", "clockmaker", "town", "know", "fix", "clock", "others", "deem", "beyond",
    "repair", "one", "rainy", "season", "young", "man", "bring", "small", "break", "locket", "word",
    "tick", "decades", "explain", "it", "belong", "late", "grandmother", "pick", "wristwatch", "surprise",
    "precision", "weak", "hand", "open", "case", "back", "find", "gear", "intricate", "fold",
    "note", "hide", "inside", "mechanism", "instead", "he", "poor", "thing", "clean", "rust",
    "exterior", "girl", "gossip", "treasure", "design", "memories", "rather", "tell", "little", "box",
    "saw", "map", "garden", "eye", "bloom", "wildflowers", "she", "understand", "watch", "need",
    "precious", "lead", "new", "begin", "heirloom", "true", "purpose", "ilyas", "pass", "moments",
    "people", "we", "believe", "share", "always", "never", "sometimes", "today", "tomorrow", "yesterday",
    "book", "read", "write", "paper", "pen", "pencil", "sit", "stand", "run", "jump", "door", "window",
    "sun", "moon", "star", "tree", "flower", "grass", "bird", "dog", "cat", "fish", "food", "drink", "car"
]

def generate_avatars():
    base_dir = Path(__file__).resolve().parent.parent
    input_img_path = base_dir / "frontend" / "avatar.png"
    out_dir = base_dir / "dataset" / "2d_avatars"
    
    out_dir.mkdir(parents=True, exist_ok=True)
    
    if not input_img_path.exists():
        print(f"Error: Base image not found at {input_img_path}")
        return

    # Load base image
    base_img = cv2.imread(str(input_img_path), cv2.IMREAD_UNCHANGED)
    if base_img is None:
        print("Failed to load image correctly.")
        return
        
    # Convert BGRA to BGR if transparency exists, otherwise just use it
    if base_img.shape[2] == 4:
        # Create white background
        white_bg = np.ones_like(base_img[:,:,:3]) * 255
        alpha = base_img[:,:,3] / 255.0
        for c in range(3):
            white_bg[:,:,c] = (alpha * base_img[:,:,c] + (1 - alpha) * white_bg[:,:,c])
        base_img = white_bg.astype(np.uint8)

    height, width, _ = base_img.shape
    
    print(f"Generating {len(set(WORDS))} avatars in {out_dir}...")
    
    for word in set(WORDS):
        # Create a copy of the base image
        img = base_img.copy()
        
        # Create a hash of the word to deterministically generate hand positions
        word_hash = int(hashlib.md5(word.encode()).hexdigest(), 16)
        
        # Center of chest area loosely (approximate for typical portraits)
        center_x = width // 2
        center_y = int(height * 0.6)
        
        # Offset hands based on hash to simulate different signs uniquely
        offset_x1 = (word_hash % 120) - 60
        offset_y1 = ((word_hash // 100) % 80) - 40
        offset_x2 = ((word_hash // 10000) % 120) - 60
        offset_y2 = ((word_hash // 1000000) % 80) - 40
        
        # Stylized hands (circles with slight transparency overlay on image)
        overlay = img.copy()
        cv2.circle(overlay, (center_x + offset_x1 - 50, center_y + offset_y1), 25, (0, 200, 255), -1)
        cv2.circle(overlay, (center_x + offset_x2 + 50, center_y + offset_y2), 25, (0, 255, 200), -1)
        
        # Blend overlay (glassmorphism effect over the body)
        cv2.addWeighted(overlay, 0.4, img, 0.6, 0, img)
        
        # Add stylized Word Tag at bottom
        tag_bg_color = (30, 30, 30)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        thickness = 2
        
        text = f"SIGN: {word.upper()}"
        (t_w, t_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        
        tag_x = (width - t_w) // 2
        tag_y = height - 30
        
        # Draw background rect with slight padding
        cv2.rectangle(img, (tag_x - 15, tag_y - t_h - 15), (tag_x + t_w + 15, tag_y + baseline + 10), tag_bg_color, -1)
        
        # Draw text
        cv2.putText(img, text, (tag_x, tag_y), font, font_scale, (255, 255, 255), thickness)
        
        # Save output
        out_path = out_dir / f"avatar_{word.lower()}.png"
        cv2.imwrite(str(out_path), img)
        
    print(f"Successfully generated {len(set(WORDS))} distinct avatars!")

if __name__ == "__main__":
    generate_avatars()
