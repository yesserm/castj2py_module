import os
import sqlite3
import logging

from src.utils.localdb_rb import load_db_bots

logger = logging.getLogger('app_logger')


class BotsRB:
    _instance = None
    _bots = []

    def __new__(cls, db_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if db_path is not None:
                cls._bots = cls.load_db_bots(db_path)
        return cls._instance

    @staticmethod
    def load_db_bots(db_path):
        bots_loaded = []
        bots_loaded = load_db_bots(db_path)
        return bots_loaded

    def get_bots(self):
        return self._bots
