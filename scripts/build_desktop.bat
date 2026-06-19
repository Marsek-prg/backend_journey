@echo off
setlocal

if not exist ".venv\Scripts\python.exe" (
    echo Error: .venv was not found. Run this script from the project root.
    exit /b 1
)

if not exist "desktop.py" (
    echo Error: desktop.py was not found. Run this script from the project root.
    exit /b 1
)

echo Installing desktop dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements-desktop.txt
if errorlevel 1 exit /b 1

echo Installing build dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements-build.txt
if errorlevel 1 exit /b 1

echo Building TaskTracker...
".venv\Scripts\python.exe" -m PyInstaller ^
    --noconfirm ^
    --onedir ^
    --windowed ^
    --name TaskTracker ^
    --add-data "app/templates;app/templates" ^
    --add-data "app/static;app/static" ^
    desktop.py
if errorlevel 1 exit /b 1

echo Build completed: dist\TaskTracker\TaskTracker.exe
endlocal
