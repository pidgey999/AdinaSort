@echo off
setlocal

REM Build a standalone Windows executable for app.py
python -m pip install --upgrade pip
python -m pip install pyinstaller

pyinstaller --noconfirm --clean --onefile --windowed --name BattleRoyaleHelper app.py

echo.
echo Build complete. Executable is at:
echo dist\BattleRoyaleHelper.exe
endlocal
