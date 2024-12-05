import json
import logging
import base64
import os

logger = logging.getLogger('app_logger')

json_dict = {}


def convert_json_decoded_to_python(json_decoded, output_file_path):
    logger.debug(f"Converting {json_decoded} to Python code and saving to {output_file_path}")
    if os.path.exists(output_file_path):
        try:
            python_code = json.dumps(json_decoded, indent=4)
            with open(output_file_path, 'w') as file:
                file.write(python_code)
            logger.info(f"Conversion complete. Saved to {output_file_path}")
        except Exception as e:
            logger.error(f"Error converting JSON to Python: {e}")
            raise e
    else:
        logger.error(f"Error: {output_file_path} does not exist")
        raise FileNotFoundError(f"Error: {output_file_path} does not exist")


def load_json_from_base64(encoded_str):
    decoded_str = base64.b64decode(encoded_str).decode('utf-8')
    json_data = json.loads(decoded_str)
    return json_data


def load_json_dict(path_json):
    global json_dict
    with open(path_json, 'r') as file:
        json_d = json.load(file)
        json_dict = json_d
    return json_d
