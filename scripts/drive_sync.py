import os
import shutil
from datetime import datetime

DUMP_ZONE = r"C:\VISWA\CHESS_PRO_AUTOMATION\dump_zone"
BASE_DIR = r"C:\VISWA\CHESS_PRO_AUTOMATION"
ARCHIVE_DIR = os.path.join(BASE_DIR, r"scripts\generator\archive")

def organize_dump_zone():
    print(f"📂 Checking {DUMP_ZONE} for new brochures...")
    if not os.path.exists(DUMP_ZONE):
        os.makedirs(DUMP_ZONE)
        return

    files = [f for f in os.listdir(DUMP_ZONE) if os.path.isfile(os.path.join(DUMP_ZONE, f))]
    
    for f in files:
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.mp4')):
            # Logic: V_Chess_Academy -> V_C
            parts = f.split('_')
            folder_name = f"{parts[0]}_{parts[1][0]}" if len(parts) > 1 else "Misc_Chess"
            target_path = os.path.join(BASE_DIR, folder_name)
            
            os.makedirs(target_path, exist_ok=True)
            shutil.move(os.path.join(DUMP_ZONE, f), os.path.join(target_path, f))
            print(f"✅ Organized: {f} -> {folder_name}")

def archive_processed():
    print("📦 Archiving processed tournaments...")
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    # PROTECT ASSETS: Added 'assets' and 'archive' to exclude
    exclude = ['dump_zone', 'scripts', 'output', '.git', 'venv', 'archive', 'assets']
    
    folders = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d)) and d not in exclude]

    for folder in folders:
        source = os.path.join(BASE_DIR, folder)
        destination = os.path.join(ARCHIVE_DIR, folder)
        
        if os.path.exists(destination):
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            destination = f"{destination}_{stamp}"
        
        try:
            shutil.move(source, destination)
            print(f"✅ Archived {folder} to {os.path.basename(destination)}")
        except Exception as e:
            print(f"⚠️ Archive failed for {folder}: {e}")

if __name__ == "__main__":
    import sys
    # If run without args, organize; if run with 'archive', archive.
    if len(sys.argv) > 1 and sys.argv[1] == 'archive':
        archive_processed()
    else:
        organize_dump_zone()