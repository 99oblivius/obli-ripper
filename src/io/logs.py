import glob
import logging
import os
from datetime import datetime

from src.io.data import get_appdata_path
from src.config import (
    NAME,
    APP_NAME,
    VERSION,
    LOG_COUNT,
)
from src.io.data import pd

logger = logging.getLogger()


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


def setup():
    os.makedirs(os.path.join(get_appdata_path(), "Logs"), exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(get_appdata_path(), "Logs", f"logs-{NAME}{APP_NAME}{VERSION}-{datetime.now().strftime('%Y_%m_%d-%H_%M_%S')}.log"),
        format='%(asctime)s %(levelname)s| %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    delete_oldest_files(os.path.join(get_appdata_path(), "Logs"), LOG_COUNT)

    logger.setLevel(pd.config['debug_level'])
    logger.info(f"Logging file generated")
