import json
import logging
import re



vars_dict = {
    "configP": "bot.configP",
    "bot_name": "bot.bot_name",
    "other_info": "bot.other_info",
    "returned_values": "bot.returned_values",
    "current_row": "bot.current_row",
    "current_patient": "bot.current_patient",
    "sheet": "bot.sheet",
    "todays_date": "bot.todays_date",
    "gsheet_columns": "bot.gsheet_columns",
    "clinic_name": "bot.current_patient['clinic_name']",
    "carrier_name": "bot.current_patient['carrier_name']",
    "member_id": "bot.current_patient['member_id']",
    "zip_code": "bot.current_patient['zip_code']",
    "policyh_name": "bot.current_patient['policyh_name']",
    "policyh_last_name": "bot.current_patient['policyh_last_name']",
    "policyh_dob": "bot.current_patient['policyh_dob']",
    "patient_name": "bot.current_patient['patient_name']",
    "patient_last_name": "bot.current_patient['patient_last_name']",
    "patient_dob": "bot.current_patient['patient_dob']",
    "relationship": "bot.current_patient['relationship']",
    "status": "bot.current_patient['status']",
    "state_verification": "bot.current_patient['state_verification']",
    "verification_type": "bot.current_patient['verification_type']",
    "primary": "bot.current_patient['primary']",
    "comments": "bot.current_patient['comments']",
    "Appointment Codes": "bot.current_patient['Appointment Codes']",
    "child_info": "bot.current_patient['child_info']",
    "Codes": "bot.current_patient['Codes']",
    "gsheet_credentials": "bot.gsheet_credentials",
    "appt_date": "bot.appt_date",
    "gdrive_credentials": "bot.gdrive_credentials",
    "clinics": "bot.clinics",
    "zkeep_login_clients": "bot.zkeep_login_clients",
    "carriers_token": "bot.carriers_token",
    "short_configP": "bot.short_configP",
    "long_configP": "bot.long_configP",
    "result_integration": "bot.result_integration",
    "username": "bot.username",
    "password": "bot.password",
    "bot_indexes": "bot.bot_indexes",
    "bot_path": "bot.bot_path",
    "bots_path": "bot.bots_path",
    "modules_path": "bot.modules_path",
    "carriers_path": "bot.carriers_path",
    "state_parameter": "bot.state_parameter"
}

logger = logging.getLogger('app_logger')
object_select = ""
object_select_type = ""
list_vars = []
list_vars_bot = []

