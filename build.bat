@echo off
setlocal

echo ==============================
echo   Trim MP3 Cover Art Build
echo ==============================

rem ========================================
rem 設定
rem ========================================
set "APP_NAME=trim-mp3-cover-art"
set "ENTRY_POINT=trim_mp3_cover_art\__main__.py"
set "PACKAGE_PATH=.\trim_mp3_cover_art"
set "ICON_PATH=.\assets\trim_mp3_icon.ico"

rem ========================================
rem クリーン処理
rem ========================================
echo Cleaning previous builds...

if exist build (
    rmdir /s /q build
)

if exist dist (
    rmdir /s /q dist
)

if exist "%APP_NAME%.spec" (
    del /q "%APP_NAME%.spec"
)

echo Clean complete.

rem ========================================
rem UPX の場所を取得
rem ========================================
call :find_upx
if errorlevel 1 goto :error

echo UPX Directory: %UPX_DIR%

rem ========================================
rem アイコン確認
rem ========================================
if not exist "%ICON_PATH%" (
    echo Error: Icon file not found: %ICON_PATH%
    goto :error
)

rem ========================================
rem ビルド実行
rem ========================================
call :build
if errorlevel 1 goto :error

echo.
echo ==============================
echo   Build complete!
echo   Output: dist\%APP_NAME%.exe
echo ==============================

pause
exit /b 0

rem ========================================
rem 関数: UPX検索
rem ========================================
:find_upx
set "UPX_DIR="
for /f "usebackq tokens=*" %%i in (`powershell -NoProfile -Command "(Get-Command upx.exe -ErrorAction SilentlyContinue).Path | Split-Path"`) do (
    set "UPX_DIR=%%i"
)

if "%UPX_DIR%"=="" (
    echo Error: UPX not found in PATH.
    echo Please install UPX and add it to PATH.
    exit /b 1
)

exit /b 0

rem ========================================
rem 関数: ビルド
rem ========================================
:build
echo Building executable...

uv run pyinstaller ^
    --onefile ^
    --name "%APP_NAME%" ^
    --console ^
    --icon "%ICON_PATH%" ^
    --hidden-import=trim_mp3_cover_art ^
    --upx-dir "%UPX_DIR%" ^
    -p "%PACKAGE_PATH%" ^
    "%ENTRY_POINT%"

exit /b %ERRORLEVEL%

rem ========================================
rem エラー処理
rem ========================================
:error
echo.
echo ==============================
echo   Build failed!
echo ==============================
pause
exit /b 1