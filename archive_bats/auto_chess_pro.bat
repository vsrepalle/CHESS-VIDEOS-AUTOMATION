@echo off
setlocal enabledelayedexpansion

:: --- Configuration ---
set "ROOT=C:\VISWA\CHESS_PRO_AUTOMATION"
set "AI_GEN=%ROOT%\scripts\generator\src\utils\ai_puzzle_gen.py"
set "PIPELINE=%ROOT%\pipeline_runner.py"
set "UPLOADER=%ROOT%\scripts\generator\src\youtube\youtube_uploader.py"
set "FEN_DIR=%ROOT%\scripts\generator\input\FEN"
set "VIDEO_DIR=%ROOT%\output\videos"
set "MANUAL_IMPORT=%ROOT%\fen_short_puzzle\add_fen.bat"

echo ==================================================
echo       CHESS PRO: SELECT YOUR PUZZLE SOURCE
echo ==================================================
echo [1] Generate fresh puzzle with Gemini AI
echo [2] Use existing my_puzzle.json (Manual)
echo [3] Skip to Rendering (Use files already in FEN folder)
echo ==================================================
set /p "choice=Select option (1, 2, or 3): "

:: 1. Handle Input Source
if "%choice%"=="1" (
    echo [PROCESS] Invoking Gemini AI...
    python "%AI_GEN%"
) else if "%choice%"=="2" (
    echo [PROCESS] Importing from my_puzzle.json...
    call "%MANUAL_IMPORT%"
) else (
    echo [PROCESS] Skipping import, using existing FEN files...
)

:: 2. Clean Ghost Files
if exist "%FEN_DIR%\.txt" del "%FEN_DIR%\.txt"

:: 3. Run Pipeline
echo [PROCESS] Rendering and Assembling Video...
python "%PIPELINE%"

:: --- NEW: AUTO-OPEN VIDEO FOLDER ---
echo [PROCESS] Opening video folder for preview...
start explorer "%VIDEO_DIR%"
timeout /t 2 >nul

:: 4. Upload to YouTube
echo ==================================================
echo             YOUTUBE UPLOAD SECTION
echo ==================================================
echo Check the folder that just opened. Are the videos ready?
set /p "up_choice=Upload generated videos now? (y/n): "
if /i "%up_choice%"=="y" (
    for %%F in ("%VIDEO_DIR%\*.mp4") do (
        set "vid_name=%%~nF"
        echo [UPLOAD] Processing: %%~nxF
        python "%UPLOADER%" --video "%%F" --json "%FEN_DIR%\!vid_name!.json"
    )
)

echo.
echo Done! Pipeline finished.
pause