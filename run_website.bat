@echo off
title CampusHire - College Placement & Recruitment Management System
color 0B
echo ===============================================================================
echo                CAMPHUSHIRE - DBMS MINI PROJECT WEB APPLICATION
echo ===============================================================================
echo Starting CampusHire Web Server on http://127.0.0.1:5000 ...
echo Press Ctrl+C in this window to stop the server at any time.
echo ===============================================================================

start http://127.0.0.1:5000
python app.py
pause