def translate_j_to_py(j_cod, conversion_d, output_file_path, level=1):
    global object_select, object_select_type, list_vars, list_vars_bot
    py_cod = j_cod
    #print("\nCODE", py_cod)


    vars_add = []
    python_code = ''

    #Manejo de sangria 
    indent='    '
    current_indent = indent * level
    next_indent = indent * (level + 1)

    group = py_cod['group']
    comando = json.dumps(py_cod['command'])
    vars_in_command = list(set(re.findall(r'\{(.*?)\}', comando)))
    comand = re.sub(r'["\']?\{([^}]*)\}["\']?', r'\1', py_cod['command'])
    if isinstance(py_cod, dict) and 'father' in py_cod and py_cod['father'] in conversion_d:
        
        # se evalua cada grupo
        if group == 'scripts':
            if str(py_cod['father']).lower() == 'execrocketbotdb':
                for var in list_vars_bot:
                    python_code += f'{current_indent}bot.setvar(\"{var}\", {var})' + '\n'    
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}' + f'(f\"C:/DentalRobot/IV/Carriers/Bots/{{bot_name}}/{py_cod["command"]}.py\")' + '\n'
                inject_vars(["bot_name"], output_file_path)
            if str(py_cod['father']).lower() == 'execpython': 
                if py_cod["var"] != "":
                    python_code += f'{current_indent}{conversion_d[py_cod["father"]]}({py_cod["var"]}, bot)'+'\n'
                else: 
                    python_code += f'{current_indent}{conversion_d[py_cod["father"]]}({comando}, bot)'+'\n'
        elif group == 'web':   
            if str(py_cod['father']).lower() == 'execjs':
                var = py_cod['getvar']

                comando, varss =  extract_vars(eval(comando))  

                inject_vars(varss, output_file_path)
                    
                comando = comando.encode().decode('unicode_escape') 
                comando = aplicar_sangria(comando, current_indent)

                if var == '':
                    if len(varss) > 0:
                        python_code += f'{current_indent}{conversion_d[py_cod["father"]]}(r"""{comando}""",{", ".join(varss)})' + '\n'   
                    else:            
                        python_code += f'{current_indent}{conversion_d[py_cod["father"]]}(r"""{comando}""")' + '\n'
                else:
                    if var not in list_vars:
                        list_temp = [var]
                        inject_vars([var], output_file_path)
               
                    if len(varss) > 0:
                        python_code += f'{current_indent}{var} = {conversion_d[py_cod["father"]]}(r"""{comando}""",{", ".join(varss)})' + '\n'
                    else:
                        python_code += f'{current_indent}{var} = {conversion_d[py_cod["father"]]}(r"""{comando}""")' + '\n'
            elif str(py_cod['father']).lower() == 'injectjs':
                python_code += f'{current_indent}js =  requests.get({comando}).text' + '\n'
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}(js)' + '\n'
            
            elif str(py_cod['father']).lower() == 'waitforobject':
                comando_json= json.loads(py_cod['command'])
                object_select = str(comando_json["object"])
                object_select_type = str(py_cod["option"])

                if int(comando_json['before']) != 0:
                    python_code += f'{current_indent}sleep({comando_json["before"]})' + '\n'
 
                if py_cod["getvar"] == "":
                    python_code += f'{current_indent}{conversion_d[py_cod["father"]]}(\"{comando_json["wait_for"]}\",\"{py_cod["option"]}\",\"{comando_json["object"]}\",{comando_json["wait_time"]})' + '\n'
                else:
                    python_code += f'{current_indent}{py_cod["getvar"]} = {conversion_d[py_cod["father"]]}(\"{comando_json["wait_for"]}\",\"{py_cod["option"]}\",\"{comando_json["object"]}\",{comando_json["wait_time"]})' + '\n'

                if int(comando_json['after']) != 0:
                    python_code += f'{current_indent}sleep({comando_json["after"]})' + '\n'

            elif str(py_cod['father']).lower() == 'sendkeyweb':
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}(\"{py_cod["option"]}\",\"{object_select}\",\"{object_select_type}\",{comando})' + '\n'
            
            elif str(py_cod['father']).lower() == 'clickweb':
                object_select = str(comand)
                object_select_type = str(py_cod["option"])

                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}({comando},0,\"{py_cod["option"]}\")' + '\n'

            elif str(py_cod['father']).lower() == 'openurl':
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}({comando})' + '\n'

            elif str(py_cod['father']).lower() == 'countwindow':
                python_code += f'{current_indent}{comand} = {conversion_d[py_cod["father"]]}()' + '\n'
            elif str(py_cod['father']).lower() == 'closewindow':
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}(\"{py_cod["option"]}\", {comando})' + '\n'
            elif str(py_cod['father']).lower() == 'getwindowhandle':
                python_code += f'{current_indent}{comand} = {conversion_d[py_cod["father"]]}()' + '\n'
            elif str(py_cod['father']).lower() == 'getwindowtitle':
                python_code += f'{current_indent}{comand} = {conversion_d[py_cod["father"]]}()' + '\n'
            elif str(py_cod['father']).lower() == 'switchtowindow':
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}({comand},\"{py_cod["option"]}\")' + '\n'
            elif str(py_cod['father']).lower() == 'maximize':
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}()' + '\n'
            elif str(py_cod['father']).lower() == 'minimize':
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}()' + '\n'
            elif str(py_cod['father']).lower() == 'killdriver':
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}()' + '\n'
            elif str(py_cod['father']).lower() == 'swichtoframe':
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}({comando},\"{py_cod["option"]}\")' + '\n'
            elif str(py_cod['father']).lower() == 'swichtodefaultcontent': 
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}()' + '\n'

        elif group == 'logic':       
            if str(py_cod['father']).lower() == 'evaluateif':    
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}'+' '+f'{comand}:' + '\n'
                inject_vars(vars_in_command, output_file_path)
         
                # Procesa los hijos del bloque "if"
                for child in py_cod['children']:
                    python_code += translate_j_to_py(child, conversion_d, output_file_path, level + 1)

                                    
                # Procesa el bloque "else"
                if len(py_cod['else']) > 0:
                    python_code += f'{current_indent}{conversion_d["else"]}:' + '\n'
                    for els in py_cod['else']:
                       python_code += translate_j_to_py(els, conversion_d, output_file_path, level + 1)

            elif str(py_cod['father']).lower() == 'for':
                var = py_cod['var']
                comand_as_json = json.loads(py_cod['command'])
                cmd = comand_as_json['iterable'].replace("{", "").replace("}", "")
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}'+' i in range('+f'len({cmd})):' + '\n'
                python_code += f'{next_indent}{var} = i + 1' + '\n'
                
                # Procesa los hijos del bloque "for"
                for child in py_cod['children']:
                    python_code += translate_j_to_py(child, conversion_d,output_file_path, level + 1)

            elif str(py_cod['father']).lower() == 'evaluatewhile':
  
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}'+' '+f'{comand}:' + '\n'


                # Procesa los hijos del bloque "While"
                for child in py_cod['children']:
                    python_code += translate_j_to_py(child, conversion_d, output_file_path, level + 1)

            elif str(py_cod['father']).lower() == 'break':
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]} '+ '\n' 

            elif str(py_cod['father']).lower() == 'trycatch':   
                python_code += f'{current_indent}{conversion_d[py_cod["father"]]}:'+ '\n'
                
                # Procesa los hijos del bloque "try"
                for child in py_cod['children']:
                    python_code += translate_j_to_py(child, conversion_d, output_file_path, level + 1)

                python_code += f'{current_indent}except:'+ '\n'

                  # Procesa los hijos del bloque "execpt"
                for child in py_cod['else']:
                    python_code += translate_j_to_py(child, conversion_d, output_file_path, level + 1)       

        elif group == 'system':        
            if str(py_cod['father']).lower() == 'setvar':
                var = py_cod['var']    
                com = py_cod['command']
                matches = re.findall(r"\{(.*?)\}", com)
 
                if matches:
                    print("\nMACHES", matches)
          
                    for match in matches:
                        if match not in list_vars:
                            if match != '' and ":" not in match and "," not in match:
                                print("ENTRO")
                                obten = f'bot.getvar(\"{match}\")'
                                com = com.replace(f"\"{{{match}}}\"", obten)
                                com = com.replace(f"{{{match}}}", obten)
                                comand = com
                            else:
                                comand = com
                if var in list_vars_bot:
                    python_code += f'{current_indent}{var} = {comand}' + '\n'
                elif var in list_vars: 
     
                    python_code += f'{current_indent}{var} = {comand}' + '\n'
                    python_code += f'{current_indent}{conversion_d[py_cod["father"]]}(\"{var}\",{comand}) ' + '\n'
                else:
                    python_code += f'{current_indent}{conversion_d[py_cod["father"]]}(\"{var}\",{comand}) ' + '\n'

            elif str(py_cod['father']).lower() == 'wait':
          
                 python_code += f'{current_indent}{conversion_d[py_cod["father"]]}(float({comand}))' + '\n'        
                
        if py_cod['father'] == 'module':
            comand_as_json = json.loads(py_cod['command'])
            modul =  comand_as_json['module']
          
            if len(comand_as_json)  > 2:
                if modul.lower() == 'carrieralert':
                    python_code += f'{current_indent}{conversion_d[modul]}(module=\"{comand_as_json["module_name"]}\", command=\"{modul}\",  params={{ \'text\': f\"{comand_as_json["text"]}\"}})' + '\n'  
                elif modul.lower() == 'carrieralert2fa':
                    python_code += f'{current_indent}{conversion_d[modul]}(module=\"{comand_as_json["module_name"]}\", command=\"{modul}\",  params={{ \'text\': f\"{comand_as_json["text"]}\"}})' + '\n'                 
                elif modul.lower() == 'gethandle':
                    python_code += f'{current_indent}{conversion_d[modul]}(module=\"{comand_as_json["module_name"]}\", command=\"{modul}\",  params={{ \'var\': f\"{comand_as_json["var"]}\"}})' + '\n'    
                elif modul.lower() == 'cleanvars':
                    variables = comand_as_json["vars"].split(",")
                    for var in variables:
                        if var in list_vars:
                            python_code += f'{current_indent}{var} = \"\"' + '\n'
                    python_code += f'{current_indent}{conversion_d[modul]}(module=\"{comand_as_json["module_name"]}\", command=\"{modul}\",  params={{ \'vars\': \"{comand_as_json["vars"]}\"}})' + '\n'                      
                elif modul.lower() == 'chromemode':
                    python_code += f'{current_indent}{conversion_d[modul]}(module=\"{comand_as_json["module_name"]}\", command=\"{modul}\",  params={{ \'mode\': \" {comand_as_json["mode"]}\", \'url\': {var_in_text(comand_as_json["url"])}}})' + '\n'                  
                elif modul.lower() == 'sendkeys':
                    python_code += f'{current_indent}{conversion_d[modul]}(module=\"{comand_as_json["module_name"]}\", command=\"{modul}\",  params={{ \'special\': \" {comand_as_json["special"]}\", \'text\': f{var_in_text(comand_as_json.get("text",""))}}})' + '\n'                  
                elif modul.lower() == 'openbrowser':
                    python_code += f'{current_indent}{conversion_d[modul]}(module=\"{comand_as_json["module_name"]}\", command=\"{modul}\",  params={{ \'profile_chrome\': {var_in_text(comand_as_json["profile_chrome"])}, \'timeout_chrome\': {comand_as_json["timeout_chrome"]},\'url_chrome\': {var_in_text(comand_as_json["url_chrome"])} }})' + '\n'  
                elif modul.lower() == 'instantprinter':
                    python_code += f'{current_indent}{conversion_d[modul]}(module=\"{comand_as_json["module_name"]}\", command=\"{modul}\",  params={{ \'onlyMove\': {comand_as_json["onlyMove"]}, \'waitDocument\': {comand_as_json["waitDocument"]}}})' + '\n'  
                elif modul.lower() == 'changeiframepro':
                    python_code += f'{current_indent}{conversion_d[modul]}(module=\"{comand_as_json["module_name"]}\", command=\"{modul}\",  params={{ \'data_type\': \"{comand_as_json["data_type"]}\", \'data\': \"{comand_as_json["data"]}\" , \'wait\': {comand_as_json["wait"]}}})' + '\n'                  
                elif modul.lower() == 'cleaninputs':
                    var = comand_as_json["texto"].replace('{', '').replace('}', '')
                    inject_vars([var], output_file_path)
                    python_code += f'{current_indent}{conversion_d[modul]}(module=\"{comand_as_json["module_name"]}\", command=\"{modul}\",  params={{ \'search_data\': \"{comand_as_json["search_data"]}\", \'texto\': {comand_as_json["texto"]}, \'tipo\': \"{comand_as_json["tipo"]}\" }})' + '\n'            
                elif modul.lower() == 'clickpro':  
                    python_code += f'{current_indent}{conversion_d[modul]}(module=\"{comand_as_json["module_name"]}\", command=\"{modul}\",  params={{ \'data\': \"{comand_as_json["data"]}\", \'data_type\': \"{comand_as_json["data_type"]}\", \'wait\': {comand_as_json["wait"]} }})' + '\n'                                      
                elif modul.lower() == 'setvariable':
                    comand_as_json = json.loads(py_cod['command'])  
                    varss = comand_as_json['vars']
                    varss_list = varss.split(",")
                    datas = comand_as_json['data']
                    datas = datas.replace("'", '"') 
                    datas =  json.loads(datas)
                    for i in range(len(varss_list)):
                        if datas[i] == "":
                            if varss_list[i] in list_vars:
                                python_code += f'{current_indent}{varss_list[i]} = \"\"' + '\n' 
                            else:                     
                                python_code += f'{current_indent}bot.setvar(\"{varss_list[i]}\", \"\")' + '\n'   
                        else:  
                            if varss_list[i] in list_vars:                  
                                python_code += f'{current_indent}{varss_list[i]} = {datas[i]}' + '\n' 
                            else:
                                python_code += f'{current_indent}bot.setvar(\"{varss_list[i]}\", {datas[i]})' + '\n'
                else: 
                    logger.error(f"Error: {modul} not found in conversion dictionary")
            else:
                python_code += f'{current_indent}bot.execute_command(module=\"{comand_as_json["module_name"]}\", command=\"{modul}\")' + '\n'  


            

    else:
        logger.error(f"Error: {py_cod} not found in conversion dictionary")

    return python_code



