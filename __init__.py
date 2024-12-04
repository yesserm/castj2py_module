from json import load
from pathlib import Path
import os
import sys

current_path = Path(os.getcwd()).resolve()
sys.path.append(os.path.join(current_path, 'modules', 'castj2py'))

from src.main import run

try:
    module = GetParams("module")

    if module == "convertJson2Py":
        bot_name = GetParams("inputBotName")
        run(bot_name)
except Exception as e:
    print(f"Error: {e}")
    raise e
