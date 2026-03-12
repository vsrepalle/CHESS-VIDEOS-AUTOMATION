import chess
import chess.svg
import cairosvg
import os
import argparse
from datetime import datetime

def render_fen_to_png(fen_string, output_path):
    """converts a fen string into a high-res png board using cairosvg."""
    try:
        board = chess.Board(fen_string)
        
        # generate svg with modern colors for a premium look
        svg_data = chess.svg.board(
            board=board,
            size=1080,
            coordinates=True,
            lastmove=board.peek() if board.move_stack else None,
            check=board.king(board.turn) if board.is_check() else None,
            colors={
                'square light': '#dee3e6',
                'square dark': '#8ca2ad',
                'margin': '#262626',
                'coord': '#ffffff'
            }
        )

        cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=output_path)
        print(f"[success] board rendered to: {output_path}")
        return True
    except Exception as e:
        print(f"[error] board_renderer failed: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="render fen to png")
    parser.add_argument("--fen", required=True)
    parser.add_argument("--output", help="filename without extension")
    args = parser.parse_args()

    render_dir = r"C:\VISWA\CHESS_PRO_AUTOMATION\dump_zone\chess_boards"
    os.makedirs(render_dir, exist_ok=True)

    filename = f"{args.output.lower()}.png" if args.output else f"fen_{datetime.now().strftime('%H%M%S')}.png"
    render_fen_to_png(args.fen, os.path.join(render_dir, filename))