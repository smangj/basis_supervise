# coding: utf-8
# Author: smangj
import logging
from logging.handlers import RotatingFileHandler
import os

from app.common.utils import check_and_mkdirs

MAX_BYTES = 25 * 1024 * 1024
BACK_UP_COUNT = 5

LOG_DIR = r'./data/log'
check_and_mkdirs(LOG_DIR)


def init_logging(logger, log_name: str, log_root_dir: str = LOG_DIR):
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(module)s : %(levelname)s : %(message)s')

    error_fh = RotatingFileHandler(os.path.join(log_root_dir, "{}.err".format(log_name)), maxBytes=MAX_BYTES,
                                   backupCount=BACK_UP_COUNT)

    error_fh.setFormatter(formatter)
    error_fh.setLevel(logging.ERROR)

    info_fh = RotatingFileHandler(os.path.join(log_root_dir, "{}.log".format(log_name)), maxBytes=MAX_BYTES,
                                  backupCount=BACK_UP_COUNT)

    info_fh.setFormatter(formatter)
    info_fh.setLevel(logging.INFO)

    logger.addHandler(error_fh)
    logger.addHandler(info_fh)


if __name__ == '__main__':
    pass
