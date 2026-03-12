import os
import sys
import json
from datetime import datetime
from pathlib import Path

# --- ENVIRONMENT SETUP ---
# Ensure the project root is in the path for module imports
PROJECT_ROOT = r"C:\VISWA\CHESS_PRO_AUTOMATION"
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from scripts.generator.src.video.short_video_generator import generate_short_video

# --- DIRECTORY CONFIGURATION ---
# We look for metadata in the output folder where Step 1 (OCR) saves them
METADATA_DIR = os.path.join(PROJECT_ROOT, "output", "videos")
# We look for the original images in the extractor's input folder
IMAGE_SOURCE_DIR = os.path.join(PROJECT_ROOT, "scripts", "extractor", "input")
# Output & Assets
AUDIO_PATH = os.path.join(PROJECT_ROOT, "assets", "music", "background_track.mp3")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "previews")

def log(msg):
    """Standardized logging with timestamp."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def run_pipeline():
    # 1. Verification and Setup
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if not os.path.exists(METADATA_DIR):
        log(f"❌ Error: Metadata directory not found: {METADATA_DIR}")
        return

    # 2. Collect all JSON files (projects) from the central folder
    metadata_files = [f for f in os.listdir(METADATA_DIR) if f.lower().endswith(".json")]

    if not metadata_files:
        log("⚠️ No metadata JSONs found in output/videos. Please run Step 1 (OCR) first.")
        return

    log(f"🎬 Found {len(metadata_files)} project(s) to render.")

    # 3. Process each project individually
    for json_name in metadata_files:
        project_stem = os.path.splitext(json_name)[0]  # e.g., 'brochure1'
        json_path = os.path.join(METADATA_DIR, json_name)
        
        # Load the Metadata
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            log(f"❌ Error reading {json_name}: {e}")
            continue

        # 4. Find the matching image for this project
        # We check common extensions in the extractor's input folder to find the source image
        found_images = []
        for ext in [".jpg", ".jpeg", ".png"]:
            img_path = os.path.join(IMAGE_SOURCE_DIR, project_stem + ext)
            if os.path.exists(img_path):
                found_images.append(img_path)
                break  # Use the first matching image file found

        if not found_images:
            log(f"⚠️ Skipping {project_stem}: No matching image found in {IMAGE_SOURCE_DIR}")
            continue

        # 5. Execute Video Generation
        try:
            log(f"🧵 Rendering: {project_stem}...")
            
            # Use 'filename' as the keyword to match the updated generator signature
            video_path = generate_short_video(
                data=data, 
                audio_path=AUDIO_PATH, 
                images=found_images, 
                output_dir=OUTPUT_DIR, 
                filename=f"{project_stem}.mp4"
            )
            
            log(f"✅ Success! Generated: {os.path.basename(video_path)}")
            
        except Exception as e:
            log(f"❌ Render Error for {project_stem}: {e}")

if __name__ == "__main__":
    run_pipeline()