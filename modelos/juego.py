"""
modelos/juego.py — Clase Juego (modelo del dominio).

Un objeto Juego representa UN videojuego del catálogo de Juegoteca. Es la
"ficha" de cada juego: el catálogo, los árboles y el menú trabajan con
objetos de esta clase.

Cada Juego se arma a partir de un registro del dataset de Steam
(datos/games.json). De todos los campos que trae Steam, la aplicación usa
solo tres: appid, nombre y géneros.
"""


class Juego:
    """Representa un videojuego del catálogo de Juegoteca.

    ENCAPSULAMIENTO: los atributos empiezan con guion bajo (_appid, _nombre,
    _generos) para indicar que son privados. Desde afuera de la clase no se
    acceden directamente, sino a través de los getters (get_nombre,
    get_appid, ...). Así, si cambia la forma de guardar un dato, el resto
    del programa no necesita modificarse.
    """

    def __init__(self, appid, nombre, generos):
        # Identificador único del juego en Steam. El catálogo lo usa para
        # no cargar dos veces el mismo juego.
        self._appid = appid

        # Nombre del juego. Es la CLAVE de ordenamiento de los árboles
        # (el BST y el AVL ordenan alfabéticamente por este campo).
        self._nombre = nombre

        # Lista de géneros de Steam, por ejemplo ["Action", "Indie"]. Un juego
        # puede tener varios. Si viene vacía o None guardamos una lista vacía
        # para que el resto del código nunca se encuentre con None.
        self._generos = generos if generos else []

    # ==================== GETTERS ====================
    # Son la única forma de leer los datos del juego desde otras clases.

    def get_appid(self):
        """Devuelve el id del juego en Steam."""
        return self._appid

    def get_nombre(self):
        """Devuelve el nombre del juego."""
        return self._nombre

    def get_generos(self):
        """Devuelve la lista completa de géneros del juego."""
        return self._generos

    def get_categoria_principal(self):
        """Devuelve la categoría principal: el PRIMER género de la lista.

        Es la categoría que se muestra al lado del nombre en pantalla.
        Si el juego no tiene géneros devuelve "Sin categoría".
        """
        return self._generos[0] if self._generos else "Sin categoría"

    # ==================== REPRESENTACIÓN EN TEXTO ====================

    def __repr__(self):
        """Texto que se muestra al hacer print(juego): 'Nombre (Categoría)'."""
        return (
            f"{self._nombre} ({self.get_categoria_principal()}) "
        )