def aplicar_sangria(texto, indent):
    lineas = texto.split('\n')
    texto_indentado = '\n'.join(indent + linea for linea in lineas)
    return texto_indentado

def translate_var_to_python(j_cod):
    global list_vars, list_vars_bot
    py_cod = j_cod
    indent='    '
    python_code = ''
    logger.debug(f"Variable to convert: {py_cod['name']}")
    if isinstance(py_cod, dict) and 'name' in py_cod:
        var = py_cod["data"]
        if var.lower() == 'true' or var.lower() == 'false':
            python_code += f'{indent}{py_cod["name"]} = {var}' + '\n'
        else:
            try:
                json.loads(var)
                python_code += f'{indent}{py_cod["name"]} = json.loads({json.dumps(var)})' + '\n'
            except json.JSONDecodeError:
                python_code += f'{indent}{py_cod["name"]} = {json.dumps(var)}' + '\n'
        list_vars.append(py_cod["name"])
        list_vars_bot.append(py_cod["name"])
    else:
        logger.error(f"Error: {py_cod['name']} not found in conversion dictionary")
    return python_code

def var_in_text(text):
    if text == "":
        return "\"\""
    return text if text.replace('{', '').replace('}', '') in list_vars else 'bot.getvar(\"' +  text.replace('{', '').replace('}', '') + '\")'
