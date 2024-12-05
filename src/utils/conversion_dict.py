import sqlite3
import os
from pathlib import Path


class ConversionDict:
    _instance = None
    _conversion_dict = None

    def __init__(self, db_path=None):
        if db_path is not None and self._conversion_dict is None:
            self._conversion_dict = self.load_conversion_dict(db_path)

    def __new__(cls, db_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if db_path is not None:
                cls._conversion_dict = cls.load_conversion_dict(db_path)
        return cls._instance

    @classmethod
    def load_conversion_dict(cls, db_path: str) -> dict:
        """Load the conversion dictionary from the database
        :param db_path: Path to the SQLite database
        :return: A dictionary with the conversion data
        """
        root_path = get_project_root()
        full_db_path = os.path.join(root_path, db_path)
        conn = sqlite3.connect(full_db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT j_code, py_code FROM conversion_dict')
        rows = cursor.fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows}

    def get_conversion_dict(self):
        return self._conversion_dict


def get_project_root():
    samples_path = os.path.join(Path(os.getcwd()).resolve(), 'modules', 'castj2py', 'samples')
    os.makedirs(samples_path, exist_ok=True)
    return samples_path

