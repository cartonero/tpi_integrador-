class Juego:
    """Representa un videojuego del catálogo de Juegoteca."""

    def __init__(self, appid, nombre, generos):
        self._appid = appid
        self._nombre = nombre
        self._generos = generos if generos else []


    def get_appid(self):
        return self._appid

    def get_nombre(self):
        return self._nombre

    def get_generos(self):
        return self._generos

    def get_categoria_principal(self):
        return self._generos[0] if self._generos else "Sin categoría"



    def __repr__(self):
        return (
            f"{self._nombre} ({self.get_categoria_principal()}) "
        )