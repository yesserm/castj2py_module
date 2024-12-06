import json
import logging
import base64
import os

from .json_loader import get_all_commands
from .translator import translate_j_to_py

logger = logging.getLogger('app_logger')

json_dict = {}


def convert_json_decoded_to_python(json_decoded, output_file_path, conversion_dict):
    logger.debug(f"Converting json {isinstance(json_decoded, dict)} to Python code and saving to"
                 f" {output_file_path}")
    if os.path.exists(output_file_path):
        try:
            all_comands_json = get_all_commands(json_decoded)
            for command in all_comands_json:
                if command is not None:
                    try:
                        python_code = translate_j_to_py(command, conversion_dict)
                        logger.debug(f"Python code: {python_code}")
                        python_code = python_code + '\n'
                        with open(output_file_path, 'w') as file:
                            file.write(python_code)
                        logger.info(f"Conversion complete. Saved to {output_file_path}")
                    except Exception as e:
                        logger.error(f"Error converting JS to Python: {e}")
                        pass
        except Exception as e:
            logger.error(f"Error converting JSON to Python: {e}")
            raise e
    else:
        logger.error(f"Error: {output_file_path} does not exist")
        raise FileNotFoundError(f"Error: {output_file_path} does not exist")


def load_json_from_base64(encoded_str) -> dict:
    decoded_str = base64.b64decode(encoded_str).decode('utf-8')
    json_data = json.loads(decoded_str)
    return json_data


def load_json_dict(path_json):
    global json_dict
    with open(path_json, 'r') as file:
        json_d = json.load(file)
        json_dict = json_d
    return json_d
