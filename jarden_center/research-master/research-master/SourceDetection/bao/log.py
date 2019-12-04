# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import logging


class Logger():
    format_dict = {
        logging.DEBUG: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
        logging.INFO: logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s'),
        logging.WARNING: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
        logging.ERROR: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
        logging.CRITICAL: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    }

    def __init__(self, logname, loglevel, logger):
        """write the log to a file, set the log level"""

        self.logger = logging.getLogger(logger)
        self.logger.setLevel(loglevel)

        fh = logging.FileHandler(logname)
        fh.setLevel(loglevel)

        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)

        formatter = self.format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        # ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        # self.logger.addHandler(ch)

    def get_log(self):
        return self.logger
