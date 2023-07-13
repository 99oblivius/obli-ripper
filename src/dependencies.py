from config import *


def check_ffmpeg(path):
    if os.name == 'nt':
        # ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        binary_name = "ffmpeg.exe"
    else:
        # ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz"
        binary_name = "ffmpeg"
    binary_path = os.path.join(path, binary_name)
    return os.path.exists(binary_path)


def rquirements_setup():
    if os.name == 'nt':
        program_files_path = os.environ.get('ProgramFiles')
    else:
        program_files_path = '/usr/local/bin'
    bin_folder = os.path.join(program_files_path, NAME, APP_NAME, "bin")
    os.makedirs(bin_folder, exist_ok=True)

    return check_ffmpeg(bin_folder)
