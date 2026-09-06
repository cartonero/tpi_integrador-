from modelos.juego import Juego


class Catalogo:
    """Contiene y gestiona la colección de juegos de Juegoteca."""

    def __init__(self):
        self._juegos = []

    def agregar(self, juego: Juego):
        if self.buscar_por_appid(juego.get_appid()) is not None:
            return False
        self._juegos.append(juego)
        return True

    def buscar(self, nombre):
        nombre = nombre.strip().lower()
        for juego in self._juegos:
            if juego.get_nombre().strip().lower() == nombre:
                return juego
        return None

    def buscar_por_appid(self, appid):
        for juego in self._juegos:
            if juego.get_appid() == appid:
                return juego
        return None

    def listar(self):
        return list(self._juegos)

    def filtrar_por_categoria(self, categoria):
        categoria = categoria.strip().lower()
        return [
            juego for juego in self._juegos
            if categoria in [g.lower() for g in juego.get_generos()]
        ]

    def cantidad(self):
        return len(self._juegos)