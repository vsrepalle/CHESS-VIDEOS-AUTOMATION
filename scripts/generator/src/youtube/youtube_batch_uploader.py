import os
import glob
import subprocess
import argparse
import tkinter as tk
from tkinter import filedialog

VIDEO_DIR = r"output\videos"
SINGLE_UPLOADER = r"scripts\generator\src\youtube\youtube_uploader.py"

def get_file_path(title, file_types):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    init_dir = os.path.abspath(VIDEO_DIR)
    file_path = filedialog.askopenfilename(title=title, filetypes=file_types, initialdir=init_dir)
    root.destroy()
    return file_path

def run_batch_upload(manual_mode=False):
    to_process = []
    if manual_mode:
        print("[PROMPT] Opening File Explorer...")
        video_path = get_file_path("Select Video to Upload", [("Video files", "*.mp4")])
        if not video_path: return
            
        abs_video = os.path.abspath(video_path)
        json_path = os.path.splitext(abs_video)[0] + ".json"
        
        if os.path.exists(json_path):
            to_process.append((abs_video, json_path))
        else:
            print(f"❌ Error: JSON not found!")
            print(f"   Expected: {os.path.basename(json_path)}")
            print(f"   In folder: {os.path.dirname(json_path)}")
            return
    else:
        video_files = glob.glob(os.path.join(VIDEO_DIR, "*.mp4"))
        for v in video_files:
            j = os.path.splitext(v)[0] + ".json"
            if os.path.exists(j):
                to_process.append((os.path.abspath(v), os.path.abspath(j)))

    for video, metadata in to_process:
        print(f"\n🚀 UPLOADING: {os.path.basename(video)}")
        cmd = ["python", SINGLE_UPLOADER, "--video", video, "--json", metadata]
        result = subprocess.run(cmd)
        if result.returncode == 0:
            os.remove(video)
            os.remove(metadata)
            print(f"🗑️ Cleaned up: {os.path.basename(video)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manual", action="store_true")
    args = parser.parse_args()
    run_batch_upload(manual_mode=args.manual)