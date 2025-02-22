from json import load
from pathlib import Path
import os
import sys

current_path = Path(os.getcwd()).resolve()
sys.path.append(os.path.join(current_path, 'modules', 'castj2py'))

from src.main import run
from src.initialize_db import main

try:
    module = GetParams("module")

    if module == "convertJson2Py":
        bot_name = GetParams("inputBotName")
   
        bot_name_lower = str(bot_name).replace(" ", "_").lower()
        # crear el fichero samples/bot_name .py
        ruta_bot = os.path.join(current_path, 'modules', 'castj2py', 'samples', f'{bot_name_lower}.py')
        if not os.path.exists(ruta_bot):
            with open(ruta_bot, 'w') as file:
                file.write('import json\n'  + 'import time\n' + 'def run(bot):\n')
        else:
            with open(ruta_bot, 'w') as file:
                file.write('import json\n' + 'import time\n' + 'def run(bot):\n')
        # Initializar la database

        main()
   
        run(bot_name, ruta_bot)
      
except Exception as e:
    print(f"Error: {e}")
    raise e
