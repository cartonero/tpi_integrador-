"""Pruebas del Grafo y de la construcción del grafo de juegos relacionados."""
import unittest

from estructuras.grafo import Grafo
from modelos.catalogo import Catalogo
from modelos.juego import Juego
from servicios.relaciones import (construir_grafo_relacionados, incorporar_juego,
                                  juegos_relacionados, pesos_de_generos, similitud)


class TestGrafo(unittest.TestCase):
    def setUp(self):
        self.g = Grafo()
        for v in "ABCD":
            self.g.agregar_vertice(v)
        self.g.agregar_arista("A", "B", 0.5)
        self.g.agregar_arista("A", "C", 0.2)

    def test_arista_es_no_dirigida(self):
        self.assertTrue(self.g.hay_arista("A", "B"))
        self.assertTrue(self.g.hay_arista("B", "A"))
        self.assertEqual(self.g.peso("B", "A"), 0.5)

    def test_conteos_y_grado(self):
        self.assertEqual(self.g.cantidad_vertices(), 4)
        self.assertEqual(self.g.cantidad_aristas(), 2)
        self.assertEqual(self.g.grado("A"), 2)
        self.assertEqual(self.g.grado("D"), 0)

    def test_vecinos_ordenados_por_peso(self):
        self.assertEqual(self.g.vecinos("A"), [("C", 0.2), ("B", 0.5)])
        self.assertEqual(self.g.vecinos("ZZZ"), [])

    def test_vertice_repetido_no_borra_aristas(self):
        self.g.agregar_vertice("A")
        self.assertEqual(self.g.grado("A"), 2)

    def test_errores(self):
        with self.assertRaises(ValueError):
            self.g.agregar_arista("A", "X", 1)      # vértice inexistente
        with self.assertRaises(ValueError):
            self.g.agregar_arista("A", "A", 1)      # consigo mismo
        with self.assertRaises(ValueError):
            self.g.agregar_arista("A", "D", -1)     # peso negativo


def _catalogo():
    c = Catalogo()
    datos = [
        ("1", "Alfa", ["Action", "Indie"]),
        ("2", "Beta", ["Action", "Indie"]),
        ("3", "Gamma", ["Action", "Indie", "Racing"]),
        ("4", "Delta", ["RPG", "Strategy"]),
        ("5", "Epsilon", ["RPG", "Strategy", "Indie"]),
        ("6", "Zeta", ["Racing"]),
    ]
    for appid, nombre, generos in datos:
        c.agregar(Juego(appid, nombre, generos))
    return c


class TestRelaciones(unittest.TestCase):
    def test_similitud(self):
        pesos = {"A": 1.0, "B": 1.0, "C": 2.0}
        self.assertEqual(similitud({"A"}, {"A"}, pesos), 1.0)
        self.assertEqual(similitud({"A"}, {"B"}, pesos), 0.0)
        self.assertAlmostEqual(similitud({"A", "C"}, {"A"}, pesos), 1 / 3)
        self.assertEqual(similitud(set(), set(), pesos), 0.0)

    def test_genero_raro_pesa_mas_que_el_comun(self):
        pesos = pesos_de_generos(_catalogo().listar())
        self.assertGreater(pesos["Strategy"], pesos["Indie"])

    def test_grafo_tiene_un_vertice_por_juego_y_ninguno_aislado(self):
        c = _catalogo()
        g = construir_grafo_relacionados(c, vecinos_por_juego=2)
        self.assertEqual(g.cantidad_vertices(), c.cantidad())
        for juego in c.listar():
            self.assertGreaterEqual(g.grado(juego), 1, juego.get_nombre())

    def test_el_mas_parecido_es_el_de_mismos_generos(self):
        c = _catalogo()
        g = construir_grafo_relacionados(c, vecinos_por_juego=2)
        alfa = c.buscar("Alfa")
        mejor, similitud_mejor = juegos_relacionados(g, alfa)[0]
        self.assertEqual(mejor.get_nombre(), "Beta")
        self.assertEqual(similitud_mejor, 1.0)

    def test_pesos_en_rango(self):
        g = construir_grafo_relacionados(_catalogo(), vecinos_por_juego=3)
        for v in g.vertices():
            for _, peso in g.vecinos(v):
                self.assertTrue(0 <= peso <= 1)

    def test_incorporar_juego_nuevo(self):
        c = _catalogo()
        g = construir_grafo_relacionados(c, vecinos_por_juego=2)
        nuevo = Juego("local-7", "Nuevo", ["RPG", "Strategy"])
        c.agregar(nuevo)
        creadas = incorporar_juego(g, c, nuevo, vecinos_por_juego=2)
        self.assertEqual(creadas, 2)
        self.assertTrue(g.hay_vertice(nuevo))
        self.assertEqual(juegos_relacionados(g, nuevo)[0][0].get_nombre(), "Delta")


if __name__ == "__main__":
    unittest.main()