def extract_vars(text):
    modified_text = ""
    extracted_texts = []
    i = 0
    
    while i < len(text):
        if text[i] == '{' and text[i-1] != '$':


            j = i + 1
            while j < len(text) and j < i + 23:
                if text[j] == '{':
                    i = j - 1 
                   
                    break
                if text[j] == '}':
                    extracted_texts.append(text[i+1:j])
                    modified_text += text[i+1:j]  
                    i = j  
                    break
                j += 1
            else:
                modified_text += text[i]  
        else:
            modified_text += text[i]
        
        i += 1

    filtered_texts = list({
    text for text in extracted_texts 
    if len(text) > 1 and "," not in text and text.strip() != "" and "=" not in text and '"' not in text and ";" not in text and ":" not in text and "." not in text
    })
  
    output = [f"const {var} = arguments[{i+1}];" for i, var in enumerate(filtered_texts)]
    
    modified_text = '\n'.join(output) + '\n' + modified_text 

    return modified_text, filtered_texts



def inject_vars(varss, output_file_path):
    global list_vars
    missing_vars = [var for var in varss if var not in list_vars]

    if len(missing_vars) > 0:
        vars_add = [f"{var} = {vars_dict[var]}" if var in vars_dict else f"{var} = bot.getvar(\"{var}\")" for var in missing_vars]
        list_vars.extend(missing_vars)
     

        with open(output_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()


        insert_index = None
        for i, line in enumerate(lines):
            if line.strip().startswith("def run(bot):"):
                insert_index = i + 1  
                break

        for var in reversed(vars_add):  
            lines.insert(insert_index, f"    {var}\n") 

        with open(output_file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)
