import sys
import os
import glob
import shutil

sys.path.insert(
    0, os.path.join(os.path.abspath(os.getcwd()), os.path.normpath("modules/castj2py/libs"))
)

from Cython.Build import cythonize 
from setuptools import setup
ruta = os.environ.get("ruta_bot")

if not os.path.exists(ruta):
    print("No se encontro la carpeta del bot dentro de samples")
else:
    ficheros = [os.path.join(ruta, f) for f in os.listdir(ruta) if f.endswith(".py")]


    os.chdir(ruta)
    setup(
        ext_modules=cythonize(ficheros)
    )

    for file in glob.glob(os.path.join(ruta, "*.c")):
        os.remove(file)
    shutil.rmtree(ruta + r"\build")