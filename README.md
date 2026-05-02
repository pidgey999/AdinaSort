# AdinaSort GUI

This project provides a simple Tkinter GUI for:
- Sorting inventory
- Buying items from shop
- Configuring hotkeys for chest grabbing

## Build `.exe` (Windows)

### 1) Place custom icon
Put your icon file here (ICO format):
- `assets/adina.ico`

> Note: Windows executable icons require `.ico`. If your source image is PNG/JPG, convert it to ICO first.

### 2) Run one-click build + release zip
```bat
build_exe.bat
```

### 3) Output
- Executable: `dist\\AdinaSort.exe`
- Release package: `release\\AdinaSort.zip`

The zip includes:
- `AdinaSort.exe`
- `README.md`

## Manual build command
```bat
python -m pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name AdinaSort --icon assets\adina.ico app.py
```
