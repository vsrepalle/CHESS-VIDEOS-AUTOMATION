import os
import sys
from datetime import datetime

# Add root to sys.path
PROJECT_ROOT = r"C:\VISWA\CHESS_PRO_AUTOMATION"
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from scripts.generator.src.video.fen_processor import process_single_fen
from scripts.generator.src.video.short_video_generator import generate_short_video

# Setup Test Data
TEST_FEN = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
TEST_ID = "test_run_001"
AUDIO_PATH = os.path.join(PROJECT_ROOT, "assets", "music", "background_track.mp3")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "previews")

def quick_test():
    print("?? Starting FEN-to-Short Test...")
    
    # 1. Process FEN to Image
    img_path = process_single_fen(TEST_FEN, TEST_ID)
    if not img_path or not os.path.exists(img_path):
        print(f"? Failed to render board image. Path tried: {img_path}")
        return

    # 2. Metadata for the Video
    video_data = {
        "headline": "CHESS OPENING TRAP",
        "hook_text": "White to play. Can you find the win?",
        "prize": "GM Analysis"
    }

    # 3. Generate the Video
    try:
        final_video = generate_short_video(video_data, AUDIO_PATH, [img_path], OUTPUT_DIR)
        print(f"? SUCCESS! Video saved at: {final_video}")
    except Exception as e:
        print(f"? Video generation failed: {e}")

if __name__ == "__main__":
    quick_test()
