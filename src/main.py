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

    def run(bot_name,bot_json, path):
        logger.debug(f"Bot corriendo {bot_name}")
        sample_db = "conversion_dict.db"
        conversion_instance = ConversionDict(sample_db)
        conversion_dict = conversion_instance.get_conversion_dict()
        convert_json_var_to_python(bot_json, path)
        convert_json_decoded_to_python(bot_json, path, conversion_dict)
        logger.debug(f"Bot {bot_name} executed")

except Exception as e:
    logger.error(f"Error: there is a error running bot")
    raise Exception(f"Error: there is a error running bot")
