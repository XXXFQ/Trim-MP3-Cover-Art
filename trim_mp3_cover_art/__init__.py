import argparse
import shutil
from pathlib import Path

from .mp3_processor import process_mp3_file
from .logger import Logger

logger = Logger.get_logger(__name__)

def init_parser() -> argparse.ArgumentParser:
    '''
    コマンドライン引数を解析するためのパーサーを初期化する

    Returns
    -------
    parser : argparse.ArgumentParser
        パーサー
    '''
    parser = argparse.ArgumentParser(description='Trim Mp3 Cover Art')
    parser.add_argument(
        'inputs',
        nargs='+',
        type=str,
        help='Input mp3 files or directories containing mp3 files'
    )
    return parser

def collect_mp3_files(input_paths: list[str]) -> list[Path]:
    '''
    入力されたパス群からmp3ファイル一覧を収集する

    Parameters
    ----------
    input_paths : list[str]
        コマンドライン引数で渡されたパス一覧

    Returns
    -------
    list[Path]
        処理対象となるmp3ファイル一覧
    '''
    mp3_files: list[Path] = []

    for input_path_str in input_paths:
        input_path = Path(input_path_str)

        if not input_path.exists():
            logger.warning(f"Path does not exist: {input_path}")
            continue

        if input_path.is_dir():
            mp3_files.extend(sorted(input_path.glob("*.mp3")))
        elif input_path.is_file() and input_path.suffix.lower() == ".mp3":
            mp3_files.append(input_path)
        else:
            logger.warning(f"Unsupported path: {input_path}")

    # 重複除去
    return sorted(set(mp3_files))

def main(argv=None):
    '''
    メイン関数
    '''
    parser = init_parser()
    args = parser.parse_args(argv)

    mp3_files_list = collect_mp3_files(args.inputs)

    if not mp3_files_list:
        logger.error("No mp3 files found.")
        return

    target_aspect_ratio = 1
    TEMP_DIR = Path("./_temp")
    TEMP_DIR.mkdir(exist_ok=True)

    try:
        for mp3_file_path in mp3_files_list:
            process_mp3_file(str(mp3_file_path), target_aspect_ratio, TEMP_DIR)
            logger.info(f"Processed {mp3_file_path}")
    finally:
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)
            logger.info("Temporary files deleted")
