import chess
import chess.svg
import cairosvg
import os
import argparse
from datetime import datetime

def render_fen_to_png(fen_string, output_path):
    """
    Converts a FEN string into a high-res PNG board.
    """
    try:
        # 1. Initialize the board
        board = chess.Board(fen_string)
        
        # 2. Generate SVG 
        svg_data = chess.svg.board(
            board=board,
            size=1080,
            coordinates=True,
            lastmove=board.peek() if board.move_stack else None,
            check=board.king(board.turn) if board.is_check() else None
        )

        # 3. Convert SVG to PNG
        cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=output_path)
        print(f"[SUCCESS] Board rendered to: {output_path}")
        return True
    except Exception as e:
        print(f"[ERROR] board_renderer failed: {e}")
        return False

# ------------------------------------------------
# COMMAND LINE INTERFACE (The Missing Brain)
# ------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render FEN to PNG")
    parser.add_argument("--fen", required=True, help="The FEN string of the board")
    parser.add_argument("--output", help="Name of the output file (without extension)")
    
    args = parser.parse_args()

    # Define the directory where images MUST go so the video generator finds them
    render_dir = r"C:\VISWA\CHESS_PRO_AUTOMATION\scripts\generator\output\rendered_boards"
    os.makedirs(render_dir, exist_ok=True)

    # Create filename: use provided name or timestamp
    filename = f"{args.output}.png" if args.output else f"fen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    final_save_path = os.path.join(render_dir, filename)

    # Run the render
    render_fen_to_png(args.fen, final_save_path)