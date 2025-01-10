import json
import logging

logger = logging.getLogger('app_logger')


def translate_j_to_py(j_cod, conversion_d):
    py_cod = j_cod
    print(f"\n code : {py_cod}")
    python_code = ''
    block='    '
    group = py_cod['group']
    comando = json.dumps(py_cod['command'])
    if isinstance(py_cod, dict) and 'father' in py_cod and py_cod['father'] in conversion_d:
        if group == 'web':

            # execjs    
            if str(py_cod['father']).lower() == 'execjs':
                var = py_cod['getvar']
                if var == '':
                    python_code += f'{conversion_d[py_cod["father"]]}(f{comando})' + '\n'
                else:
                    python_code += f'{var} = {conversion_d[py_cod["father"]]}(f{comando})' + '\n'

        elif group == 'logic':       
            if str(py_cod['father']).lower() == 'evaluateif':
                comand = py_cod['command'].replace("{", "").replace("}", "")     
                python_code += f'{conversion_d[py_cod["father"]]}'+' '+f'{comand}:' + '\n'
                for child in py_cod['children']:
                    python_code += f'{block}{translate_j_to_py(child, conversion_d)}'
                python_code += f'{conversion_d["else"]}:' + '\n'
                for els in py_cod['else']:
                    python_code += f'{block}{translate_j_to_py(els, conversion_d)}'
    else:
        logger.error(f"Error: {py_cod} not found in conversion dictionary")

    return python_code


def translate_var_to_python(j_cod):
    py_cod = j_cod
    python_code = ''
    logger.debug(f"Variable to convert: {py_cod['name']}")
    if isinstance(py_cod, dict) and 'name' in py_cod:
        var = py_cod["data"]
        if var.lower() == 'true' or var.lower() == 'false':
            python_code += f'{py_cod["name"]} = {var}' + '\n'
        else:
            try:
                json.loads(var)
                python_code += f'{py_cod["name"]} = json.loads({json.dumps(var)})' + '\n'
            except json.JSONDecodeError:
                python_code += f'{py_cod["name"]} = {json.dumps(var)}' + '\n'

    else:
        logger.error(f"Error: {py_cod['name']} not found in conversion dictionary")
    return python_code
