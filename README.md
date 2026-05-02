# Battle Royale Helper GUI

This project provides a simple Tkinter GUI for:
- Sorting inventory
- Buying items from shop
- Configuring hotkeys for chest grabbing

## Build `.exe` (Windows)

### 1) Install Python (only for builder)
Install Python 3.11+ and ensure `python` is available in terminal.

### 2) Run build script
```bat
build_exe.bat
```

### 3) Output
The standalone executable will be generated at:
- `dist\\BattleRoyaleHelper.exe`

## Manual build command
If you prefer running manually:
```bat
python -m pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name BattleRoyaleHelper app.py
```
