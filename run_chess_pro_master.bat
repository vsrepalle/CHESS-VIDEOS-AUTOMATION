@echo off
setlocal enabledelayedexpansion
title Chess Pro Automation - Master Controller

:: --- environment setup ---
set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

:MENU
cls
echo.
echo ======================================================
echo       CHESS PRO AUTOMATION - MASTER CONTROLLER
echo ======================================================
echo  1. Process Tournament Brochures (Brochure -^> JSON)
echo  2. FEN TO VIDEO (FEN -^> Board -^> Short Video)
echo  3. (Reserved for Rendering)
echo  4. UPLOAD PIPELINE (Process output\videos)
echo  5. RUN FULL FEN PIPELINE (Step 2 + Step 4)
echo  6. Exit
echo ======================================================
echo  Working Directory: %CD%
echo ======================================================
set /p choice="select an option (1-6): "

if "%choice%"=="1" goto TOURNAMENT
if "%choice%"=="2" goto FEN_VIDEO
if "%choice%"=="3" goto MENU
if "%choice%"=="4" goto UPLOAD
if "%choice%"=="5" goto FULL_FEN
if "%choice%"=="6" goto EXIT
goto MENU

:TOURNAMENT
echo.
echo ------------------------------------------------------
echo [info] step 1: running ocr extractor...
python scripts/extractor/main.py
if %ERRORLEVEL% NEQ 0 (
    echo [error] ocr script failed.
    pause
    goto MENU
)
echo [success] ocr processing complete.
pause
goto MENU

:FEN_VIDEO
echo.
echo ------------------------------------------------------
echo [info] step 2: converting fen to video shorts...
python scripts/generator/src/video/fen_processor.py
if %ERRORLEVEL% NEQ 0 (
    echo [error] fen to video conversion failed.
    pause
    goto MENU
)
echo [success] videos and metadata ready in output\videos.
if "%choice%"=="5" goto UPLOAD
pause
goto MENU

:UPLOAD
echo.
echo ------------------------------------------------------
echo [info] step 4: starting upload process...
python scripts/generator/src/youtube/youtube_batch_uploader.py
if %ERRORLEVEL% NEQ 0 (
    echo [error] upload session encountered errors.
) else (
    echo [success] upload and cleanup finished.
)
pause
goto MENU

:FULL_FEN
echo [system] starting full fen pipeline...
goto FEN_VIDEO

:EXIT
exit