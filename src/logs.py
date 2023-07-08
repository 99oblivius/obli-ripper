import glob
import logging
from datetime import datetime

from config import *


def delete_oldest_files(directory, limit):
    file_pattern = os.path.join(directory, '*.log')
    files = glob.glob(file_pattern)

    sorted_files = []
    for file in files:
        date = validate_file_format(file)
        if date: sorted_files.append((file, date))

    sorted_files = sorted(sorted_files, key=lambda d: d[1], reverse=True)

    for file in sorted_files[limit:]:
        file_path = file[0]
        os.remove(file_path)


def validate_file_format(file):
    file_name = os.path.basename(file)
    try:
        return datetime.strptime(file_name[-23:-4], '%Y_%m_%d-%H_%M_%S')
    except ValueError:
        return False


logs_folder = os.path.join(get_appdata_path(), NAME, APP_NAME, "Logs")
os.makedirs(logs_folder, exist_ok=True)
logging_file = os.path.join(logs_folder, f"logs-{NAME}{APP_NAME}{VERSION}-{datetime.now().strftime('%Y_%m_%d-%H_%M_%S')}.log")
logging.basicConfig(
    filename=logging_file,
    format='%(asctime)s %(levelname)s| %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class MyLogger:
    def debug(self, msg):
        if msg.startswith('[debug] '):
            logging.debug(f"YT-DLP {msg[8:]}")
        elif msg.startswith('[info] '):
            logging.info(f"YT-DLP {msg[7:]}")

    def info(self, msg):
        pass

    def warning(self, msg):
        logging.warning(f"YT-DLP {msg[10:]}")

    def error(self, msg):
        logging.error(f"YT-DLP {msg[8:]}")


delete_oldest_files(logs_folder, LOG_COUNT)
