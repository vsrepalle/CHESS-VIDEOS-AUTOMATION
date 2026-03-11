@echo off
setlocal enabledelayedexpansion

:MENU
cls
echo ==================================================
echo       CHESS PRO AUTOMATION - MASTER MENU
echo ==================================================
echo  1. FULL PIPELINE (AI Generate -^> Render)
echo  2. MANUAL PUZZLE (Import my_puzzle.json -^> Render)
echo  3. RENDER ONLY  (Process files already in FEN folder)
echo  4. YOUTUBE UPLOAD (Auto-Scan or Manual Picker)
echo  5. DEBUG SYSTEM (Check Environment ^& Paths)
echo  6. EXIT
echo ==================================================
set /p choice="Select an option (1-6): "

if "%choice%"=="1" goto FULL_PIPELINE
if "%choice%"=="2" goto MANUAL_IMPORT
if "%choice%"=="3" goto RENDER_ONLY
if "%choice%"=="4" goto UPLOAD_ONLY
if "%choice%"=="5" goto DEBUG
if "%choice%"=="6" exit

:MANUAL_IMPORT
echo [RUNNING] Manual Import and Pipeline...
python pipeline_runner.py
pause
goto MENU

:UPLOAD_ONLY
cls
echo ==================================================
echo             YOUTUBE UPLOAD SETTINGS
echo ==================================================
echo  1. UPLOAD ALL (Scan output\videos - Default)
echo  2. MANUAL PICKER (Open File Explorer)
echo  3. BACK TO MENU
echo ==================================================
set /p up_choice="Select an option (1-3): "

if "%up_choice%"=="3" goto MENU

if "%up_choice%"=="1" (
    python scripts\generator\src\youtube\youtube_batch_uploader.py
    pause
    goto MENU
)

if "%up_choice%"=="2" (
    python scripts\generator\src\youtube\youtube_batch_uploader.py --video PICKER
    pause
    goto MENU
)
goto UPLOAD_ONLY

:DEBUG
python scripts\generator\src\debug_system.py
pause
goto MENU