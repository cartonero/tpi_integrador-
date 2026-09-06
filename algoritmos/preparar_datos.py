import json
import random

RUTA_JSON_ORIGINAL = "lux/games.json"
RUTA_SALIDA = "datos/games.json"
CANTIDAD_JUEGOS = 2000  # cuántos juegos queremos en nuestra muestra


def cargar_dataset_completo(ruta):
    print("Cargando dataset original (puede tardar un poco, es grande)...")
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def filtrar_y_convertir(dataset_completo, cantidad):
    juegos_validos = []

    for appid, datos in dataset_completo.items():
        nombre = datos.get("name", "").strip()
        positivos = datos.get("positive", 0)
        negativos = datos.get("negative", 0)
        generos = datos.get("genres", [])
        tiempo = datos.get("average_playtime_forever", 0)

        # Descartamos juegos sin nombre, sin reseñas o sin género
        if not nombre or (positivos + negativos) == 0 or not generos:
            continue

        juegos_validos.append({
            "appid": appid,
            "name": nombre,
            "genres": generos,
            "average_playtime_forever": tiempo,
            "positive": positivos,
            "negative": negativos,
        })

    print(f"Juegos válidos encontrados: {len(juegos_validos)}")

    muestra = random.sample(juegos_validos, min(cantidad, len(juegos_validos)))
    return muestra


def guardar_json_reducido(juegos, ruta_salida):
    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        json.dump(juegos, archivo, ensure_ascii=False, indent=2)
    print(f"Listo: {len(juegos)} juegos guardados en {ruta_salida}")


if __name__ == "__main__":
    dataset = cargar_dataset_completo(RUTA_JSON_ORIGINAL)
    juegos_filtrados = filtrar_y_convertir(dataset, CANTIDAD_JUEGOS)
    guardar_json_reducido(juegos_filtrados, RUTA_SALIDA)