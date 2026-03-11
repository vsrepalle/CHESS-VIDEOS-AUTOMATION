import os
import glob
import subprocess
import argparse
import tkinter as tk
from tkinter import filedialog

VIDEO_DIR = r"C:\VISWA\CHESS_PRO_AUTOMATION\output\videos"
SINGLE_UPLOADER = r"C:\VISWA\CHESS_PRO_AUTOMATION\scripts\generator\src\youtube\youtube_uploader.py"

def get_file_path(title, file_types):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    file_path = filedialog.askopenfilename(title=title, filetypes=file_types, initialdir=VIDEO_DIR)
    root.destroy()
    return file_path

def run_batch_upload(manual_video=None, manual_json=None):
    to_process = []

    if manual_video == "PICKER":
        print("[PROMPT] Opening File Explorer for Video...")
        manual_video = get_file_path("Select Chess Video (MP4)", [("Video files", "*.mp4")])
        
        if manual_video:
            # Smart Auto-Find JSON logic
            potential_json = os.path.splitext(manual_video)[0] + ".json"
            if os.path.exists(potential_json):
                print(f"[AUTO-FOUND] Found matching metadata: {os.path.basename(potential_json)}")
                manual_json = potential_json
            else:
                print("[PROMPT] No matching JSON found. Select manually...")
                manual_json = get_file_path("Select Metadata (JSON)", [("JSON files", "*.json")])

    if manual_video and manual_json:
        to_process.append((manual_video, manual_json))
    else:
        print(f"[AUTO] Scanning {VIDEO_DIR} for content...")
        video_files = glob.glob(os.path.join(VIDEO_DIR, "*.mp4"))
        for v in video_files:
            j = os.path.splitext(v)[0] + ".json"
            if os.path.exists(j):
                to_process.append((v, j))

    if not to_process:
        print("[!] No valid video/metadata pairs found.")
        return

    for video_path, json_path in to_process:
        print(f"\n🚀 STARTING UPLOAD: {os.path.basename(video_path)}")
        # Call the core uploader
        cmd = ["python", SINGLE_UPLOADER, "--video", video_path, "--json", json_path]
        subprocess.run(cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", help="Video path or 'PICKER'")
    parser.add_argument("--json", help="JSON path")
    args = parser.parse_args()
    run_batch_upload(args.video, args.json) 