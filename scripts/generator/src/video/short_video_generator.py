import os
import numpy as np
import logging
import json
import glob
import argparse
from datetime import datetime
from PIL import Image
from thefuzz import process

# MoviePy 2.0+ Core Imports
from moviepy import ImageClip, TextClip, ColorClip, AudioFileClip, CompositeVideoClip
import moviepy.video.fx as vfx

# ------------------------------------------------
# CONFIGURATION & CONSTANTS
# ------------------------------------------------
SHORT_DURATION = 15 
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def log(msg):
    logging.info(msg)

# ------------------------------------------------
# UTILS & EXTRACTION
# ------------------------------------------------
def intelligent_extract(data, intent, default="n/a"):
    intent_map = {
        "location": ["venue", "location", "place", "address", "hall"],
        "prize": ["prize", "total prize", "prize pool"],
        "fee": ["fee", "entry fee", "registration"],
        "headline": ["headline", "title", "name", "tournament_name"]
    }
    keys = list(data.keys())
    if not keys: return default

    for keyword in intent_map.get(intent, []):
        best, score = process.extractOne(keyword, keys)
        if score > 85:
            return str(data[best]).upper() 
    return default

def normalize_audio(audio_path, duration):
    audio = AudioFileClip(audio_path)
    if audio.duration > duration:
        return audio.subclipped(0, duration)
    return audio.with_duration(duration)

def apply_ken_burns(clip, duration):
    def zoom(t):
        return 1 + 0.12 * (t / duration)
    return (clip.with_duration(duration)
            .resized(zoom)
            .with_position(("center", "center")))

# ------------------------------------------------
# MAIN GENERATOR
# ------------------------------------------------
def generate_short_video(data, audio_path, images, output_dir, filename="short_video.mp4"):
    """
    Core function to render the video. 
    Argument 'filename' matches the main.py caller exactly.
    """
    log(f"🚀 RENDERING {len(images)} PAGES INTO VIDEO...")
    os.makedirs(output_dir, exist_ok=True)
    
    W, H, FPS = (1080, 1920, 30)
    output_file = os.path.join(output_dir, filename)

    # 1. Background Layers
    page_duration = SHORT_DURATION / len(images)
    background_clips = []
    
    for i, path in enumerate(images):
        img_raw = Image.open(path).convert("RGB")
        img_w, img_h = img_raw.size
        aspect_ratio = img_w / img_h
        
        base_clip = ImageClip(np.array(img_raw)).with_duration(page_duration)
        
        if 0.9 <= aspect_ratio <= 1.1:
            base_clip = base_clip.resized(width=W)
            bg_fill = ColorClip(size=(W, H), color=(0,0,0)).with_duration(page_duration)
            base_clip = CompositeVideoClip([bg_fill, base_clip.with_position("center")])
        else:
            base_clip = base_clip.resized(height=H)
            base_clip = base_clip.cropped(x_center=base_clip.w/2, y_center=H/2, width=W, height=H)
        
        page_clip = apply_ken_burns(base_clip, page_duration).with_start(i * page_duration)
        if i > 0: 
            page_clip = page_clip.with_effects([vfx.CrossFadeIn(0.5)])
        background_clips.append(page_clip)

    # 2. Overlays
    shadow = (ColorClip(size=(W, 480), color=(0,0,0)).with_opacity(0.65)
              .with_duration(SHORT_DURATION).with_position(("center", "bottom")))
    
    title_text = intelligent_extract(data, "headline", "CHESS TOURNAMENT")
    prize_text = intelligent_extract(data, "prize", "")
    header_str = f"{title_text}\n{prize_text}" if prize_text and prize_text != "N/A" else title_text

    header_info = (TextClip(text=header_str, font_size=85, color="yellow", 
                            font=r"C:\Windows\Fonts\arialbd.ttf", 
                            method="caption", size=(W-100, None))
                   .with_duration(SHORT_DURATION).with_position(("center", 150)))

    # 3. Subtitles
    texts = []
    if "hook_text" in data: texts.append(data["hook_text"])
    if "details" in data: texts.extend([s.strip() for s in str(data["details"]).split(".") if s.strip()][:2])
    
    subtitle_clips = []
    if texts:
        sub_dur = SHORT_DURATION / len(texts)
        for i, txt in enumerate(texts):
            c = (TextClip(text=txt.lower(), font_size=60, color="white", stroke_color="black", stroke_width=2,
                          font=r"C:\Windows\Fonts\arialbd.ttf", method="caption", size=(W-150, None))
                 .with_duration(sub_dur).with_start(i * sub_dur).with_position(("center", H - 350)))
            c = c.with_effects([vfx.CrossFadeIn(0.3)])
            subtitle_clips.append(c)

    # 4. Branding
    watermark = (TextClip(text="@CHESS_PRO_AI", font_size=40, color="white", 
                          font=r"C:\Windows\Fonts\arial.ttf")
                 .with_opacity(0.4)
                 .with_duration(SHORT_DURATION)
                 .with_position(("right", "bottom")))
    
    cta = (TextClip(text="Subscribe to find out more", font_size=60, color="white", bg_color="red",
                    font=r"C:\Windows\Fonts\arialbd.ttf", method="caption", size=(W, 150))
           .with_start(SHORT_DURATION - 3).with_duration(3).with_position(("center", "center")))

    # 5. Assembly
    layers = background_clips + [shadow, header_info, watermark, cta] + subtitle_clips
    final_video = CompositeVideoClip(layers, size=(W, H)).with_audio(normalize_audio(audio_path, SHORT_DURATION))

    final_video.write_videofile(output_file, fps=FPS, codec="libx264", audio_codec="aac", threads=1, logger='bar')
    final_video.close()
    return output_file

# ------------------------------------------------
# SAFE ENTRY POINT
# ------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", help="Path to JSON metadata")
    parser.add_argument("--output", help="Final video output path")
    parser.add_argument("--brochures", nargs="+", help="Paths to image files")
    args = parser.parse_args()

    audio_track = r"C:\VISWA\CHESS_PRO_AUTOMATION\assets\music\background_track.mp3"
    final_data = {}
    
    if args.metadata and os.path.exists(args.metadata):
        with open(args.metadata, 'r', encoding="utf-8") as f:
            final_data = json.load(f)

    if args.brochures:
        out_path = args.output if args.output else os.path.join(r"C:\VISWA\CHESS_PRO_AUTOMATION\output\videos", "short_video.mp4")
        generate_short_video(
            data=final_data,
            audio_path=audio_track,
            images=args.brochures,
            output_dir=os.path.dirname(out_path),
            filename=os.path.basename(out_path)
        )