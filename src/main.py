import os
from pathlib import Path
from pdb import run
import sys


current_path = Path(os.getcwd()).resolve()
sys.path.append(os.path.join(current_path, 'modules', 'castj2py', 'src'))

from utils.logging_config import configure_logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logger = configure_logging()

try:
    logger.info("Bot creado")
    def run():
        logger.info("Bot corriendo")
        pass
except Exception as e:
    logger.error(f"Error: {e}")
    raise e

run()