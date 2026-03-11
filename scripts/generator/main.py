import os
import sys
import json
from datetime import datetime

# Path Configuration
PROJECT_ROOT = r"C:\VISWA\CHESS_PRO_AUTOMATION"
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from scripts.generator.src.video.short_video_generator import generate_short_video

DUMP_ZONE = os.path.join(PROJECT_ROOT, "dump_zone")
AUDIO_PATH = os.path.join(PROJECT_ROOT, "assets", "music", "background_track.mp3")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "previews")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def run_pipeline():
    # 1. Detect Active Project Folder
    target_folder, content_type = None, None
    for t in ["puzzle", "tournament"]:
        base_path = os.path.join(DUMP_ZONE, t)
        if os.path.exists(base_path):
            # Check for subdirectories (e.g., dump_zone/tournament/TournamentName)
            subs = [os.path.join(base_path, d) for d in os.listdir(base_path) 
                    if os.path.isdir(os.path.join(base_path, d))]
            if subs:
                target_folder, content_type = subs[0], t
                break

    if not target_folder:
        log("No project folders found in dump_zone/puzzle or dump_zone/tournament.")
        sys.exit(1)

    # 2. Collect Images and JSON
    json_file = None
    brochures = []
    for f in sorted(os.listdir(target_folder)):
        path = os.path.join(target_folder, f)
        if f.lower().endswith(".json"):
            json_file = path
        elif f.lower().endswith((".jpg", ".jpeg", ".png")):
            brochures.append(path)

    if not brochures:
        log("❌ Error: No images found in folder.")
        sys.exit(1)

    # 3. Load Metadata
    data = {}
    if json_file:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            log(f"⚠️ JSON load error: {e}")

    # Default Puzzle Metadata
    if content_type == "puzzle":
        data.setdefault("headline", "daily chess puzzle")
        data.setdefault("hook_text", "white to move and win!")
        data.setdefault("prize", "bragging rights")

    # 4. Generate Video
    try:
        log(f"Processing {content_type}: {os.path.basename(target_folder)}")
        video_path = generate_short_video(data, AUDIO_PATH, brochures, OUTPUT_DIR)
        log(f"✅ Success! Generated: {video_path}")
    except Exception as e:
        log(f"❌ Render Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
    