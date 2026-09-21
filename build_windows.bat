@echo off
setlocal
cd /d "%~dp0.."
echo [1/3] Installing dependencies...
python -m pip install -r requirements.txt
echo [2/3] Building application...
python -m PyInstaller --noconfirm --clean --windowed --name "PVC Card Studio V3" main.py
echo [3/3] Build complete.
echo EXE: dist\PVC Card Studio V3\PVC Card Studio V3.exe
pause
