import os
from pathlib import Path
import sys

current_path = Path(os.getcwd()).resolve()
sys.path.append(os.path.join(current_path, 'modules', 'castj2py', 'src'))

from .utils.bots_rb import BotsRB
from utils.logging_config import configure_logging
from utils.conversion_dict import ConversionDict
from .core.converter import load_json_from_base64, convert_json_decoded_to_python, convert_json_var_to_python

logger = configure_logging()

path_samples = os.path.join(current_path, 'modules', 'castj2py', 'samples')

try:
    logger.debug("Bot creado")

    def run(bot_name, path):
        logger.debug(f"Bot corriendo {bot_name}")
        db_path = os.path.join(current_path, 'robot.db')
        sample_db = "conversion_dict.db"
        bots = BotsRB(db_path)
        conversion_instance = ConversionDict(sample_db)
        conversion_dict = conversion_instance.get_conversion_dict()
        bots_names = bots.get_bot_names()
        if bot_name in bots_names:
      
            bot = bots.get_bots_recent()[bots_names.index(bot_name)]
           
            bot_data = str(bot[2])
            bot_data_decoded = load_json_from_base64(bot_data.encode())
            convert_json_var_to_python(bot_data_decoded, path)
            convert_json_decoded_to_python(bot_data_decoded, path, conversion_dict)
            logger.debug(f"Bot {bot_name} executed")
        else:
            logger.error(f"Bot {bot_name} not found")
            raise FileNotFoundError(f"Error: {bot_name} not found")
except Exception as e:
    logger.error(f"Error: there is a error running bot")
    raise Exception(f"Error: there is a error running bot")
