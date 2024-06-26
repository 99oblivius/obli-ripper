from __future__ import unicode_literals

import os
import logging
from datetime import datetime

from src.config import (
    NAME,
    APP_NAME,
    RESOLUTION_Y,
    RESOLUTION_X,
)

logger = logging.getLogger(__name__)


def stamp_now():
    return datetime.utcnow().timestamp()


def shift_focus(obj):
    obj.focus()


def check_ffmpeg(path):
    if os.name == 'nt':
        # ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        binary_name = "ffmpeg.exe"
    else:
        # ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz"
        binary_name = "ffmpeg"
    binary_path = os.path.join(path, binary_name)
    return os.path.exists(binary_path)


def requirements_setup():
    if os.name == 'nt':
        program_files_path = os.environ.get('ProgramFiles')
    else:
        program_files_path = '/usr/local/bin'
    bin_folder = os.path.join(program_files_path, NAME, APP_NAME, "bin")
    os.makedirs(bin_folder, exist_ok=True)

    return check_ffmpeg(bin_folder)






