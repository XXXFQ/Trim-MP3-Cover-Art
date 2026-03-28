#!/usr/bin/env bash
set -euo pipefail

echo "=============================="
echo "  Trim MP3 Cover Art Build"
echo "=============================="

# ========================================
# 設定
# ========================================
APP_NAME="trim-mp3-cover-art"
ENTRY_POINT="trim_mp3_cover_art/__main__.py"
PACKAGE_PATH="./trim_mp3_cover_art"
ICON_PATH="./assets/trim_mp3_icon.ico"

# ========================================
# エラー処理
# ========================================
error_exit() {
    echo
    echo "=============================="
    echo "  Build failed!"
    echo "=============================="
    exit 1
}

trap error_exit ERR

# ========================================
# クリーン処理
# ========================================
echo "Cleaning previous builds..."

rm -rf build
rm -rf dist
rm -f "${APP_NAME}.spec"

echo "Clean complete."

# ========================================
# UPX の場所を取得
# ========================================
if ! command -v upx >/dev/null 2>&1; then
    echo "Error: UPX not found in PATH."
    echo "Please install UPX and add it to PATH."
    exit 1
fi

UPX_DIR="$(dirname "$(command -v upx)")"
echo "UPX Directory: ${UPX_DIR}"

# ========================================
# アイコン確認
# ========================================
if [[ ! -f "${ICON_PATH}" ]]; then
    echo "Error: Icon file not found: ${ICON_PATH}"
    exit 1
fi

# ========================================
# ビルド実行
# ========================================
echo "Building executable..."

uv run pyinstaller \
    --onefile \
    --name "${APP_NAME}" \
    --console \
    --icon "${ICON_PATH}" \
    --hidden-import=trim_mp3_cover_art \
    --upx-dir "${UPX_DIR}" \
    -p "${PACKAGE_PATH}" \
    "${ENTRY_POINT}"

echo
echo "=============================="
echo "  Build complete!"
echo "  Output: dist/${APP_NAME}"
echo "=============================="