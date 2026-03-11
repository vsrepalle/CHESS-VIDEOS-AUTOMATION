import os
import subprocess
import glob
import json
import shutil

# ============================================================
# PATH CONFIGURATION (Matched to your Tree)
# ============================================================
ROOT_DIR = r"C:\VISWA\CHESS_PRO_AUTOMATION"
# This is where your my_puzzle.json lives
PUZZLE_SOURCE_DIR = os.path.join(ROOT_DIR, "fen_short_puzzle")
# This is where the generator scripts expect to find data
FEN_INPUT_DIR = os.path.join(ROOT_DIR, r"scripts\generator\input\FEN")

RENDERER_SCRIPT = os.path.join(ROOT_DIR, r"scripts\generator\src\video\board_renderer.py")
VIDEO_GEN_SCRIPT = os.path.join(ROOT_DIR, r"scripts\generator\src\video\short_video_generator.py")
OUTPUT_DIR = os.path.join(ROOT_DIR, r"output\videos")

def process_puzzle(data, original_json_path):
    puzzle_name = data.get("name", "untitled_puzzle")
    fen = data.get("fen")
    
    print(f"\n--- 🎬 STARTING: {puzzle_name} ---")

    # STEP 1: RENDER THE BOARD IMAGE
    # board_renderer.py creates the PNG in output\rendered_boards
    render_cmd = ["python", RENDERER_SCRIPT, "--fen", fen, "--output", puzzle_name]
    subprocess.run(render_cmd)

    # STEP 2: GENERATE THE VIDEO
    video_output_path = os.path.join(OUTPUT_DIR, f"{puzzle_name}.mp4")
    
    video_cmd = [
        "python", VIDEO_GEN_SCRIPT,
        "--fen", fen,
        "--metadata", original_json_path,
        "--output", video_output_path
    ]
    subprocess.run(video_cmd)
    
    # STEP 3: SAVE YOUTUBE METADATA (UTF-8) for the Uploader
    if "youtube_metadata" in data and os.path.exists(video_output_path):
        metadata_file = os.path.join(OUTPUT_DIR, f"{puzzle_name}.json")
        with open(metadata_file, 'w', encoding="utf-8") as f:
            json.dump(data["youtube_metadata"], f, indent=4, ensure_ascii=False)
        print(f"[METADATA] Saved YouTube info to: {puzzle_name}.json")

def run_pipeline():
    # Ensure directories exist
    os.makedirs(FEN_INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"[SEARCHING] Checking {PUZZLE_SOURCE_DIR} for my_puzzle.json...")
    
    source_file = os.path.join(PUZZLE_SOURCE_DIR, "my_puzzle.json")
    
    if not os.path.exists(source_file):
        print(f"[!] Critical Error: {source_file} not found!")
        return

    # Load and process the file
    with open(source_file, 'r', encoding="utf-8") as f:
        try:
            content = json.load(f)
        except Exception as e:
            print(f"[ERROR] JSON Read Error: {e}")
            return
    
    # Handle list of puzzles
    if isinstance(content, list):
        print(f"[BATCH] Found {len(content)} puzzles in my_puzzle.json")
        for item in content:
            # Create a temporary single-puzzle JSON for the generator to read
            temp_name = item.get('name', 'temp_puz')
            temp_json = os.path.join(FEN_INPUT_DIR, f"{temp_name}.json")
            
            with open(temp_json, 'w', encoding="utf-8") as tf:
                json.dump(item, tf, ensure_ascii=False)
            
            process_puzzle(item, temp_json)
            
            # Clean up temp file
            if os.path.exists(temp_json): 
                os.remove(temp_json)
    else:
        process_puzzle(content, source_file)

if __name__ == "__main__":
    run_pipeline()