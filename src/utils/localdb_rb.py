import sqlite3
import os
import logging

logger = logging.getLogger('app_logger')


def load_db_bots(db_path):
    is_file = os.path.isfile(db_path)
    if is_file is False:
        logger.error(f"File not found: {db_path}")
        return []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bots")
    bots = cursor.fetchall()
    conn.close()
    return bots
