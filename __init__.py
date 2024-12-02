from json import load
from pathlib import Path
import os
import sys

current_path = Path(os.getcwd()).resolve()
print(f"Current path: {current_path}")
print(f"Current path: {os.path.join(current_path, 'modules', 'castj2py')}")
sys.path.append(os.path.join(current_path, 'modules', 'castj2py'))

from src.main import run
                
try:
    module = GetParams("module")

    if module == "convertJson2Py":
        run()
        print('Bot creado')

except Exception as e:
    print(f"Error: {e}")
    raise e




