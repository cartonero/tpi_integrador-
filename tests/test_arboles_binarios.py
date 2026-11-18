
"""Pruebas del BST y del AVL (estructuras/)."""
import random
import unittest

from estructuras.arbol_binario import ArbolBST
from estructuras.avl import AVL

def CLAVE(texto):
    """Clave de ordenamiento: el texto en minúsculas."""
    return texto.lower()


def _es_avl_valido(nodo):
    """Devuelve la altura del subárbol, o lanza AssertionError si hay desbalance."""
    if nodo is None:
        return 0
    hi = _es_avl_valido(nodo.izquierdo)
    hd = _es_avl_valido(nodo.derecho)
    assert abs(hi - hd) <= 1, "factor de balance fuera de -1..1"
    return 1 + max(hi, hd)


class TestBST(unittest.TestCase):
    def test_inorder_queda_ordenado(self):
        arbol = ArbolBST()
        for n in ["Matrix", "Inception", "Titanic", "Blade Runner", "Arrival"]:
            arbol.insertar(n, CLAVE)
        self.assertEqual(arbol.inorder(),
                            ["Arrival", "Blade Runner", "Inception", "Matrix", "Titanic"])

    def test_preorder_y_postorder(self):
        arbol = ArbolBST()
        for n in ["b", "a", "c"]:
            arbol.insertar(n, CLAVE)
        self.assertEqual(arbol.preorder(), ["b", "a", "c"])
        self.assertEqual(arbol.postorder(), ["a", "c", "b"])

    def test_buscar(self):
        arbol = ArbolBST()
        for n in ["b", "a", "c"]:
            arbol.insertar(n, CLAVE)
        self.assertEqual(arbol.buscar("c", CLAVE), "c")
        self.assertIsNone(arbol.buscar("zzz", CLAVE))

    def test_datos_ordenados_degeneran_en_cadena(self):
        arbol = ArbolBST()
        for n in "abcdefghij":
            arbol.insertar(n, CLAVE)
        self.assertEqual(arbol.altura(), 10)

    def test_arbol_vacio(self):
        arbol = ArbolBST()
        self.assertEqual(arbol.altura(), 0)
        self.assertEqual(arbol.inorder(), [])
        self.assertIsNone(arbol.buscar("a", CLAVE))


class TestAVL(unittest.TestCase):
    def test_datos_ordenados_quedan_balanceados(self):
        avl = AVL()
        for n in "abcdefghij":
            avl.insertar(n, CLAVE)
        self.assertEqual(avl.altura(), 4)
        _es_avl_valido(avl.raiz)

    def test_cuatro_casos_de_rotacion(self):
        # LL, RR, LR, RL: en los cuatro casos 3 datos quedan en altura 2.
        for orden in (["c", "b", "a"], ["a", "b", "c"], ["c", "a", "b"], ["a", "c", "b"]):
            avl = AVL()
            for n in orden:
                avl.insertar(n, CLAVE)
            self.assertEqual(avl.altura(), 2, orden)
            self.assertEqual(avl.preorder(), ["b", "a", "c"], orden)

    def test_mil_datos_ordenados_y_aleatorios(self):
        datos = [f"juego{i:05d}" for i in range(1000)]
        for orden in (datos, random.sample(datos, len(datos))):
            avl = AVL()
            for d in orden:
                avl.insertar(d, CLAVE)
            self.assertEqual(len(avl), 1000)
            self.assertEqual(avl.inorder(), datos)
            self.assertLessEqual(avl.altura(), 14)
            _es_avl_valido(avl.raiz)

    def test_duplicados_se_ignoran(self):
        avl = AVL()
        avl.insertar("a", CLAVE)
        avl.insertar("A", CLAVE)
        self.assertEqual(len(avl), 1)

    def test_buscar(self):
        avl = AVL()
        for n in "abc":
            avl.insertar(n, CLAVE)
        self.assertEqual(avl.buscar("b", CLAVE), "b")
        self.assertIsNone(avl.buscar("z", CLAVE))


if __name__ == "__main__":
    unittest.main()
