@echo off
setlocal enabledelayedexpansion

:: --- CONFIGURATION ---
set "SCHEMA_DIR=schema"
set "SCHEMA_FILE=%SCHEMA_DIR%\video_schema.json"
set "DATA_FILE=data.json"
set "VALIDATOR_SCRIPT=app\json_validator.py"

echo =======================================================
echo   TRENDWAVE NOW: VALIDATION AND CLEANUP UTILITY
echo =======================================================

:: 1. CREATE MISSING DIRECTORIES
echo [1/3] Checking Project Structure...
if not exist "%SCHEMA_DIR%" (
    mkdir "%SCHEMA_DIR%"
    echo   - Created %SCHEMA_DIR%
)
if not exist "output" mkdir "output"
if not exist "logs" mkdir "logs"

:: 2. RUN JSON VALIDATION
echo [2/3] Validating %DATA_FILE%...
if exist "%VALIDATOR_SCRIPT%" (
    python "%VALIDATOR_SCRIPT%"
    if %errorlevel% neq 0 (
        echo [ERROR] JSON Validation failed! Fix data.json and try again.
        pause
        exit /b %errorlevel%
    )
) else (
    echo [WARNING] Validator script not found at %VALIDATOR_SCRIPT%. Skipping validation.
)

:: 3. CLEAN UP TEMPORARY FILES
echo [3/3] Cleaning Temporary Assets...

:: Clean Temp Audio
if exist "temp_audio" (
    del /q "temp_audio\*"
    echo   - Cleared temp_audio
)

:: Clean Temp Chunks
if exist "temp_chunks" (
    del /q "temp_chunks\*"
    echo   - Cleared temp_chunks
)

:: Clean Fetched Images (but keep the folder)
if exist "images\fetched" (
    del /q "images\fetched\*"
    echo   - Cleared images\fetched
)

:: Clean MoviePy temporary sound/video files (*TEMP_MPY*)
del /q *TEMP_MPY* 2>nul
if %errorlevel% equ 0 echo   - Removed MoviePy crash artifacts.

echo =======================================================
echo   READY FOR PRODUCTION: PRE-FLIGHT CHECK COMPLETE
echo =======================================================
pause