import json

from modelos.juego import Juego
from modelos.catalogo import Catalogo


def cargar_catalogo(ruta_json="datos/games.json"):
    """Lee el JSON de juegos y arma un Catalogo con objetos Juego."""
    catalogo = Catalogo()

    with open(ruta_json, "r", encoding="utf-8") as archivo:
        juegos_raw = json.load(archivo)

    for datos in juegos_raw:
        juego = Juego(
            appid=datos.get("appid"),
            nombre=datos.get("name"),
            generos=datos.get("genres", []),
        )
        catalogo.agregar(juego)

    return catalogo