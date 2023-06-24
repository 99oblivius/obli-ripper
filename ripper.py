from __future__ import unicode_literals

import logging
import os
import sys
from datetime import datetime

import yt_dlp

import src.rippergui as ripper
from config import *
from src.data import ProgramData


def input_with_check(statement: str = "", yes: str = 'y', no: str = 'n'):
	while True:
		answer = input(statement)
		if answer.lower().strip().startswith(yes):
			return True
		elif answer.lower().strip().startswith(no):
			return False
		else:
			print("Try again\n")


def yt_dl_process():
	file = open("songs.txt", "r")
	inputs = file.read().splitlines()
	directory = inputs[0]

	if input_with_check("Video or Audio download\n>Video/Audio?: ", 'v', 'a'):
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

	if not input_with_check(f"You have chosen the following download path: {str(directory)}\nConfirm >Y/N?: ", 'y',
							'n'):
		sys.exit()

	if not os.path.exists(directory):
		if input_with_check("The download path you chose does not exist.\nDo you wish to create it?\n>Y/N?: ", 'y',
							'n'):
			os.mkdir(directory)
		else:
			sys.exit()

	os.chdir(directory)
	try:
		with yt_dlp.YoutubeDL(download_options) as ydl:
			ydl.download(inputs[1:])
	except Exception:
		print("There was an issue with the download.\nTry again and or ensure all songs are publicly accessible.")


def main():
	pd = ProgramData()
	pd.load_appdata()

	logging.basicConfig(
		filename=os.path.join(pd.appdata, "Logs", f"logs-{VERSION}-{datetime.now().strftime('%Y-%m-%d %H %M %S')}.log"),
		format='%(asctime)s %(levelname)s| %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S.uuu',
		level=pd.config['debug_level'])

	window = ripper.RipperGUI()
	window.run()


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(f"Exception at: {repr(e)}")
	finally:
		input("Press RETURN")