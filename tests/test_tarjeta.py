"""Pruebas del rating de Juego y de la tarjeta que muestra la búsqueda."""
import unittest

from modelos.juego import Juego
from ui.terminal import _ancho_visual, _tarjeta_juego, _texto_rating


class TestRating(unittest.TestCase):
    def test_rating_sobre_10(self):
        j = Juego("1", "A", ["RPG"], 0, 94, 6)
        self.assertEqual(j.get_votos(), 100)
        self.assertEqual(j.get_rating(), 9.4)
        self.assertEqual(j.get_porcentaje_positivo(), 94)

    def test_sin_votos(self):
        j = Juego("1", "A", ["RPG"])
        self.assertFalse(j.tiene_rating())
        self.assertIsNone(j.get_rating())
        self.assertEqual(_texto_rating(j), "sin votos")

    def test_none_cuenta_como_cero(self):
        self.assertEqual(Juego("1", "A", ["RPG"], 0, None, None).get_votos(), 0)

    def test_pocos_votos_se_avisa(self):
        self.assertIn("pocos votos", _texto_rating(Juego("1", "A", ["RPG"], 0, 1, 0)))
        self.assertNotIn("pocos votos", _texto_rating(Juego("1", "A", ["RPG"], 0, 50, 5)))

    def test_un_solo_voto_va_en_singular(self):
        self.assertIn("1 voto", _texto_rating(Juego("1", "A", ["RPG"], 0, 1, 0)))
        self.assertNotIn("1 votos", _texto_rating(Juego("1", "A", ["RPG"], 0, 1, 0)))


class TestTarjeta(unittest.TestCase):
    def _juego(self, nombre="Hollow Knight"):
        return Juego("1", nombre, ["Action", "Indie"], 1620, 900, 100)

    def test_contiene_los_datos_del_boceto(self):
        otro = Juego("2", "Ori", ["Action"], 0, 88, 12)
        texto = "\n".join(_tarjeta_juego(self._juego(), [(otro, 0.75)]))
        for esperado in ("HOLLOW KNIGHT", "Categoría: Action", "27 h",
                         "9.0 / 10", "quizás te interesen", "Ori", "75% parecido"):
            self.assertIn(esperado, texto)

    def test_sin_relacionados(self):
        texto = "\n".join(_tarjeta_juego(self._juego(), []))
        self.assertIn("No hay juegos relacionados", texto)

    def test_todas_las_filas_tienen_el_mismo_ancho(self):
        # Incluye un nombre con caracteres de 2 columnas y uno muy largo.
        for nombre in ("Hollow Knight", "大逃亡专家 Escape Expert", "X" * 200):
            filas = _tarjeta_juego(self._juego(nombre), [(self._juego("Ori"), 0.5)])
            self.assertEqual(len({_ancho_visual(f) for f in filas}), 1, nombre[:10])


if __name__ == "__main__":
    unittest.main()
