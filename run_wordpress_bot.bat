@echo off
chcp 65001 > nul
cd /d %~dp0
python wordpress_bot.py
pause
