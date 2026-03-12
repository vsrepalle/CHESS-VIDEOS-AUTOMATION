import os
import sys
import json
import shutil
import time
from datetime import datetime
from PIL import Image
from google import genai

PROJECT_ROOT = r"C:\VISWA\CHESS_PRO_AUTOMATION"
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from scripts.generator.src.video.short_video_generator import generate_short_video
# New import for the overlay logic
from scripts.generator.src.video.create_chess_short import create_chess_short

# Replace with your actual API Key
client = genai.Client(api_key="AIzaSyBKpgiIJ-XWDEf4yefrVlAfVj4TrCa_2Zw")

TOURNAMENT_BASE_DIR = os.path.join(PROJECT_ROOT, "dump_zone", "tournaments")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "videos")
AUDIO_PATH = os.path.join(PROJECT_ROOT, "assets", "music", "background_track.mp3")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def extract_metadata_with_vision(image_path, retries=2):
    """Uses Gemini 1.5 Flash (Fixed Typo) to extract brochure data."""
    for i in range(retries + 1):
        try:
            img = Image.open(image_path)
            prompt = """
            Analyze this chess tournament brochure. Return ONLY a JSON object with:
            'tournament_name': A punchy title.
            'prize_pool': Total prizes mentioned.
            'hook_text': A 1-sentence YouTube hook.
            'details': 2-sentence summary of location/date.
            'white_player': The name of the main featured player if mentioned, else 'unknown'.
            """
            # TYPO FIXED: gemini-1.5-flash
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=[prompt, img]
            )
            
            json_text = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(json_text)
            
        except Exception as e:
            if "429" in str(e) and i < retries:
                log(f"⏳ Rate limit. Retrying in 15s ({i+1}/{retries})...")
                time.sleep(15)
                continue
            log(f"⚠️ Vision failed: {e}")
            return None

def run_pipeline():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    folders = [d for d in os.listdir(TOURNAMENT_BASE_DIR) 
               if os.path.isdir(os.path.join(TOURNAMENT_BASE_DIR, d))]

    if not folders:
        log("⚠️ No folders found in tournaments directory.")
        return

    for folder_name in folders:
        folder_path = os.path.join(TOURNAMENT_BASE_DIR, folder_name)
        
        # Check for any valid image format
        images = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) 
                         if f.lower().endswith((".jpg", ".png", ".jpeg", ".webp"))])
        
        if not images:
            log(f"❓ Skipping {folder_name}: No images found in folder.")
            continue

        log(f"🧠 Analyzing brochure for: {folder_name}...")
        data = extract_metadata_with_vision(images[0])
        
        if not data:
            log(f"⚠️ Fallback activated for {folder_name}.")
            data = {
                "tournament_name": folder_name.replace("_", " ").title(), 
                "details": "New Tournament Alert!", 
                "hook_text": "Check out the details!",
                "white_player": "unknown"
            }

        try:
            log(f"🧵 Rendering base video for {folder_name}...")
            temp_video_name = f"temp_{folder_name}.mp4"
            temp_video_path = os.path.join(OUTPUT_DIR, temp_video_name)
            final_video_path = os.path.join(OUTPUT_DIR, f"{folder_name}.mp4")

            # 1. Generate the standard board video
            generate_short_video(data=data, audio_path=AUDIO_PATH, images=images, output_dir=OUTPUT_DIR, filename=temp_video_name)
            
            # 2. Add the player image overlay
            player_name = data.get("white_player", "unknown")
            log(f"👤 Adding portrait overlay for: {player_name}...")
            create_chess_short(temp_video_path, player_name, final_video_path)
            
            # 3. Save metadata and cleanup temp file
            with open(os.path.join(OUTPUT_DIR, f"{folder_name}.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
                
            log(f"✅ Created artifacts for {folder_name}")
            time.sleep(2) # Prevent burst limits
            
        except Exception as e:
            log(f"❌ Render Error: {e}")

if __name__ == "__main__":
    run_pipeline()