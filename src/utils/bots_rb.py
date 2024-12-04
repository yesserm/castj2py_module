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

    def get_bots_recent(self):
        bots_ids = []
        bots_recent = []
        for bot in reversed(self._bots):
            if bot[0] not in bots_ids:
                if len(bots_recent) == 0:
                    bots_recent.append(bot)
                    bots_ids.append(bot[0])
                else:
                    if bot[1] != bots_recent[-1][1]:
                        bots_recent.append(bot)
                        bots_ids.append(bot[0])
        return bots_recent

    def get_bot_names(self):
        bots_recent = self.get_bots_recent()
        return [bot[1] for bot in bots_recent]
