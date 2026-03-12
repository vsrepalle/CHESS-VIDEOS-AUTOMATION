import os
import numpy as np
import moviepy as mp
from moviepy.video import fx as vfx
from icrawler.builtin import GoogleImageCrawler

# --- setup paths ---
PROJECT_ROOT = r"C:\VISWA\CHESS_PRO_AUTOMATION"
IMAGE_DUMP = os.path.join(PROJECT_ROOT, "dump_zone", "player_images")

def fetch_player_face(player_name):
    """safely attempts to download a face, returning none on failure."""
    if not player_name or player_name.lower() in ["unknown", "composition"]:
        return None
    
    player_dir = os.path.join(IMAGE_DUMP, player_name.replace(" ", "_").lower())
    os.makedirs(player_dir, exist_ok=True)
    
    # 1. check for local manual override first
    for ext in ['jpg', 'png', 'jpeg']:
        local_path = os.path.join(player_dir, f"000001.{ext}")
        if os.path.exists(local_path):
            return local_path

    # 2. attempt crawling with a soft-fail try/except
    try:
        google_crawler = GoogleImageCrawler(storage={'root_dir': player_dir})
        google_crawler.crawl(keyword=f"{player_name} chess portrait", max_num=1)
        for ext in ['jpg', 'png', 'jpeg']:
            path = os.path.join(player_dir, f"000001.{ext}")
            if os.path.exists(path):
                return path
    except Exception:
        pass
    return None

def make_circle_mask(size):
    """creates a circular mask with integer dimensions."""
    w, h = int(size[0]), int(size[1])
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    xx, yy = np.meshgrid(x, y)
    mask = (xx**2 + yy**2 <= 1).astype(float)
    return mask

def create_chess_short(board_video_path, player_name, hook_text, output_path):
    """overlays portrait and hook text in safe zones (outside the chess board)."""
    if not os.path.exists(board_video_path):
        print(f"❌ input video missing: {board_video_path}")
        return

    base_clip = mp.VideoFileClip(board_video_path)
    clips = [base_clip]

    # 1. render hook text (top margin safe zone)
    if hook_text:
        try:
            txt_w = int(base_clip.w * 0.9)
            txt_clip = mp.TextClip(
                text=hook_text.lower(),
                font_size=50,
                color='white',
                bg_color='black',
                method='caption',
                size=(txt_w, None)
            ).with_duration(5).with_position(('center', 150)).with_start(0.5)
            # y=150 ensures it stays above the 1080p centered board
            clips.append(txt_clip)
        except Exception as e:
            print(f"⚠️ text overlay error: {e}")

    # 2. render player portrait (bottom margin safe zone)
    img_path = fetch_player_face(player_name)
    if img_path:
        try:
            face_clip = mp.ImageClip(img_path).with_duration(base_clip.duration)
            w, h = face_clip.size
            min_dim = int(min(w, h))
            
            # crop to square
            face_clip = vfx.crop(face_clip, x_center=int(w/2), y_center=int(h/2), 
                                 width=min_dim, height=min_dim)
            
            # resize and apply mask
            portrait_size = 220
            face_clip = face_clip.resized(height=portrait_size)
            mask_data = make_circle_mask((portrait_size, portrait_size))
            face_clip = face_clip.with_mask(mp.ImageClip(mask_data, ismask=True))
            
            # position at bottom-right (below the 1080p board)
            face_clip = face_clip.with_position((800, 1600))
            clips.append(face_clip)
        except Exception as e:
            print(f"⚠️ portrait processing error: {e}")

    # 3. composite and export
    try:
        final_video = mp.CompositeVideoClip(clips, size=base_clip.size)
        if base_clip.audio:
            final_video = final_video.with_audio(base_clip.audio)
        
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    except Exception as e:
        print(f"🔥 composite render failure: {e}")
    finally:
        base_clip.close()
        if 'final_video' in locals(): final_video.close()