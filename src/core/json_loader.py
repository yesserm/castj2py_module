import json
import logging

json_file_object = {}

logger = logging.getLogger('app_logger')


def load_json_file(file_path):
    global json_file_object
    with open(file_path, 'r') as file:
        json_file_object = json.load(file)
        return json_file_object


def get_json_file():
    return json_file_object


def get_js_code():
    global json_file_object
    js_code_list = []
    if json_file_object and json_file_object['project']['commands']:
        for command in json_file_object['project']['commands']:
            if 'command' in command and command['father'] == 'execJs':
                js_code_list.append(command['command'])
        return js_code_list
    return js_code_list


def get_all_commands(json_decoded=None):
    global json_file_object
    commands_list = []
    if json_decoded and isinstance(json_decoded, dict):
        json_file_object = json_decoded
    else:
        logger.info(f"Error: json_decoded is not a dictionary")
        pass
    if json_file_object and json_file_object['project']['commands']:
        for command in json_file_object['project']['commands']:
            commands_list.append(command)
        logger.debug(f"Commands list: {commands_list}")
        return commands_list
    return commands_list
