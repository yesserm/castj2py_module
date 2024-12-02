import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def configure_logging():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.DEBUG)

    path_to_log = os.path.join('..', '..', 'app.log')
    file_handler = logging.FileHandler(path_to_log)
    file_handler.setLevel(logging.ERROR)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger