@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo      CHESS PRO: JSON TO FEN IMPORTER
echo ==========================================
echo.

:: 1. Set the source filename
set "JSON_SOURCE=my_puzzle.json"

:: 2. Check if the file exists in the current directory
if not exist "%~dp0%JSON_SOURCE%" (
    echo [ERROR] File not found: %JSON_SOURCE%
    echo Please ensure %JSON_SOURCE% is in this folder: %~dp0
    echo.
    pause
    exit /b
)

:: 3. Define the target directory
set "TARGET_DIR=C:\VISWA\CHESS_PRO_AUTOMATION\scripts\generator\input\FEN"
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

echo [PROCESS] Reading %JSON_SOURCE% from current folder...

:: 4. Use PowerShell to parse and split the files
powershell -Command ^
    "$jsonPath = Join-Path '%~dp0' '%JSON_SOURCE%';" ^
    "$json = Get-Content $jsonPath | ConvertFrom-Json;" ^
    "$name = $json.name -replace '[^a-zA-Z0-9_]', '_';" ^
    "$fen = $json.fen;" ^
    "$outTxt = Join-Path '%TARGET_DIR%' \"$name.txt\";" ^
    "$outJson = Join-Path '%TARGET_DIR%' \"$name.json\";" ^
    "Set-Content -Path $outTxt -Value $fen;" ^
    "$json | ConvertTo-Json | Set-Content -Path $outJson;" ^
    "Write-Host \"Successfully created $name.txt and $name.json\" -ForegroundColor Green"

echo.
echo ------------------------------------------
echo DONE! Files moved to pipeline input.
echo ------------------------------------------
pause