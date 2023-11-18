import os


NAME = "Oblivius"
APP_NAME = "Ripper"
VERSION = "V2.0"

if os.name == 'nt':
    APP_ICON = f"{os.environ.get('ProgramFiles')}\\{NAME}\\{APP_NAME}\\assets\\256.png"
else:
    APP_ICON = f"/usr/local/bin{NAME}/{APP_NAME}/assets/256.png"

CONFIGURATION_FILE = "config.conf"
LOG_COUNT = 100

RESOLUTION_X = 420
RESOLUTION_Y = 470


##### DEFAULTS #####
DOWNLOAD_PATH = os.path.expanduser('~')
DEBUG_LEVEL = 10  # 10:DEBUG 20:INFO 30:WARN 40:ERROR 50:CRITICAL
DOWNLOAD_CONTAINER = "webm"
VIDEO_CONTAINERS = "avi", "mkv", "m4v", "mov", "mp4", "webm"
AUDIO_CONTAINERS = "aac", "flac", "mp3", "ogg", "wav", "opus"
SONGS_FILE = ""
OUTPUT_TEMPLATE = "[ripper] %(fulltitle)s.%(ext)s"


# TODO
# Reload config
# set clip time and duration
# implement MediaTools
