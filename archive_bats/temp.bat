@echo off
setlocal enabledelayedexpansion
title Chess Pro Project Polisher

echo [1/3] Creating Master Control Center (run_chess_pro.bat)...
(
echo @echo off
echo setlocal enabledelayedexpansion
echo title CHESS PRO - Master Menu
echo :MENU
echo cls
echo echo ==================================================
echo echo       CHESS PRO AUTOMATION - MASTER MENU
echo echo ==================================================
echo echo  1. FULL PIPELINE (AI Generate -^> Render)
echo echo  2. MANUAL PUZZLE (Import my_puzzle.json -^> Render)
echo echo  3. RENDER ONLY  (Process files already in FEN folder)
echo echo  4. UPLOAD ONLY  (Upload existing MP4s to YouTube)
echo echo  5. DEBUG SYSTEM (Check Environment ^& Paths)
echo echo  6. EXIT
echo echo ==================================================
echo set /p "choice=Select an option (1-6): "
echo.
echo :: --- FORCE CLEANER ---
echo echo [CLEAN] Wiping temporary boards and old inputs...
echo if exist "scripts\generator\output\rendered_boards\*.png" del /q "scripts\generator\output\rendered_boards\*.png"
echo if exist "scripts\generator\input\FEN\*" del /q "scripts\generator\input\FEN\*"
echo.
echo if "%%choice%%"=="1" goto FULL_PIPELINE
echo if "%%choice%%"=="2" goto MANUAL_PUZZLE
echo if "%%choice%%"=="3" goto RENDER_ONLY
echo if "%%choice%%"=="4" goto UPLOAD_ONLY
echo if "%%choice%%"=="5" goto DEBUG
echo if "%%choice%%"=="6" exit
echo goto MENU
echo.
echo :FULL_PIPELINE
echo python scripts\generator\src\utils\ai_puzzle_gen.py
echo python pipeline_runner.py
echo goto END
echo.
echo :MANUAL_PUZZLE
echo call fen_short_puzzle\add_fen.bat
echo python pipeline_runner.py
echo goto END
echo.
echo :RENDER_ONLY
echo python pipeline_runner.py
echo goto END
echo.
echo :UPLOAD_ONLY
echo python scripts\generator\src\youtube\youtube_uploader.py
echo goto END
echo.
echo :DEBUG
echo python debug_pipeline.py
echo pause
echo goto MENU
echo.
echo :END
echo echo.
echo echo Done! Video should be in output\videos.
echo pause
echo goto MENU
) > run_chess_pro.bat

echo [2/3] Creating HOWTORUN.md...
(
echo # ♟️ Chess Pro Automation Guide
echo.
echo ## 🚀 How to Run
echo 1. Edit `fen_short_puzzle/my_puzzle.json` for manual puzzles.
echo 2. Run `run_chess_pro.bat` and select Option 2.
echo.
echo ## 🧹 Built-in Force Cleaner
echo The system now automatically wipes `rendered_boards` before every run to prevent "ghost" images from old puzzles.
echo.
echo ## 📂 Output
echo Videos are saved to: `C:\VISWA\CHESS_PRO_AUTOMATION\output\videos\`
) > HOWTORUN.md

echo [3/3] Cleaning up Root Directory...
if not exist "archive_bats" mkdir "archive_bats"
move "auto_chess_pro.bat" "archive_bats\" >nul 2>&1
move "run_all.bat" "archive_bats\" >nul 2>&1
move "setup_ui.bat" "archive_bats\" >nul 2>&1
move "temp.bat" "archive_bats\" >nul 2>&1
move "app_fix_temp.py" "archive_bats\" >nul 2>&1

echo ==================================================
echo SETUP COMPLETE!
echo Use "run_chess_pro.bat" from now on.
echo ==================================================
pause