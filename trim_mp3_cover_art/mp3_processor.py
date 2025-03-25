from pathlib import Path

from PIL import Image
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TRCK

from .logger import Logger

logger = Logger.get_logger(__name__)

def process_mp3_file(mp3_file_path: str, target_aspect_ratio: float, temp_dir: Path):
    '''
    MP3のカバーアートを抽出して中央トリミングし、トラック番号を維持する

    Parameters
    ----------
    mp3_file_path : str
        MP3ファイルのパス
    target_aspect_ratio : float
        目標のアスペクト比 (幅/高さ)
    temp_dir : Path
        一時ファイルを保存するディレクトリ
    '''
    # MP3ファイルを開く
    audio = MP3(mp3_file_path, ID3=ID3)

    if audio.tags is None:
        audio.add_tags()

    tags = audio.tags

    # APICタグを取得
    apic = _extract_apic(tags)
    track_number = _preserve_track_number(tags)

    if apic:
        temp_dir.mkdir(parents=True, exist_ok=True)

        temp_cover_path = temp_dir / 'temp_cover'
        temp_cover_cropped_path = temp_dir / 'temp_cover_cropped.jpg'

        # 画像を一時ファイルに保存
        with open(temp_cover_path, 'wb') as img_file:
            img_file.write(apic.data)

        # 画像を中央トリミング
        image = Image.open(temp_cover_path)
        image = _center_crop(image, target_aspect_ratio)

        # 画像をJPEG形式に変換
        if apic.mime == 'image/png':
            image = image.convert('RGB')

        # 画像を保存
        image.save(temp_cover_cropped_path, format='JPEG')

        # 画像をMP3ファイルに埋め込む
        with open(temp_cover_cropped_path, 'rb') as img_file:
            new_apic_data = img_file.read()

        # APICタグを削除して新しいAPICタグを追加
        tags.delall('APIC')
        tags.add(APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc='',
            data=new_apic_data
        ))

        if track_number:
            tags.add(track_number)

        tags.save(mp3_file_path, v2_version=3)

def _center_crop(img: Image, target_aspect_ratio: float) -> Image:
    '''
    画像を中央基準で指定されたアスペクト比にトリミング

    Parameters
    ----------
    img : PIL.Image
        元の画像
    target_aspect_ratio : float
        目標のアスペクト比 (幅/高さ)

    Returns
    -------
    PIL.Image
        トリミングされた画像
    '''
    img_width, img_height = img.size
    current_aspect_ratio = img_width / img_height

    if current_aspect_ratio > target_aspect_ratio:
        new_width = int(target_aspect_ratio * img_height)
        left = (img_width - new_width) // 2
        cropped_img = img.crop((left, 0, left + new_width, img_height))
    else:
        new_height = int(img_width / target_aspect_ratio)
        top = (img_height - new_height) // 2
        cropped_img = img.crop((0, top, img_width, top + new_height))

    return cropped_img

def _extract_apic(tags: ID3) -> APIC:
    '''
    APICタグを取得

    Parameters
    ----------
    tags : ID3
        MP3ファイルのタグ

    Returns
    -------
    APIC
        APICタグ
    '''
    for tag in tags.values():
        if isinstance(tag, APIC):
            return tag
    return None

def _preserve_track_number(tags: ID3) -> TRCK:
    '''
    トラック番号を取得して保持

    Parameters
    ----------
    tags : ID3
        MP3ファイルのタグ

    Returns
    -------
    TRCK
        トラック番号タグ
    '''
    return tags.get('TRCK')
