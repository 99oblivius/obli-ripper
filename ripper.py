from __future__ import unicode_literals

import atexit

import src.rippergui as ripper
from src.data import pd
from src.dependencies import setup
from src.logs import logging as log


def exit_function():
    pd.save_appdata()
    log.critical("Program closed")


def main():
    pd.load_appdata()
    log.getLogger().setLevel(pd.config['debug_level'])
    log.info(f"Logging file generated")
    atexit.register(exit_function)
    setup()
    window = ripper.RipperGUI()
    window.run()


if __name__ == "__main__":
    main()
