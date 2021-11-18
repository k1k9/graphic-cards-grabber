#!/usr/bin/env python3
# Author: K1K9
# Release date: 04/2021

import os
import coloredlogs
import logging
import grab
from datetime import date

# Setting up logger
log_file = date.today().strftime("%d%m%Y")
log_dir = os.path.dirname(os.path.realpath(__file__))+"/logs/"
logger = logging.getLogger(__name__)
fh = logging.FileHandler(f"{log_dir}{log_file}.log")
formatter = logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s')
coloredlogs.install(level='DEBUG')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)


def main(search):
    logger.debug("Started new cycle")
    search = input('Entry full name of card: ')
    grabber = grab.Grab(logger, search)
    grabber.run()


if __name__ == '__main__':
    main()