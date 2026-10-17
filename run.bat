@echo off
chcp 65001 >nul
title MotionIQ — AI-Powered Human Motion Analysis
cd /d "%~dp0"

echo ===================================================================
echo   🏃‍♂️ MotionIQ — سامانه تحلیل هوشمند حرکت انسان
echo   بررسی پورت و راه‌اندازی سرور تازه...
echo ===================================================================

:: بستن پروسه قدیمی که پورت 7860 را قفل کرده است (در صورت وجود)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :7860 ^| findstr LISTENING 2^>nul') do (
    taskkill /f /pid %%a >nul 2>&1
)

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" run.py
) else (
    python run.py
)

pause
