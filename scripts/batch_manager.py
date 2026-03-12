import os
import subprocess
import shutil
from datetime import datetime

PROJECT_ROOT = r"C:\VISWA\CHESS_PRO_AUTOMATION"
VIDEO_DIR = os.path.join(PROJECT_ROOT, "output", "videos")
SOURCE_BASE_DIR = os.path.join(PROJECT_ROOT, "dump_zone", "tournaments")
UPLOAD_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "uploader", "upload_to_youtube.py")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def purge_project(project_name):
    log(f"🧹 Cleaning up: {project_name}")
    # Remove rendered files
    for ext in [".mp4", ".json"]:
        f = os.path.join(VIDEO_DIR, f"{project_name}{ext}")
        if os.path.exists(f): os.remove(f)
    # Remove source brochures
    src = os.path.join(SOURCE_BASE_DIR, project_name)
    if os.path.exists(src): shutil.rmtree(src)

def run_uploader():
    if not os.path.exists(VIDEO_DIR): return
    videos = [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith(".mp4")]

    for video_file in videos:
        proj = os.path.splitext(video_file)[0]
        v_path = os.path.join(VIDEO_DIR, video_file)
        j_path = os.path.join(VIDEO_DIR, f"{proj}.json")

        if not os.path.exists(j_path): continue

        log(f"📤 Uploading {proj}...")
        # Call the actual uploader script
        result = subprocess.run(["python", UPLOAD_SCRIPT, "--video", v_path, "--metadata", j_path])

        if result.returncode == 0:
            log(f"🌟 {proj} uploaded successfully!")
            purge_project(proj)
        else:
            log(f"❌ Upload failed for {proj}. Files preserved.")

if __name__ == "__main__":
    run_uploader()