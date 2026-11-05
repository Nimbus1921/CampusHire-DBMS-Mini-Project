@echo off
title CampusHire - Public Online Sharing Tunnel
color 0A
echo ===============================================================================
echo        CAMPUSHIRE - PUBLIC INTERNET SHARING FOR COLLEAGUES & TEACHER
echo ===============================================================================
echo 1. Ensure your website is already running in another window (run_website.bat).
echo 2. This will generate a public URL (https://....loca.lt) you can share with
echo    anyone over WhatsApp/Email even if they are NOT on your Wi-Fi!
echo 3. Any changes they make on that link will update your database in real time!
echo ===============================================================================
echo.
echo Generating public link now...
npx localtunnel --port 5000
pause
