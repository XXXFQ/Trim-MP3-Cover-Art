import argparse
import glob
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
    parser.add_argument('input_dir', type=str, help='Input directory path containing mp3 files')
    return parser

def main(argv=None):
    '''
    メイン関数
    '''
    parser = init_parser()
    args = parser.parse_args(argv)

    input_dir = Path(args.input_dir)

    if not input_dir.exists() or not input_dir.is_dir():
        logger.error(f"Input directory {input_dir} does not exist or is not a directory.")
        return

    target_aspect_ratio = 1
    mp3_files_list = sorted(glob.glob(str(input_dir / "*.mp3")))
    TEMP_DIR = Path("./_temp")

    for mp3_file_path in mp3_files_list:
        process_mp3_file(mp3_file_path, target_aspect_ratio, TEMP_DIR)
        logger.info(f"Processed {mp3_file_path}")

    shutil.rmtree(TEMP_DIR)
    logger.info("Temporary files deleted")
