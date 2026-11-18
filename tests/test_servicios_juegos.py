# pylint: disable=missing-function-docstring,missing-class-docstring
"""Pruebas de servicios/juegos.py: duración, comparación y alta de juegos."""
import unittest

from estructuras.arbol_binario import ArbolBST
from estructuras.avl import AVL
from modelos.catalogo import Catalogo
from modelos.juego import Juego
from servicios.juegos import (MAX_HORAS, agregar_juego, clave_nombre,
                              comparar_tiempos, formatear_duracion,
                              horas_a_minutos, parsear_generos)

VALIDOS = ["Action", "Indie", "RPG"]


class TestFormatoYConversion(unittest.TestCase):
    def test_formatear_duracion(self):
        self.assertEqual(formatear_duracion(0), "sin datos")
        self.assertEqual(formatear_duracion(45), "45 min")
        self.assertEqual(formatear_duracion(180), "3 h")
        self.assertEqual(formatear_duracion(232), "3 h 52 min")

    def test_horas_a_minutos(self):
        self.assertEqual(horas_a_minutos(""), 0)
        self.assertEqual(horas_a_minutos("2"), 120)
        self.assertEqual(horas_a_minutos("1.5"), 90)
        self.assertEqual(horas_a_minutos("1,5"), 90)

    def test_horas_invalidas(self):
        for texto in ("abc", "-3", str(MAX_HORAS + 1)):
            with self.assertRaises(ValueError, msg=texto):
                horas_a_minutos(texto)

    def test_parsear_generos(self):
        elegidos, invalidos = parsear_generos("action, INDIE, action, xyz,,", VALIDOS)
        self.assertEqual(elegidos, ["Action", "Indie"])
        self.assertEqual(invalidos, ["xyz"])


class TestComparar(unittest.TestCase):
    def test_ordena_de_menor_a_mayor_y_separa_sin_datos(self):
        a = Juego("1", "A", ["RPG"], 300)
        b = Juego("2", "B", ["RPG"], 60)
        c = Juego("3", "C", ["RPG"], 0)
        con_datos, sin_datos = comparar_tiempos([a, b, c])
        self.assertEqual(con_datos, [b, a])
        self.assertEqual(sin_datos, [c])


class TestAgregarJuego(unittest.TestCase):
    def setUp(self):
        self.cat, self.bst, self.avl = Catalogo(), ArbolBST(), AVL()
        base = Juego("10", "Hollow Knight", ["Action"], 600)
        self.cat.agregar(base)
        self.bst.insertar(base, clave_nombre)
        self.avl.insertar(base, clave_nombre)

    def test_alta_exitosa_queda_en_las_tres_estructuras(self):
        j = agregar_juego("Mi Juego", ["RPG"], 120, self.cat, self.bst, self.avl)
        self.assertEqual(self.cat.cantidad(), 2)
        self.assertIs(self.avl.buscar("mi juego", clave_nombre), j)
        self.assertIs(self.bst.buscar("mi juego", clave_nombre), j)
        self.assertIs(self.cat.buscar("Mi Juego"), j)

    def test_nombre_vacio_o_sin_generos_no_modifica_nada(self):
        with self.assertRaises(ValueError):
            agregar_juego("   ", ["RPG"], 0, self.cat, self.bst, self.avl)
        with self.assertRaises(ValueError):
            agregar_juego("Otro", [], 0, self.cat, self.bst, self.avl)
        self.assertEqual(self.cat.cantidad(), 1)
        self.assertEqual(len(self.avl), 1)

    def test_nombre_repetido_ignora_mayusculas(self):
        with self.assertRaises(ValueError):
            agregar_juego("HOLLOW KNIGHT", ["RPG"], 0, self.cat, self.bst, self.avl)
        self.assertEqual(self.cat.cantidad(), 1)


if __name__ == "__main__":
    unittest.main()
