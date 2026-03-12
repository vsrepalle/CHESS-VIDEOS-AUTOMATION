import os
import sys
import json
from datetime import datetime
import moviepy as mp

# absolute path setup
PROJECT_ROOT = r"C:\VISWA\CHESS_PRO_AUTOMATION"
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# dynamic import to handle both module and direct script execution
try:
    from scripts.generator.src.video.board_renderer import render_fen_to_png
    from scripts.generator.src.video.create_chess_short import create_chess_short
except ImportError:
    import board_renderer
    import create_chess_short
    render_fen_to_png = board_renderer.render_fen_to_png
    create_chess_short = create_chess_short.create_chess_short

INPUT_JSON = os.path.join(PROJECT_ROOT, "scripts", "extractor", "input", "puzzles.json")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "videos")
DUMP_DIR = os.path.join(PROJECT_ROOT, "dump_zone")
AUDIO_FILE = os.path.join(PROJECT_ROOT, "assets", "music", "background_track.mp3")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def process_pipeline():
    if not os.path.exists(INPUT_JSON):
        log(f"❌ missing input: {INPUT_JSON}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(DUMP_DIR, "chess_boards"), exist_ok=True)

    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        puzzles = json.load(f)

    for puzzle in puzzles:
        name = puzzle.get("name", "short").lower()
        log(f"➡️ processing: {name}")

        board_img = os.path.join(DUMP_DIR, "chess_boards", f"{name}.png")
        render_fen_to_png(puzzle.get("fen"), board_img)

        temp_mp4 = os.path.join(DUMP_DIR, f"temp_{name}.mp4")
        # 10 second duration for shorts
        clip = mp.ImageClip(board_img).with_duration(10)
        if os.path.exists(AUDIO_FILE):
            audio = mp.AudioFileClip(AUDIO_FILE).with_duration(10)
            clip = clip.with_audio(audio)
        
        clip.write_videofile(temp_mp4, fps=24, codec="libx264", audio_codec="aac")
        clip.close()

        final_mp4 = os.path.join(OUTPUT_DIR, f"{name}.mp4")
        create_chess_short(temp_mp4, puzzle.get("white_player", "unknown"), puzzle.get("hook_text", ""), final_mp4)

        if os.path.exists(final_mp4):
            log(f"✅ success: {final_mp4}")
            # generate metadata json for uploader
            with open(final_mp4.replace(".mp4", ".json"), 'w', encoding='utf-8') as j:
                json.dump(puzzle, j, indent=4)
            if os.path.exists(temp_mp4): os.remove(temp_mp4)

if __name__ == "__main__":
    process_pipeline()