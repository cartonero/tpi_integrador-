"""
servicios/cargador_datos.py — Carga de datos desde el JSON.

Es el puente entre los datos crudos (archivo datos/games.json) y los
objetos del programa (Juego y Catalogo).

Flujo de datos:
    datos/games.json  ->  lista de diccionarios  ->  objetos Juego  ->  Catalogo

El archivo datos/games.json es una muestra reducida (2000 juegos) del
dataset completo de Steam. La genera algoritmos/preparar_datos.py.
"""
import json
from pathlib import Path

from modelos.juego import Juego
from modelos.catalogo import Catalogo

# Ruta del JSON calculada a partir de la ubicación de ESTE archivo
# (servicios/cargador_datos.py): subimos dos niveles hasta la raíz del
# proyecto y de ahí entramos a datos/games.json. Así funciona sin importar
# desde qué carpeta se ejecute el programa.
RUTA_JSON_POR_DEFECTO = Path(__file__).resolve().parent.parent / "datos" / "games.json"


def cargar_catalogo(ruta_json=RUTA_JSON_POR_DEFECTO):
    """Lee el JSON de juegos y arma un Catalogo con objetos Juego.

    Si no se indica otra ruta, usa datos/games.json de este proyecto.
    """
    catalogo = Catalogo()

    # Abrimos el archivo en UTF-8 para que los nombres con tildes o con
    # caracteres de otros idiomas (por ejemplo chino) se lean bien.
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        # Resultado: una lista de diccionarios, uno por juego.
        juegos_raw = json.load(archivo)

    for datos in juegos_raw:
        # Cada diccionario trae más campos (tiempo de juego, votos...), pero
        # el modelo Juego solo usa estos tres. .get() devuelve el valor por
        # defecto si la clave no existe, así un registro incompleto no
        # rompe la carga.
        juego = Juego(
            appid=datos.get("appid"),
            nombre=datos.get("name"),
            generos=datos.get("genres", []),
        )
        # agregar() descarta los juegos cuyo appid ya está cargado.
        catalogo.agregar(juego)

    return catalogo