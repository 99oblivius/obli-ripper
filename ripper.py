from __future__ import unicode_literals

import atexit
import logging

import src.logs
import src.rippergui as ripper
from src.data import pd

logger = logging.getLogger()


def exit_function():
    pd.save_appdata()
    logger.info("Program closed")


def main():
    pd.load_appdata()

    atexit.register(exit_function)

    window = ripper.RipperGUI()
    window.run()


if __name__ == "__main__":
    src.logs.setup()
    main()
