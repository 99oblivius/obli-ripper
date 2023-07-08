import os

NAME = "Oblivius"
APP_NAME = "Ripper"
VERSION = "V2.0"

CONFIGURATION_FILE = "config.conf"
LOG_COUNT = 10

RESOLUTION_X = 420
RESOLUTION_Y = 470

##### DEFAULTS #####
DOWNLOAD_PATH = os.path.expanduser('~')
DEBUG_LEVEL = 10  # 10:DEBUG 20:INFO 30:WARN 40:ERROR 50:CRITICAL
DOWNLOAD_CONTAINER = "webm"
VIDEO_CONTAINERS = "avi", "flv", "mkv", "m4v", "mov", "mp4", "webm"
AUDIO_CONTAINERS = "aac", "flac", "m4a", "mp3", "ogg", "wav", "webm"
SONGS_FILE = ""


def get_appdata_path():
    if os.name == 'nt':
        appdata_path = os.getenv('APPDATA')
        appdata_path = os.path.dirname(appdata_path)
        appdata_path = os.path.join(appdata_path, 'LocalLow')
    else:
        appdata_path = os.path.expanduser('~/.config')
    appdata_folder = os.path.join(appdata_path, NAME, APP_NAME)
    os.makedirs(appdata_folder, exist_ok=True)
    return appdata_folder
