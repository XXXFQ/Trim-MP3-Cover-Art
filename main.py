import glob
import os
import shutil
from pathlib import Path

from PIL import Image
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

def center_crop(img: Image, target_aspect_ratio: float) -> Image:
    '''
    画像を中央を基準にして、指定されたアスペクト比にトリミング

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
        # 幅が広すぎる場合
        new_width = int(target_aspect_ratio * img_height)
        left = (img_width - new_width) // 2
        right = left + new_width
        cropped_img = img.crop((left, 0, right, img_height))
    else:
        # 高さが高すぎる場合
        new_height = int(img_width / target_aspect_ratio)
        top = (img_height - new_height) // 2
        bottom = top + new_height
        cropped_img = img.crop((0, top, img_width, bottom))

    return cropped_img

def process_mp3_file(mp3_file_path: str, target_aspect_ratio: float):
    '''
    MP3のカバーアートを抽出して中央トリミング

    Parameters
    ----------
    mp3_file_path : str
        MP3ファイルのパス
    target_aspect_ratio : float
        目標のアスペクト比 (幅/高さ)
    '''
    audio = MP3(mp3_file_path, ID3=ID3)
    
    # ID3タグが無ければ読み込み
    if audio.tags is None:
        audio.add_tags()
    
    tags = audio.tags
    
    # APICタグ取得
    apic = None
    for tag in tags.values():
        if isinstance(tag, APIC):
            apic = tag
            break

    if apic:
        TEMP_DIR = Path("./_temp")
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        temp_cover_path = TEMP_DIR / 'temp_cover.jpg'
        temp_cover_cropped_path = TEMP_DIR / 'temp_cover_cropped.jpg'
        
        # 一時画像書き出し
        with open(temp_cover_path, 'wb') as img_file:
            img_file.write(apic.data)

        # 画像処理（中央トリミング）
        image = Image.open(temp_cover_path)
        image = center_crop(image, target_aspect_ratio)
        image.save(temp_cover_cropped_path, format='JPEG')

        # 新しい画像データを取得
        with open(temp_cover_cropped_path, 'rb') as img_file:
            new_apic_data = img_file.read()
        
        # APICタグだけを更新
        tags.delall('APIC')
        tags.add(APIC(
            encoding=3,            # utf-8
            mime='image/jpeg',
            type=3,                # front cover
            desc='',
            data=new_apic_data
        ))

        # 元のタグのバージョンを保持して保存
        tags.save(mp3_file_path, v1=tags.version[0], v2_version=tags.version[1])
        
        # 一時ファイルを削除
        shutil.rmtree(TEMP_DIR)

if __name__ == '__main__':
    target_aspect_ratio = 1  # 正方形 (720x720)
    mp3_files_list = sorted(glob.iglob(os.path.join('./mp3files', "*.mp3")))

    for mp3_file_path in mp3_files_list:
        process_mp3_file(mp3_file_path, target_aspect_ratio)
        print(f"処理済み: {mp3_file_path}")
