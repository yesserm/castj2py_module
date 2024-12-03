import os
from pathlib import Path
import sys

current_path = Path(os.getcwd()).resolve()
sys.path.append(os.path.join(current_path, 'modules', 'castj2py', 'src'))

from utils.logging_config import configure_logging
from .core.converter import convert_json_to_python

logger = configure_logging()

path_samples = os.path.join(current_path, 'modules', 'castj2py', 'samples')

try:
    logger.info("Bot creado")


    def run(bot_name):
        logger.info("Versión de Python:", sys.version)
        logger.info(f"Bot corriendo {bot_name}")
        convert_json_to_python('ruta json',  path_samples)
        pass
except Exception as e:
    logger.error(f"Error: {e}")
    raise e

run(bot_name="vacio")
