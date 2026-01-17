@echo off
title Launch Risk Intelligence System Controller
echo ==================================================
echo   LAUNCH RISK INTELLIGENCE SYSTEM - CONTROL PANEL
echo ==================================================
echo.
echo [1] Launching Web Interface...
start "Risk Intelligence Dashboard" python -m streamlit run web_ui/Home.py --server.headless true
echo.
echo [2] Launching Promotion Worker...
start "Promotion Worker" python run_promotion_campaign.py
echo.
echo ==================================================
echo   SYSTEM IS LIVE
echo   - Dashboard: http://localhost:8501
echo   - Worker: Running in background window
echo ==================================================
echo.
echo NOTE: This system ONLY runs while your computer is ON.
echo To stop, simply close the opened windows.
echo.
pause