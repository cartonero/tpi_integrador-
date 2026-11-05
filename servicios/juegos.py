"""
servicios/juegos.py — Operaciones sobre juegos (duración, comparación y alta).

Reúne la lógica de las funcionalidades que trabajan con el tiempo de juego,
separada de la interfaz: este módulo no imprime ni pide datos (eso lo hace
ui/terminal.py), solo recibe datos y devuelve resultados.

Funciones:
    - formatear_duracion: convierte minutos a texto legible.
    - comparar_tiempos: separa y ordena juegos según su tiempo de juego.
    - parsear_generos: valida los géneros escritos por el usuario.
    - horas_a_minutos: convierte las horas escritas por el usuario a minutos.
    - agregar_juego: da de alta un juego en el catálogo y en los dos árboles.

"Duración estimada" es el tiempo de juego PROMEDIO que registra Steam para
cada juego (en minutos). No es el tiempo que lleva completarlo, y muchos
juegos no tienen el dato (figuran con 0).
"""
import math

from modelos.juego import Juego

# Tope de duración aceptado al añadir un juego (evita errores de tipeo).
MAX_HORAS = 100_000


def formatear_duracion(minutos):
    """Convierte minutos a un texto legible: '45 min', '3 h' o '3 h 52 min'.

    Si no hay datos (0 minutos o menos) devuelve 'sin datos'.
    """
    if minutos <= 0:
        return "sin datos"

    # divmod(a, b) devuelve (cociente, resto): minutos // 60 y minutos % 60.
    horas, resto = divmod(minutos, 60)
    if horas == 0:
        return f"{resto} min"
    if resto == 0:
        return f"{horas} h"
    return f"{horas} h {resto} min"


def comparar_tiempos(juegos):
    """Prepara una lista de juegos para compararlos por tiempo de juego.

    Devuelve una tupla (con_datos, sin_datos):
      - con_datos: los juegos que tienen duración, ordenados de MENOR a MAYOR.
      - sin_datos: los juegos sin duración (no se pueden comparar).

    Si dos juegos tienen el mismo tiempo, conservan el orden en que llegaron.
    """
    # Se separan en dos listas según tengan o no tengan dato de duración.
    con_datos = [j for j in juegos if j.tiene_tiempo()]
    sin_datos = [j for j in juegos if not j.tiene_tiempo()]

    # sort() ordena la lista de menor a mayor usando como criterio los
    # minutos de cada juego (key). Es estable: respeta el orden en los empates.
    con_datos.sort(key=lambda j: j.get_tiempo_min())
    return con_datos, sin_datos


# ==================== AÑADIR UN JUEGO (F2) ====================

def clave_nombre(juego):
    """Clave de ordenamiento de los árboles: el nombre del juego en minúsculas.

    Es la misma regla que usa main.py al armar el BST y el AVL.
    """
    return juego.get_nombre().lower()


def parsear_generos(texto, generos_validos):
    """Convierte lo que escribió el usuario en una lista de géneros válidos.

    Recibe un texto como 'action, INDIE' y la lista de géneros permitidos.
    Devuelve una tupla (elegidos, invalidos):
      - elegidos: géneros reconocidos, con su nombre oficial ('Action'), sin
        repetir y en el orden en que se escribieron.
      - invalidos: textos que no coinciden con ningún género.
    """
    # Diccionario "en minúsculas -> nombre oficial": permite comparar sin
    # importar mayúsculas y devolver siempre el nombre bien escrito.
    por_minuscula = {genero.lower(): genero for genero in generos_validos}

    elegidos = []
    invalidos = []
    for parte in texto.split(","):
        parte = parte.strip()
        if parte == "":
            continue  # ignora comas de más
        oficial = por_minuscula.get(parte.lower())
        if oficial is None:
            if parte not in invalidos:
                invalidos.append(parte)
        elif oficial not in elegidos:
            elegidos.append(oficial)
    return elegidos, invalidos


def horas_a_minutos(texto):
    """Convierte un texto con horas ('12', '12.5' o '12,5') a minutos enteros.

    Un texto vacío significa "no sé la duración" y devuelve 0 (sin datos).
    Si el texto no es válido lanza ValueError con un mensaje para el usuario.
    """
    original = texto.strip()
    if original == "":
        return 0

    # En español es común escribir la coma decimal: '12,5' se lee como 12.5.
    try:
        horas = float(original.replace(",", "."))
    except ValueError:
        raise ValueError(f"'{original}' no es un número de horas válido.") from None

    # math.isfinite descarta 'nan' e 'inf', que float() también acepta.
    if not math.isfinite(horas) or horas < 0:
        raise ValueError("La duración tiene que ser un número de horas mayor o igual a 0.")
    if horas > MAX_HORAS:
        raise ValueError(f"La duración no puede superar {MAX_HORAS} horas.")

    minutos = round(horas * 60)
    # Si escribió una duración positiva pero muy chica, no la dejamos en 0
    # (0 significa "sin datos").
    if horas > 0 and minutos == 0:
        minutos = 1
    return minutos


def agregar_juego(nombre, generos, tiempo_min, catalogo, bst, avl):
    """Da de alta un juego nuevo en el catálogo, en el BST y en el AVL.

    Devuelve el Juego creado. Lanza ValueError (con un mensaje para el
    usuario) si el nombre está vacío, si ya existe un juego con ese nombre
    o si no se indicó ningún género. Si algo falla, no se modifica nada.

    Los juegos añadidos viven solo en memoria: al cerrar el programa se
    pierden (datos/games.json no se modifica).
    """
    nombre = nombre.strip()
    if nombre == "":
        raise ValueError("El nombre no puede estar vacío.")
    if not generos:
        raise ValueError("Hace falta al menos un género.")

    # Se busca en el AVL (O(log n)). El AVL ignora en silencio los nombres
    # repetidos: si no lo rechazáramos acá, el juego quedaría en la lista pero
    # sin poder buscarse.
    existente = avl.buscar(nombre.lower(), clave=clave_nombre)
    if existente is not None:
        raise ValueError(f"Ya existe un juego llamado '{existente.get_nombre()}'.")

    # El catálogo exige un id único por juego: se arma uno propio ("local-N").
    # Se chequea ANTES de tocar nada, para no dejar las estructuras a medias.
    appid = f"local-{catalogo.cantidad() + 1}"
    if catalogo.buscar_por_appid(appid) is not None:
        raise ValueError("No se pudo agregar el juego: el id generado ya existe.")
    juego = Juego(appid, nombre, list(generos), tiempo_min)

    # ORDEN pensado para que un error nunca deje todo a medias:
    # 1) El BST va primero porque es el único que puede fallar: si recibe
    #    muchos nombres en orden alfabético se vuelve una cadena y supera el
    #    límite de recursión de Python (RecursionError). Cuando eso pasa, el
    #    árbol no llega a modificarse, así que acá todavía no se tocó nada.
    try:
        bst.insertar(juego, clave=clave_nombre)
    except RecursionError:
        raise ValueError(
            "No se pudo agregar el juego: el BST llegó al límite de profundidad "
            "de Python (demasiados nombres cargados en orden alfabético). "
            "El AVL no tiene este problema."
        ) from None

    # 2) El AVL siempre queda balanceado, así que su altura es chica y no falla.
    avl.insertar(juego, clave=clave_nombre)

    # 3) El catálogo va al final: ya se comprobó que el id es único.
    catalogo.agregar(juego)
    return juego