"""
algoritmos/preparar_datos.py — Genera la muestra de datos que usa Juegoteca.

El dataset completo de Steam (lux/games.json, ~900 MB, más de 100.000 juegos)
es demasiado grande para subirlo a GitHub y para usarlo en la demo. Este
script lo reduce: filtra los juegos válidos, elige 2000 al azar y los guarda
en datos/games.json, que es el archivo que carga la aplicación.

Se corre UNA sola vez, desde la raíz del proyecto:
    py algoritmos/preparar_datos.py

Cosas a tener en cuenta:
  - Necesita lux/games.json, que NO está en el repositorio (lo ignora el
    .gitignore por su tamaño). Se baja de Kaggle (Steam Games Dataset).
  - Carga el JSON completo en memoria con json.load: puede necesitar varios
    GB de RAM y fallar con MemoryError en computadoras con poca memoria libre.
  - La muestra es ALEATORIA y no usa semilla: cada ejecución genera 2000
    juegos distintos y PISA datos/games.json. Los números de los análisis
    (por ejemplo, altura del BST = 27 y del AVL = 13) dependen de la muestra
    actual, así que no conviene volver a correrlo sin necesidad.
"""
import json
import random

RUTA_JSON_ORIGINAL = "lux/games.json"
RUTA_SALIDA = "datos/games.json"
CANTIDAD_JUEGOS = 2000  # cuántos juegos queremos en nuestra muestra


def cargar_dataset_completo(ruta):
    """Lee el JSON original de Steam completo.

    Es un diccionario: la clave es el appid del juego y el valor es otro
    diccionario con todos sus datos (name, genres, positive, negative, ...).
    """
    print("Cargando dataset original (puede tardar un poco, es grande)...")
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def filtrar_y_convertir(dataset_completo, cantidad):
    """Se queda con los juegos válidos y devuelve una muestra al azar.

    La salida es una LISTA de diccionarios (más simple que el original) con
    solo los campos que nos interesan.
    """
    juegos_validos = []

    # .items() recorre pares (clave, valor): acá (appid, datos del juego).
    for appid, datos in dataset_completo.items():
        # .get(clave, valor_por_defecto) evita errores si falta un campo.
        nombre = datos.get("name", "").strip()
        positivos = datos.get("positive", 0)
        negativos = datos.get("negative", 0)
        generos = datos.get("genres", [])
        tiempo = datos.get("average_playtime_forever", 0)

        # Descartamos juegos sin nombre, sin reseñas o sin género
        if not nombre or (positivos + negativos) == 0 or not generos:
            continue

        # Guardamos los campos que el proyecto usa o podría usar más adelante.
        # Hoy la clase Juego solo toma appid, name y genres; el resto
        # (tiempo de juego y votos) queda en el JSON por si se necesita.
        juegos_validos.append({
            "appid": appid,
            "name": nombre,
            "genres": generos,
            "average_playtime_forever": tiempo,
            "positive": positivos,
            "negative": negativos,
        })

    print(f"Juegos válidos encontrados: {len(juegos_validos)}")

    # random.sample elige elementos al azar SIN repetir. El min() evita pedir
    # más juegos de los que hay disponibles.
    muestra = random.sample(juegos_validos, min(cantidad, len(juegos_validos)))
    return muestra


def guardar_json_reducido(juegos, ruta_salida):
    """Escribe la muestra en un JSON legible (indent=2) y con tildes (ensure_ascii=False)."""
    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        json.dump(juegos, archivo, ensure_ascii=False, indent=2)
    print(f"Listo: {len(juegos)} juegos guardados en {ruta_salida}")


# Este bloque solo corre al ejecutar el archivo directamente, no al importarlo.
if __name__ == "__main__":
    dataset = cargar_dataset_completo(RUTA_JSON_ORIGINAL)
    juegos_filtrados = filtrar_y_convertir(dataset, CANTIDAD_JUEGOS)
    guardar_json_reducido(juegos_filtrados, RUTA_SALIDA)