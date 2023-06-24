from __future__ import unicode_literals

import logging
import os
from datetime import datetime

from config import *
from src.data import pd

logs_folder = os.path.join(pd.appdata, "Logs")
os.makedirs(logs_folder, exist_ok=True)
logging_file = os.path.join(logs_folder, f"logs-{NAME}{APP_NAME}{VERSION}-{datetime.now().strftime('%Y_%m_%d-%H_%M_%S')}.log")
logging.basicConfig(
    filename=logging_file,
    format='%(asctime)s %(levelname)s| %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S.%f'[:-3],
    level=pd.config['debug_level'],
)
logging.info(f"Logging file generated '{logging_file}'")

import yt_dlp

import src.rippergui as ripper

import atexit


def yt_dl_process():
    file = open("songs.txt", "r")
    inputs = file.read().splitlines()
    directory = inputs[0]

    if file:
        download_options = {
            'ignoreerrors': True,
            'format': 'mp4/bv*+ba/b',
            'format-sort': 'ext'
        }
    else:
        download_options = {
            'ignoreerrors': True,
            'format': 'mp3/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }
    os.chdir(directory)
    try:
        with yt_dlp.YoutubeDL(download_options) as ydl:
            ydl.download(inputs[1:])
    except Exception:
        print("There was an issue with the download.\nTry again and or ensure all songs are publicly accessible.")


def main():
    pd.load_appdata()
    atexit.register(pd.save_appdata)
    window = ripper.RipperGUI()
    window.run()


if __name__ == "__main__":
    main()
