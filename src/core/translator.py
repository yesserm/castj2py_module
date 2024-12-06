import json
import logging

logger = logging.getLogger('app_logger')


def translate_j_to_py(j_cod, conversion_d):
    py_cod = j_cod
    python_code = ''
    if isinstance(py_cod, dict) and 'father' in py_cod and py_cod['father'] in conversion_d:
        comando = json.dumps(py_cod['command'])
        # execjs
        if str(py_cod['father']).lower() == 'execjs':
            python_code += f'{conversion_d[py_cod["father"]]}({comando})' + '\n'
        elif str(py_cod['father']).lower() == 'if':
            python_code += f'{conversion_d[py_cod["father"]]}({comando})' + '\n'
    else:
        logger.error(f"Error: {py_cod} not found in conversion dictionary")

    return python_code


def translate_var_to_python(j_cod):
    py_cod = j_cod
    python_code = ''
    logger.debug(f"Variable to convert: {py_cod['name']}")
    if isinstance(py_cod, dict) and 'name' in py_cod:
        python_code += f'{py_cod["name"]} = json.loads({json.dumps(py_cod["data"])})' + '\n'
    else:
        logger.error(f"Error: {py_cod['name']} not found in conversion dictionary")
    return python_code
