@echo off
title CHESS VIDEOS AUTOMATION - Secure Git Push

echo ============================================
echo    CHESS VIDEOS AUTOMATION - GITHUB PUSH
echo ============================================
echo.

REM Move to project directory
cd /d %~dp0

REM Create temporary secret backup folder
set SECRET_BACKUP=%TEMP%\chess_secret_backup

if not exist "%SECRET_BACKUP%" mkdir "%SECRET_BACKUP%"

echo.
echo Backing up secret files...

REM Move secrets out of repo temporarily
if exist "client_secret.json" move client_secret.json "%SECRET_BACKUP%"
if exist "token.pickle" move token.pickle "%SECRET_BACKUP%"
if exist ".env" move .env "%SECRET_BACKUP%"

if exist "scripts\client_secret.json" move scripts\client_secret.json "%SECRET_BACKUP%"
if exist "scripts\client_secrets.json" move scripts\client_secrets.json "%SECRET_BACKUP%"
if exist "scripts\token.json" move scripts\token.json "%SECRET_BACKUP%"

if exist "scripts\extractor.env" move scripts\extractor.env "%SECRET_BACKUP%"

echo.
echo Checking Git repository...

IF NOT EXIST ".git" (
echo Initializing Git repository...
git init
git branch -M main
git remote add origin https://github.com/vsrepalle/CHESS-VIDEOS-AUTOMATION.git
)

echo.
echo Adding files...
git add --all

echo.
echo Creating commit...

for /f "tokens=1-4 delims=/ " %%a in ('date /t') do set mydate=%%a-%%b-%%c
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a%%b

git commit -m "Auto commit %mydate% %mytime%"

echo.
echo Pushing to GitHub...

git push -u origin main

echo.
echo Restoring secret files...

REM Move secrets back
if exist "%SECRET_BACKUP%\client_secret.json" move "%SECRET_BACKUP%\client_secret.json" .
if exist "%SECRET_BACKUP%\token.pickle" move "%SECRET_BACKUP%\token.pickle" .
if exist "%SECRET_BACKUP%.env" move "%SECRET_BACKUP%.env" .

if exist "%SECRET_BACKUP%\client_secret.json" move "%SECRET_BACKUP%\client_secret.json" scripts
if exist "%SECRET_BACKUP%\client_secrets.json" move "%SECRET_BACKUP%\client_secrets.json" scripts
if exist "%SECRET_BACKUP%\token.json" move "%SECRET_BACKUP%\token.json" scripts\

if exist "%SECRET_BACKUP%.env" move "%SECRET_BACKUP%.env" scripts\extractor\

echo.
echo ============================================
echo     PUSH COMPLETE
echo ============================================

pause
