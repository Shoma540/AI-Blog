@echo off
chcp 65001 > nul
cd /d C:\Users\shoma\Desktop\AI-Blog
if exist .git\index.lock del /f .git\index.lock
git add festival-routine-prompt.md
git commit -m "add: festival-routine-prompt.md"
git push
echo.
echo === DONE ===
pause
