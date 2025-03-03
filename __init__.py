from json import load
from pathlib import Path
import os
import sys
import shutil

current_path = Path(os.getcwd()).resolve()
sys.path.append(os.path.join(current_path, 'modules', 'castj2py'))

from src.main import run
from src.initialize_db import main
from src.conection_api import get_id_bot, get_updates_bot, get_file_bot

try:
    module = GetParams("module")

    if module == "convertJson2Py":
        token = GetVar("carriers_token")
        bot_name = GetParams("inputBotName")
        bot_id = get_id_bot(bot_name, token)

        if(bot_id == None):
            print("\n")
            print("+-------------------------+")
            print("|     Bot not found       |")
            print("+-------------------------+")
    
        else: 
            ruta_bot_dir = os.path.join(current_path, 'modules', 'castj2py', 'samples', bot_name)
            # Eliminar el directorio si existe
            if os.path.exists(ruta_bot_dir):
                shutil.rmtree(ruta_bot_dir) 

            # Crear el directorio
            os.makedirs(ruta_bot_dir)
            updates = get_updates_bot(bot_id)
            for update in updates:
                file_json = get_file_bot(update)                
                bot_name_lower = str(update).replace(".json", "").replace(" ", "_").lower()
                # crear el fichero samples/bot_name .py
                ruta_bot = os.path.join(current_path, 'modules', 'castj2py', 'samples', bot_name,f'{bot_name_lower}.py')
                if not os.path.exists(ruta_bot):
                    with open(ruta_bot, 'w') as file:
                        file.write('import json\n'  + 'from time import sleep\n' + 'import requests\n' + 'def run(bot):\n')
                else:
                    with open(ruta_bot, 'w') as file:
                        file.write('import json\n' + 'import time\n' + 'def run(bot):\n')
                # Initializar la database

                main()
                
                run(update, file_json , ruta_bot)
      
except Exception as e:
    print(f"Error: {e}")
    raise e
