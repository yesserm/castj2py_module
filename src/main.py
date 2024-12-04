import os
from pathlib import Path
import sys
import base64

current_path = Path(os.getcwd()).resolve()
sys.path.append(os.path.join(current_path, 'modules', 'castj2py', 'src'))

from .utils.bots_rb import BotsRB
from utils.logging_config import configure_logging
from .core.converter import convert_json_to_python

logger = configure_logging()

path_samples = os.path.join(current_path, 'modules', 'castj2py', 'samples')

try:
    logger.debug("Bot creado")

    def run(bot_name):
        logger.debug(f"Bot corriendo {bot_name}")
        db_path = os.path.join(current_path, 'robot.db')
        bots = BotsRB(db_path)
        bots_names = bots.get_bot_names()
        logger.debug(f"Bot from db: {len(bots_names)}")
        if bot_name in bots_names:
            logger.debug(f"Bot {bot_name} found")
            bot = bots.get_bots_recent()[bots_names.index(bot_name)]
            bot_data = str(bot[2])
            bot_data_decoded = base64.b64decode(bot_data.encode()).decode()
            bot_data_decoded = bot_data_decoded.replace("'", '"')
            logger.debug(f"Bot data: {bot_data_decoded}")
        convert_json_to_python('ruta json', path_samples)
        pass
except Exception as e:
    logger.error(f"Error: there is a error running bot")
    raise e
