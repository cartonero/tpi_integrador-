# pylint: disable=missing-function-docstring,missing-class-docstring
"""Pruebas de Juego y Catalogo (modelos/)."""
import unittest

from modelos.catalogo import Catalogo
from modelos.juego import Juego


class TestJuego(unittest.TestCase):
    def test_getters(self):
        j = Juego("1", "Crab Game", ["Action", "Indie"], 90)
        self.assertEqual(j.get_appid(), "1")
        self.assertEqual(j.get_nombre(), "Crab Game")
        self.assertEqual(j.get_generos(), ["Action", "Indie"])
        self.assertEqual(j.get_tiempo_min(), 90)

    def test_categoria_principal_es_el_primer_genero(self):
        self.assertEqual(Juego("1", "A", ["RPG", "Indie"]).get_categoria_principal(), "RPG")

    def test_sin_generos_no_rompe(self):
        j = Juego("1", "A", None)
        self.assertEqual(j.get_generos(), [])

    def test_tiempo_cero_o_none_es_sin_datos(self):
        self.assertFalse(Juego("1", "A", ["RPG"]).tiene_tiempo())
        self.assertFalse(Juego("1", "A", ["RPG"], None).tiene_tiempo())
        self.assertTrue(Juego("1", "A", ["RPG"], 5).tiene_tiempo())


class TestCatalogo(unittest.TestCase):
    def setUp(self):
        self.cat = Catalogo()
        self.cat.agregar(Juego("1", "Crab Game", ["Action"]))
        self.cat.agregar(Juego("2", "Hollow Knight", ["Action", "Indie"]))
        self.cat.agregar(Juego("3", "Stardew Valley", ["Simulation"]))

    def test_agregar_devuelve_true_y_cuenta(self):
        self.assertEqual(self.cat.cantidad(), 3)
        self.assertTrue(self.cat.agregar(Juego("4", "Otro", ["RPG"])))
        self.assertEqual(self.cat.cantidad(), 4)

    def test_appid_repetido_no_se_agrega(self):
        self.assertFalse(self.cat.agregar(Juego("1", "Copia", ["RPG"])))
        self.assertEqual(self.cat.cantidad(), 3)

    def test_buscar_ignora_mayusculas(self):
        encontrado = self.cat.buscar("CRAB game")
        assert encontrado is not None
        self.assertEqual(encontrado.get_appid(), "1")
        self.assertIsNone(self.cat.buscar("no existe"))

    def test_buscar_por_appid(self):
        encontrado = self.cat.buscar_por_appid("2")
        assert encontrado is not None
        self.assertEqual(encontrado.get_nombre(), "Hollow Knight")
        self.assertIsNone(self.cat.buscar_por_appid("999"))

    def test_filtrar_por_categoria(self):
        nombres = [j.get_nombre() for j in self.cat.filtrar_por_categoria("Action")]
        self.assertEqual(nombres, ["Crab Game", "Hollow Knight"])
        self.assertEqual(self.cat.filtrar_por_categoria("Racing"), [])

    def test_listar_devuelve_copia(self):
        self.cat.listar().clear()
        self.assertEqual(self.cat.cantidad(), 3)


if __name__ == "__main__":
    unittest.main()
