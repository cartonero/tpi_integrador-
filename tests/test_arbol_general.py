# pylint: disable=missing-function-docstring,missing-class-docstring
"""Pruebas del árbol general y de la jerarquía de categorías."""
import unittest

from estructuras.arbol_general import ArbolGeneral
from modelos.catalogo import Catalogo
from modelos.juego import Juego
from servicios.categorias import GRUPOS, construir_arbol_categorias, generos_validos


def _arbol_chico():
    arbol = ArbolGeneral()
    raiz = arbol.insertar_raiz("R")
    a = arbol.agregar_hijo(raiz, "A")
    b = arbol.agregar_hijo(raiz, "B")
    arbol.agregar_hijo(a, "A1")
    arbol.agregar_hijo(a, "A2")
    arbol.agregar_hijo(b, "B1")
    return arbol


class TestArbolGeneral(unittest.TestCase):
    def test_recorridos(self):
        arbol = _arbol_chico()
        self.assertEqual(arbol.amplitud(), ["R", "A", "B", "A1", "A2", "B1"])
        self.assertEqual(arbol.profundidad_preorder(), ["R", "A", "A1", "A2", "B", "B1"])
        self.assertEqual(arbol.profundidad_postorder(), ["A1", "A2", "A", "B1", "B", "R"])

    def test_niveles_altura_y_cantidad(self):
        arbol = _arbol_chico()
        self.assertEqual(arbol.obtener_niveles(), [["R"], ["A", "B"], ["A1", "A2", "B1"]])
        self.assertEqual(arbol.altura(), 3)
        self.assertEqual(arbol.cantidad_nodos(), 6)

    def test_buscar(self):
        arbol = _arbol_chico()
        nodo = arbol.buscar("A2")
        assert nodo is not None
        self.assertEqual(nodo.dato, "A2")
        self.assertIsNone(arbol.buscar("X"))

    def test_arbol_vacio(self):
        arbol = ArbolGeneral()
        self.assertEqual(arbol.amplitud(), [])
        self.assertEqual(arbol.altura(), 0)


class TestCategorias(unittest.TestCase):
    def test_jerarquia_de_steam(self):
        arbol = construir_arbol_categorias(Catalogo())
        assert arbol.raiz is not None
        self.assertEqual(arbol.raiz.dato, "Juegoteca")
        self.assertEqual(arbol.listar_hijos(arbol.raiz), list(GRUPOS))
        self.assertEqual(arbol.cantidad_nodos(), 1 + len(GRUPOS) + len(generos_validos()))

    def test_genero_desconocido_va_a_otros(self):
        cat = Catalogo()
        cat.agregar(Juego("1", "X", ["GeneroRaro"]))
        arbol = construir_arbol_categorias(cat)
        self.assertIn("Otros", arbol.listar_hijos(arbol.raiz))
        self.assertIsNotNone(arbol.buscar("GeneroRaro"))


if __name__ == "__main__":
    unittest.main()
