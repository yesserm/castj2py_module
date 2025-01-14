import json
import logging

logger = logging.getLogger('app_logger')


def translate_j_to_py(j_cod, conversion_d, level=0):
    py_cod = j_cod
    print(f"\n code : {py_cod}")
    python_code = ''

    #Manejo de sangria 
    indent='    '
    current_indent = indent * level
    next_indent = indent * (level + 1)

    group = py_cod['group']
    comando = json.dumps(py_cod['command'])
    comand = py_cod['command'].replace("{", "").replace("}", "")   
    if isinstance(py_cod, dict) and 'father' in py_cod and py_cod['father'] in conversion_d:
        
        # se evalua cada grupo
        if group == 'web':   
            if str(py_cod['father']).lower() == 'execjs':
                var = py_cod['getvar']
                if var == '':
                    python_code += f'{current_indent}{conversion_d[py_cod["father"]]}(f{comando})' + '\n'
                else:
                    python_code += f'{current_indent}{var} = {conversion_d[py_cod["father"]]}(f{comando})' + '\n'

        elif group == 'logic':       
            if str(py_cod['father']).lower() == 'evaluateif':    
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}'+' '+f'{comand}:' + '\n'

                # Procesa los hijos del bloque "if"
                for child in py_cod['children']:
                    python_code += translate_j_to_py(child, conversion_d, level + 1)

                                    
                # Procesa el bloque "else"
                if len(py_cod['else']) > 0:
                    python_code += f'{current_indent}{conversion_d["else"]}:' + '\n'
                    for els in py_cod['else']:
                       python_code += translate_j_to_py(els, conversion_d, level + 1)

            elif str(py_cod['father']).lower() == 'for':
                var = py_cod['var']
                comand_as_json = json.loads(py_cod['command'])
                cmd = comand_as_json['iterable'].replace("{", "").replace("}", "")
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}'+' i in range('+f'len({cmd})):' + '\n'
                python_code += f'{next_indent}{var} = i + 1' + '\n'
                
                # Procesa los hijos del bloque "for"
                for child in py_cod['children']:
                    python_code += translate_j_to_py(child, conversion_d, level + 1)

            elif str(py_cod['father']).lower() == 'evaluatewhile':
  
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}'+' '+f'{comand}:' + '\n'

                # Procesa los hijos del bloque "While"
                for child in py_cod['children']:
                    python_code += translate_j_to_py(child, conversion_d, level + 1)

            elif str(py_cod['father']).lower() == 'break':
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]} '+ '\n' 

            elif str(py_cod['father']).lower() == 'trycatch':   
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}:'+ '\n'
                
                # Procesa los hijos del bloque "try"
                for child in py_cod['children']:
                    python_code += translate_j_to_py(child, conversion_d, level + 1)

                python_code += f'{current_indent}except:'+ '\n'

                  # Procesa los hijos del bloque "execpt"
                for child in py_cod['else']:
                    python_code += translate_j_to_py(child, conversion_d, level + 1)       

        elif group == 'system':        
            if str(py_cod['father']).lower() == 'setvar':
                var = py_cod['var']    
                python_code += f'{current_indent}{var} {conversion_d[py_cod["father"]]} {comand}'

            elif str(py_cod['father']).lower() == 'wait':
                 print("\n entro")
                 python_code += f'{current_indent}{conversion_d[py_cod["father"]]}(float({comand}))'        
                

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
