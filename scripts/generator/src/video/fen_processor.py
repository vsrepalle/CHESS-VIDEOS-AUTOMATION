import os
from .board_renderer import render_fen_to_png

def process_single_fen(fen_text, video_id):
    # Ensure the path is relative to the PROJECT_ROOT or absolute
    # Based on your structure, we navigate to scripts/generator/output/rendered_boards
    output_dir = os.path.join("scripts", "generator", "output", "rendered_boards")
    
    # Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    img_path = os.path.abspath(os.path.join(output_dir, f"{video_id}.png"))

    # 1. Generate the Image using your board_renderer
    try:
        render_fen_to_png(fen_text, img_path)
        print(f"Board image created at: {img_path}")
        
        # 2. Return the path so pipeline_runner.py knows where the image is
        return img_path
        
    except Exception as e:
        print(f"Error rendering FEN: {e}")
        return None