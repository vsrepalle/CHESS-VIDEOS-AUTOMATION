@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   ♟️ CHESS PIPELINE: PRE-BUILD CHECK
echo ========================================

:: 1. Check Python Version
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

for /f "tokens=2" %%I in ('python --version') do set pyver=%%I
echo [INFO] Detected Python Version: %pyver%

:: 2. Check for PyInstaller
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] PyInstaller not found. Installing now...
    pip install pyinstaller
) else (
    echo [INFO] PyInstaller is ready.
)

:: 3. Create Project Folders if missing
echo [INFO] Verifying folder structure...
if not exist "scripts\extractor\output" mkdir "scripts\extractor\output"
if not exist "scripts\generator\output" mkdir "scripts\generator\output"
if not exist "scripts\generator\input" mkdir "scripts\generator\input"

:: 4. Build the Executable
echo.
echo ========================================
echo   🚀 STARTING PYINSTALLER BUILD
echo ========================================

:: --noconfirm: Overwrites existing files
:: --onefile: Single EXE output
:: --clean: Cleans cache before building
:: --add-data: Includes your scripts folder (format: Source;Destination)
pyinstaller --noconfirm --onefile --console ^
    --name "ChessAutomationTool" ^
    --clean ^
    --add-data "scripts;scripts" ^
    --collect-all moviepy ^
    "pipeline_runner.py"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ SUCCESS! EXE created in 'dist' folder.
    echo ========================================
) else (
    echo.
    echo ❌ BUILD FAILED. Check the logs above.
)

pause