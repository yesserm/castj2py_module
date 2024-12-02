import os
from pathlib import Path
import sys

current_path = Path(os.getcwd()).resolve()
sys.path.append(os.path.join(current_path, 'modules', 'castj2py', 'src'))

from utils.logging_config import configure_logging
from .core.converter import convert_json_to_python

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logger = configure_logging()

try:
    logger.info("Bot creado")


    def run():
        logger.info("Versión de Python:", sys.version)
        logger.info("Bot corriendo")
        convert_json_to_python('ruta json', 'ruta a guardar')
        pass
except Exception as e:
    logger.error(f"Error: {e}")
    raise e

run()
