@echo off
title CHESS PRO: ZOOM 45s PREVIEW MODE
setlocal enabledelayedexpansion
CLS

:: Targeted Python 3.13 Installation
SET PY_EXE="C:\Users\viswa\AppData\Local\Programs\Python\Python313\python.exe"

echo ============================================================
echo   ♟️  STARTING CHESS PIPELINE (45s ZOOM + PREVIEW)
echo ============================================================

:: 1. Organize
echo [1/4] ORGANIZING DUMP_ZONE...
%PY_EXE% scripts\drive_sync.py

:: 2. Render
echo [2/4] RENDERING 45s ZOOM VIDEO...
:: Note: This uses MoviePy 2.1.2 as verified in diagnostics
%PY_EXE% scripts\generator\main.py

:: 3. Preview and Upload
echo [3/4] OPENING PREVIEW and WAITING FOR APPROVAL...
:: Videos will be uploaded as PRIVATE by default
%PY_EXE% scripts\generator\src\youtube\youtube_batch_uploader.py

:: 4. Archive (Only runs if folders exist)
echo [4/4] ARCHIVING...
%PY_EXE% -c "from scripts.drive_sync import archive_processed; archive_processed()"

echo.
echo ============================================================
echo ✅ SESSION COMPLETE (Sequential Mode Active)
echo ============================================================
pause