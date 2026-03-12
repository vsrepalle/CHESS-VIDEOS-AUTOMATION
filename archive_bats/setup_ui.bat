@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   ♟️  PROVISIONING CHESS PIPELINE
echo ========================================

:: 1. Create the Drive Sync Script
echo [INFO] Creating scripts\drive_sync.py...
(
echo import os
echo import subprocess
echo from pathlib import Path
echo.
echo # Paths based on your tree structure
echo BASE_DIR = Path(__file__^).resolve(^).parent.parent
echo LOCAL_INPUT = BASE_DIR / "scripts" / "generator" / "input"
echo.
echo def sync_from_drive(^):
echo     print("🚀 Pulling latest brochures from Google Drive (Remote: gdrive)..."^)
echo     # Using rclone to pull from 'Chess_Brochures' folder on Drive
echo     try:
echo         # Syncs Drive folder to your local generator input
echo         subprocess.run(["rclone", "copy", "gdrive:Chess_Brochures", str(LOCAL_INPUT^), "-P"], check=True^)
echo     except Exception as e:
echo         print(f"❌ Drive Sync Failed: {e}. Ensure rclone is configured as 'gdrive'."^)
echo         return
echo.
echo     # ORGANIZER LOGIC: Convert 'TournamentName_YYYY-MM-DD.jpg' into structured folders
echo     for file in LOCAL_INPUT.glob("*.jp*g"^):
echo         if "_" in file.stem:
echo             parts = file.stem.split("_"^)
echo             name = parts[0]
echo             # Expects YYYY-MM-DD as the second part
echo             date = parts[1] if len(parts^) ^> 1 else "Undated"
echo.            
echo             # Folder format: YYYY-MM-DD_TournamentName for chronological sorting
echo             folder_name = f"{date}_{name}"
echo             target_dir = LOCAL_INPUT / folder_name
echo             target_dir.mkdir(exist_ok=True^)
echo.
echo             # Find current page count to avoid overwriting
echo             existing = len(list(target_dir.glob("page_*.jp*g"^)^)^)
echo             new_path = target_dir / f"page_{existing + 1}{file.suffix}"
echo             file.rename(new_path^)
echo             print(f"📂 Organized: {file.name} -^> {folder_name}/page_{existing + 1}"^)
echo.
echo if __name__ == "__main__":
echo     sync_from_drive(^)
) > scripts\drive_sync.py

:: 2. Create the Sequential Master Runner
echo [INFO] Creating run_all.bat...
(
echo @echo off
echo title CHESS PRO AUTOMATION PIPELINE
echo CLS
echo echo ==============================================
echo echo   ♟️  STARTING SEQUENTIAL CHESS PIPELINE
echo echo ==============================================
echo.
echo echo [STEP 1/3] SYNCING FROM GOOGLE DRIVE...
echo python scripts\drive_sync.py
echo.
echo echo [STEP 2/3] EXTRACTING DATA (AI OCR^)...
echo python scripts\extractor\main.py
echo.
echo echo [STEP 3/3] RENDERING VIDEOS (PAN/ZOOM/SCROLL^)...
echo python scripts\generator\main.py
echo.
echo echo ==============================================
echo echo ✅ ALL TASKS COMPLETED SUCCESSFULLY
echo echo ==============================================
echo pause
) > run_all.bat

echo.
echo ========================================
echo ✅ PIPELINE SCRIPTS READY!
echo.
echo 1. Ensure 'rclone' is in your PATH.
echo 2. Run 'rclone config' and name your Drive remote 'gdrive'.
echo 3. Put files in Drive as: TournamentName_YYYY-MM-DD.jpg
echo 4. Run 'run_all.bat' to start the process.
echo ========================================
pause