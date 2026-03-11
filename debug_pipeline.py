import os
import subprocess
import time
from datetime import datetime

# --- Configuration ---
ROOT = r"C:\VISWA\CHESS_PRO_AUTOMATION"
GEN_SCRIPT = os.path.join(ROOT, r"scripts\generator\src\video\short_video_generator.py")
# Test FEN (Morphy's)
TEST_FEN = "kbK5/pp6/1P6/8/8/8/8/R7 w - - 0 1"
TEST_NAME = "debug_test_video"

def run_debug():
    print("="*50)
    print(f"DEBUGGER START: {datetime.now()}")
    print("="*50)
    
    print(f"[DEBUG] Working Directory: {os.getcwd()}")
    print(f"[DEBUG] Script Path: {GEN_SCRIPT}")
    
    # 1. Capture snapshot of files BEFORE running
    files_before = set()
    for root, _, filenames in os.walk(ROOT):
        for f in filenames:
            files_before.add(os.path.join(root, f))

    print(f"[DEBUG] Launching Generator Subprocess...")
    print("-" * 30)
    
    try:
        # We run it and capture ALL output (stdout and stderr)
        result = subprocess.run(
            ["python", GEN_SCRIPT, "--fen", TEST_FEN, "--name", TEST_NAME],
            capture_output=True,
            text=True,
            check=True
        )
        print("[GENERATOR OUTPUT]:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("[!] GENERATOR CRASHED:")
        print(e.stderr)
        return

    print("-" * 30)
    print("[DEBUG] Generator finished. Searching for new files...")

    # 2. Capture snapshot AFTER and find the difference
    files_after = set()
    for root, _, filenames in os.walk(ROOT):
        for f in filenames:
            files_after.add(os.path.join(root, f))

    new_files = files_after - files_before

    if not new_files:
        print("[RESULT] No new files were created anywhere in the ROOT folder.")
    else:
        print(f"[RESULT] Found {len(new_files)} new file(s):")
        for nf in new_files:
            print(f"  -> LOCATION: {nf}")
            if nf.endswith(".mp4"):
                print("  **** FOUND THE VIDEO! ****")

    print("="*50)

if __name__ == "__main__":
    run_debug()