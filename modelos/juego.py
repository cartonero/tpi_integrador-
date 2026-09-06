class Juego:
    """Representa un videojuego del catálogo de Juegoteca."""

    def __init__(self, appid, nombre, generos, tiempo_estimado_min, positivos, negativos):
        self._appid = appid
        self._nombre = nombre
        self._generos = generos if generos else []
        self._tiempo_estimado_min = tiempo_estimado_min or 0
        self._positivos = positivos or 0
        self._negativos = negativos or 0

    def get_appid(self):
        return self._appid

    def get_nombre(self):
        return self._nombre

    def get_generos(self):
        return self._generos

    def get_categoria_principal(self):
        return self._generos[0] if self._generos else "Sin categoría"

    def get_tiempo_estimado_horas(self):
        return round(self._tiempo_estimado_min / 60, 1)

    def get_positivos(self):
        return self._positivos

    def get_negativos(self):
        return self._negativos

    def get_rating_porcentaje(self):
        total = self._positivos + self._negativos
        if total == 0:
            return 0.0
        return round((self._positivos / total) * 100, 1)

    def __repr__(self):
        return (
            f"{self._nombre} ({self.get_categoria_principal()}) "
            f"⭐ {self.get_rating_porcentaje()}% ({self._positivos}👍/{self._negativos}👎) "
            f"· {self.get_tiempo_estimado_horas()} hs"
        )