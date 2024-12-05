import os
from pathlib import Path
import sys
import base64

current_path = Path(os.getcwd()).resolve()
sys.path.append(os.path.join(current_path, 'modules', 'castj2py', 'src'))

from .utils.bots_rb import BotsRB
from utils.logging_config import configure_logging
from .core.converter import load_json_from_base64, convert_json_decoded_to_python
from initialize_db import main

logger = configure_logging()

path_samples = os.path.join(current_path, 'modules', 'castj2py', 'samples')

try:
    logger.debug("Bot creado")

    def run(bot_name):
        logger.debug(f"Bot corriendo {bot_name}")
        db_path = os.path.join(current_path, 'robot.db')
        sample_path = os.path.join(path_samples, 'convert_dict.json')
        sample_python = os.path.join(path_samples, 'convert_dict.py')
        bots = BotsRB(db_path)
        bots_names = bots.get_bot_names()
        if bot_name in bots_names:
            logger.debug(f"Bot {bot_name} found")
            bot = bots.get_bots_recent()[bots_names.index(bot_name)]
            bot_data = str(bot[2])
            bot_data_decoded = load_json_from_base64(bot_data.encode())
            convert_json_decoded_to_python(bot_data_decoded, sample_python)
except Exception as e:
    logger.error(f"Error: there is a error running bot")
    raise e

# Initialize the database
main()
