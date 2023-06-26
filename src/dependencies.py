import io
import zipfile

import requests

from config import *


def install_ffmpeg(path):
    if os.name == 'nt':
        ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        binary_name = "ffmpeg.exe"
    else:
        ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz"
        binary_name = "ffmpeg"
    binary_path = os.path.join(path, binary_name)

    if os.path.exists(binary_path):
        return
    response = requests.get(ffmpeg_url)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        archive.extract(binary_name, path=path)


def setup():
    if os.name == 'nt':
        appdata_path = os.getenv('APPDATA')
        appdata_path = os.path.dirname(appdata_path)
        appdata_path = os.path.join(appdata_path, 'LocalLow')
    else:
        appdata_path = os.path.expanduser('~/.config')
    bin_folder = os.path.join(appdata_path, NAME, APP_NAME, "bin")
    os.makedirs(bin_folder, exist_ok=True)

    install_ffmpeg(bin_folder)
