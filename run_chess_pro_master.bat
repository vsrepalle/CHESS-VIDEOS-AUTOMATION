@echo off
setlocal enabledelayedexpansion
title Chess Pro Automation Master Controller

:: --- ENVIRONMENT SETUP ---
set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

:MENU
echo.
echo ======================================================
echo       CHESS PRO AUTOMATION - MASTER CONTROLLER
echo ======================================================
echo  1. Process Tournament Brochures (OCR -^> JSON)
echo  2. Process FEN Puzzles (JSON -^> Board Images)
echo  3. Generate Shorts (Video Rendering)
echo  4. Upload to YouTube (Batch Uploader)
echo  5. RUN FULL PIPELINE (1 through 4)
echo  6. Exit
echo ======================================================
echo  Working Directory: %CD%
echo ======================================================
set /p choice="Select an option (1-6): "

if "%choice%"=="1" goto TOURNAMENT
if "%choice%"=="2" goto FEN
if "%choice%"=="3" goto GENERATE
if "%choice%"=="4" goto UPLOAD
if "%choice%"=="5" goto FULL
if "%choice%"=="6" goto EXIT
goto MENU

:TOURNAMENT
echo.
echo ------------------------------------------------------
echo [INFO] Step 1: Running OCR Extractor...
if not exist "scripts\extractor\main.py" (
    echo [ERROR] Missing script: scripts\extractor\main.py
    goto MENU
)

python scripts/extractor/main.py

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] OCR Script failed.
    goto MENU
) else (
    echo [SUCCESS] OCR Processing complete.
    if "%choice%"=="1" (
        echo [AUTO-CHAIN] Moving to Step 3: Video Generation...
        goto GENERATE
    )
)
if "%choice%"=="5" goto FEN
goto MENU

:FEN
echo.
echo ------------------------------------------------------
echo [INFO] Step 2: Processing FEN strings...
python scripts/generator/src/video/fen_processor.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] FEN Processor failed.
    goto MENU
)
if "%choice%"=="5" goto GENERATE
goto MENU

:GENERATE
echo.
echo ------------------------------------------------------
echo [INFO] Step 3: Rendering Short Videos...
python scripts/generator/main.py

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Video Rendering failed.
    goto MENU
) else (
    echo [SUCCESS] Videos rendered successfully.
    echo [INFO] Syncing files to output\videos...
    if exist "output\previews\*.mp4" move /y "output\previews\*.mp4" "output\videos\" >nul
    if exist "output\previews\*.json" move /y "output\previews\*.json" "output\videos\" >nul
)
if "%choice%"=="5" goto UPLOAD
goto MENU

:UPLOAD
echo.
echo ------------------------------------------------------
echo [INFO] Step 4: Upload Options
echo  A. Auto-Upload ALL from output\videos
echo  B. Manually choose file (File Explorer)
echo ------------------------------------------------------
set /p up_choice="Select upload mode (A/B): "

if /i "%up_choice%"=="B" (
    python scripts/generator/src/youtube/youtube_batch_uploader.py --manual
) else (
    python scripts/generator/src/youtube/youtube_batch_uploader.py
)

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Upload session encountered errors.
) else (
    echo [SUCCESS] Upload and Cleanup finished.
)
goto MENU

:FULL
echo [SYSTEM] Starting Full Pipeline Mode...
goto TOURNAMENT

:EXIT
exit