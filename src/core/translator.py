import json
import logging

logger = logging.getLogger('app_logger')


def translate_j_to_py(j_cod, conversion_d):
    py_cod = j_cod
    python_code = ''
    if isinstance(py_cod, dict) and 'father' in py_cod and py_cod['father'] in conversion_d:
        comando = json.dumps(py_cod['command'])
        python_code += f'{conversion_d[py_cod["father"]]}({comando})' + '\n'
    else:
        logger.error(f"Error: {py_cod} not found in conversion dictionary")

    return python_code
