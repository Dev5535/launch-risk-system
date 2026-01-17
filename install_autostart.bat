@echo off
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "VBS_PATH=%~dp0start_system_hidden.vbs"

echo Installing Auto-Start Service...
echo @echo off > "%STARTUP_DIR%\launch_risk_promo.bat"
echo wscript "%VBS_PATH%" >> "%STARTUP_DIR%\launch_risk_promo.bat"

echo ✅ Success! The Launch Risk Intelligence Promotion Worker will now start automatically when your laptop turns on.
echo This ensures 24/7 coverage simulation even after restarts.
pause
