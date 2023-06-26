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
DOWNLOAD_CONTAINER = "mp4"
VIDEO_CONTAINERS = "av1", "flv", "mkv", "m4v", "mov", "mp4", "webm"
AUDIO_CONTAINERS = "aac", "flac", "m4a", "mp3", "ogg", "wav", "webm"
