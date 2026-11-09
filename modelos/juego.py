"""
modelos/juego.py — Clase Juego (modelo del dominio).

Un objeto Juego representa UN videojuego del catálogo de Juegoteca. Es la
"ficha" de cada juego: el catálogo, los árboles y el menú trabajan con
objetos de esta clase.

Cada Juego se arma a partir de un registro del dataset de Steam
(datos/games.json). De todos los campos que trae Steam, la aplicación usa
cuatro: appid, nombre, géneros y tiempo de juego.
"""


class Juego:
    """Representa un videojuego del catálogo de Juegoteca.

    ENCAPSULAMIENTO: los atributos empiezan con guion bajo (_appid, _nombre,
    _generos, _tiempo_min) para indicar que son privados. Desde afuera de la
    clase no se acceden directamente, sino a través de los getters
    (get_nombre, get_appid, ...). Así, si cambia la forma de guardar un dato,
    el resto del programa no necesita modificarse.
    """

    def __init__(self, appid, nombre, generos, tiempo_min=0, positivos=0, negativos=0):
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

        # Tiempo de juego PROMEDIO de los jugadores en Steam, en MINUTOS
        # (campo average_playtime_forever del dataset). Es la "duración
        # estimada" que muestra la app. El valor 0 significa "sin datos": en
        # la muestra de 2000 juegos, solo 555 tienen un tiempo mayor a 0.
        # El "or 0" convierte un None en 0.
        self._tiempo_min = tiempo_min or 0

        # Votos de los jugadores en Steam: cuántos recomendaron el juego
        # (positivos) y cuántos no (negativos). Sirven para calcular el rating.
        # El "or 0" convierte un None en 0.
        self._positivos = positivos or 0
        self._negativos = negativos or 0

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

    def get_tiempo_min(self):
        """Devuelve el tiempo de juego promedio, en minutos (0 = sin datos)."""
        return self._tiempo_min

    def tiene_tiempo(self):
        """Devuelve True si el juego tiene dato de duración (más de 0 minutos)."""
        return self._tiempo_min > 0

    def get_positivos(self):
        """Devuelve la cantidad de votos positivos en Steam."""
        return self._positivos

    def get_negativos(self):
        """Devuelve la cantidad de votos negativos en Steam."""
        return self._negativos

    def get_votos(self):
        """Devuelve el total de votos (positivos + negativos)."""
        return self._positivos + self._negativos

    def tiene_rating(self):
        """Devuelve True si el juego tiene al menos un voto."""
        return self.get_votos() > 0

    def get_rating(self):
        """Devuelve el rating de 0 a 10: la proporción de votos positivos x 10.

        Por ejemplo, 94 positivos y 6 negativos dan 9.4. Si no hay votos
        devuelve None (no se puede calcular).
        """
        votos = self.get_votos()
        if votos == 0:
            return None
        return round(10 * self._positivos / votos, 1)

    def get_porcentaje_positivo(self):
        """Devuelve el porcentaje de votos positivos (0 a 100), o None si no hay votos."""
        votos = self.get_votos()
        if votos == 0:
            return None
        return round(100 * self._positivos / votos)

    # ==================== REPRESENTACIÓN EN TEXTO ====================

    def __repr__(self):
        """Texto que se muestra al hacer print(juego): 'Nombre (Categoría)'."""
        return (
            f"{self._nombre} ({self.get_categoria_principal()}) "
        )