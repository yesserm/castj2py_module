import os
import logging
import sys
from pathlib import Path

logger = logging.getLogger('app_logger')

current_path = Path(os.getcwd()).resolve()
sys.path.append(os.path.join(current_path, 'modules', 'castj2py', 'src'))

from utils.db_config import create_db, load_json_to_db


def main():
    db_path = 'conversion_dict.db'
    json_path = 'convert_dict.json'
    if not os.path.exists(db_path) or not os.path.exists(json_path):
        create_db(db_path)
        load_json_to_db(db_path, json_path)
        logger.info(f"Database created at {db_path}")
        logger.info(f"Database created and loaded with data from {json_path}")
    else:
        logger.info(f"Database already exists at {db_path}")
        logger.info(f"Loading data from {json_path} to database")
        load_json_to_db(db_path, json_path)
