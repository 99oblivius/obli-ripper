from __future__ import unicode_literals

import atexit
import os

import yt_dlp

import src.rippergui as ripper
from src.data import pd
from src.logs import logging as log


def exit_function():
    pd.save_appdata()
    log.critical("Program closed")


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
    log.getLogger().setLevel(pd.config['debug_level'])
    log.info(f"Logging file generated")
    atexit.register(exit_function)
    window = ripper.RipperGUI()
    window.run()


if __name__ == "__main__":
    main()
