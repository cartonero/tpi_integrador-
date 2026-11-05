"""
modelos/catalogo.py — Clase Catalogo (colección de juegos).

El Catalogo guarda TODOS los juegos de Juegoteca en una lista de Python y
ofrece las operaciones básicas sobre ella: agregar, buscar, listar y filtrar.

Es la "fuente de datos" del programa:
  - servicios/cargador_datos.py lo llena leyendo el JSON.
  - main.py recorre sus juegos para armar los árboles (BST y AVL).
  - El menú usa listar() y filtrar_por_categoria() directamente.

Además de la lista guarda un diccionario auxiliar (id de Steam -> juego) que
permite agregar y buscar por id en O(1), sin recorrer la lista.

La búsqueda por NOMBRE (buscar) y el filtrado son SECUENCIALES (recorren la
lista de a un elemento): cuestan O(n). Justamente por eso después se
incorporaron los árboles, que buscan por nombre en O(log n).
"""
from modelos.juego import Juego


class Catalogo:
    """Contiene y gestiona la colección de juegos de Juegoteca."""

    def __init__(self):
        # Lista privada con todos los objetos Juego. Se accede solo a través
        # de los métodos de esta clase (encapsulamiento).
        self._juegos = []

        # Índice auxiliar: diccionario "appid -> Juego". Sirve para saber si
        # un id ya existe (y para obtener el juego) en O(1). Sin él, cada
        # alta tendría que recorrer toda la lista y cargar muchos juegos
        # seguidos sería cada vez más lento.
        self._por_appid = {}

    def agregar(self, juego: Juego):
        """Agrega un juego al catálogo. Devuelve True si lo agregó.

        Si ya existe un juego con el mismo appid no lo agrega (evita
        duplicados) y devuelve False. Costo: O(1), porque el chequeo se hace
        en el diccionario de ids.
        """
        appid = juego.get_appid()
        if appid in self._por_appid:
            return False
        self._juegos.append(juego)
        self._por_appid[appid] = juego
        return True

    def buscar(self, nombre):
        """Búsqueda SECUENCIAL por nombre exacto. Devuelve el Juego o None.

        Ignora mayúsculas y espacios sobrantes. Es la búsqueda original del
        TP1, O(n). El menú ya no la usa: ahora "Buscar juego" consulta el
        AVL. Se conserva como la versión de referencia contra la que se
        compara el árbol.
        """
        nombre = nombre.strip().lower()
        for juego in self._juegos:
            if juego.get_nombre().strip().lower() == nombre:
                return juego
        return None

    def buscar_por_appid(self, appid):
        """Busca un juego por id de Steam. Devuelve el Juego o None. O(1)."""
        # .get() devuelve None si el id no está en el diccionario.
        return self._por_appid.get(appid)

    def listar(self):
        """Devuelve una COPIA de la lista de juegos.

        Se devuelve una copia (list(...)) y no la lista interna para que
        quien la reciba no pueda modificar el catálogo sin querer.
        """
        return list(self._juegos)

    def filtrar_por_categoria(self, categoria):
        """Devuelve los juegos que tienen la categoría (género) indicada.

        Un juego puede tener varios géneros: alcanza con que UNO coincida.
        La comparación ignora mayúsculas. Recorre todo el catálogo: O(n).
        """
        categoria = categoria.strip().lower()
        return [
            juego for juego in self._juegos
            if categoria in [g.lower() for g in juego.get_generos()]
        ]

    def cantidad(self):
        """Devuelve cuántos juegos hay en el catálogo."""
        return len(self._juegos)