import os
import subprocess
import glob
import json

# PATH CONFIGURATION
FEN_INPUT_DIR = r"C:\VISWA\CHESS_PRO_AUTOMATION\scripts\generator\input\FEN"
RENDERER_SCRIPT = r"C:\VISWA\CHESS_PRO_AUTOMATION\scripts\generator\src\video\board_renderer.py"
VIDEO_GEN_SCRIPT = r"C:\VISWA\CHESS_PRO_AUTOMATION\scripts\generator\src\video\short_video_generator.py"
OUTPUT_DIR = r"C:\VISWA\CHESS_PRO_AUTOMATION\output\videos"

def process_puzzle(data, original_json_path):
    puzzle_name = data.get("name", "untitled_puzzle")
    fen = data.get("fen")
    
    print(f"\n--- 🎬 STARTING: {puzzle_name} ---")

    # STEP 1: RENDER THE BOARD IMAGE
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
    
    # STEP 3: SAVE YOUTUBE METADATA (UTF-8)
    if "youtube_metadata" in data and os.path.exists(video_output_path):
        metadata_file = os.path.join(OUTPUT_DIR, f"{puzzle_name}.json")
        # Added encoding="utf-8" here
        with open(metadata_file, 'w', encoding="utf-8") as f:
            json.dump(data["youtube_metadata"], f, indent=4, ensure_ascii=False)
        print(f"[METADATA] Saved YouTube info to: {puzzle_name}.json")

def run_pipeline():
    print(f"[SEARCHING] Looking for puzzles in {FEN_INPUT_DIR}...")
    json_files = glob.glob(os.path.join(FEN_INPUT_DIR, "*.json"))
    
    for json_path in json_files:
        # Added encoding="utf-8" here to fix your error
        with open(json_path, 'r', encoding="utf-8") as f:
            try:
                content = json.load(f)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Could not read {json_path}: {e}")
                continue
        
        if isinstance(content, list):
            print(f"[BATCH] Processing {len(content)} puzzles...")
            for item in content:
                temp_json = os.path.join(FEN_INPUT_DIR, f"temp_{item.get('name', 'puzzle')}.json")
                # Use utf-8 for temp files too
                with open(temp_json, 'w', encoding="utf-8") as tf:
                    json.dump(item, tf, ensure_ascii=False)
                
                process_puzzle(item, temp_json)
                
                if os.path.exists(temp_json):
                    os.remove(temp_json)
        else:
            process_puzzle(content, json_path)

if __name__ == "__main__":
    run_pipeline()