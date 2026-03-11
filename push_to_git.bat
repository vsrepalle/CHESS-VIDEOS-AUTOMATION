@echo off
title CHESS VIDEOS AUTOMATION - Git Push

echo ============================================
echo    CHESS VIDEOS AUTOMATION - GITHUB PUSH
echo ============================================
echo.

REM Move to script directory
cd /d %~dp0

echo Checking if Git repository exists...

IF NOT EXIST ".git" (
echo Initializing Git repository...
git init
git branch -M main
git remote add origin https://github.com/vsrepalle/CHESS-VIDEOS-AUTOMATION.git
)

echo.
echo Adding files...
git add .

echo.
echo Creating commit...

for /f "tokens=1-4 delims=/ " %%a in ('date /t') do set mydate=%%a-%%b-%%c
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a%%b

git commit -m "Auto commit %mydate% %mytime%"

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo ============================================
echo     PUSH COMPLETE
echo ============================================
pause
