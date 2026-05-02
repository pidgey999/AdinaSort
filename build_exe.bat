@echo off
setlocal

REM Build + release zip for AdinaSort
set APP_NAME=AdinaSort
set ICON_FILE=assets\adina.ico
set DIST_DIR=dist
set RELEASE_DIR=release
set ZIP_FILE=%RELEASE_DIR%\%APP_NAME%.zip

python -m pip install --upgrade pip
python -m pip install pyinstaller

set ICON_ARG=
if exist "%ICON_FILE%" (
  set ICON_ARG=--icon "%ICON_FILE%"
) else (
  echo [WARN] Icon file not found at %ICON_FILE%
  echo        Build will continue without custom icon.
)

pyinstaller --noconfirm --clean --onefile --windowed --name %APP_NAME% %ICON_ARG% app.py
if errorlevel 1 goto :error

if not exist "%RELEASE_DIR%" mkdir "%RELEASE_DIR%"
copy /Y "%DIST_DIR%\%APP_NAME%.exe" "%RELEASE_DIR%\%APP_NAME%.exe" >nul

powershell -NoProfile -Command "Compress-Archive -Force -Path '%RELEASE_DIR%\%APP_NAME%.exe','README.md' -DestinationPath '%ZIP_FILE%'"
if errorlevel 1 goto :error

echo.
echo Build complete:
echo   %DIST_DIR%\%APP_NAME%.exe
echo Release zip:
echo   %ZIP_FILE%
endlocal
exit /b 0

:error
echo.
echo Build failed.
endlocal
exit /b 1
