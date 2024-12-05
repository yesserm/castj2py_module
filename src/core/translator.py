import re
import logging

logger = logging.getLogger('app_logger')


def translate_j_to_py(j_cod, conversion_d):
    sorted_keys = sorted(conversion_d.keys(), key=len, reverse=True)
    py_cod = j_cod
    for key in sorted_keys:
        pattern = re.escape(key)
        py_cod = re.sub(pattern, conversion_d[key], py_cod)

    py_cod = re.sub(r'\bvar\b', '', py_cod)
    py_cod = re.sub(r'(\w+)\(\)\s*{', r'\1():', py_cod)
    py_cod = re.sub(r'\b(\w+)\s*:\s*', r'\1 = ', py_cod)
    return py_cod.strip()

