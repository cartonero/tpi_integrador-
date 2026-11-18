"""Pruebas de BFS y DFS (TP8) sobre grafos chicos armados a mano.

Se ejecutan con:  py -m unittest discover tests
"""

import unittest

from estructuras.grafo import Grafo
from algoritmos.bfs import bfs, bfs_saltos_entre
from algoritmos.dfs import dfs, componentes_conexas


def armar_grafo():
    """Arma este grafo (los números son los pesos):

        A --0.1-- B --0.2-- D
        |                   |
        0.3                 0.1
        |                   |
        C                   E          F --0.5-- G   (grupo aparte)

    A tiene dos vecinos: B (más parecido) y C.
    """
    g = Grafo()
    for v in "ABCDEFG":
        g.agregar_vertice(v)
    g.agregar_arista("A", "B", 0.1)
    g.agregar_arista("A", "C", 0.3)
    g.agregar_arista("B", "D", 0.2)
    g.agregar_arista("D", "E", 0.1)
    g.agregar_arista("F", "G", 0.5)
    return g


class TestBFS(unittest.TestCase):
    def setUp(self):
        self.g = armar_grafo()

    def test_visita_por_capas(self):
        self.assertEqual(bfs(self.g, "A"),
                         [("A", 0), ("B", 1), ("C", 1), ("D", 2), ("E", 3)])

    def test_respeta_el_limite_de_saltos(self):
        self.assertEqual(bfs(self.g, "A", max_saltos=1),
                         [("A", 0), ("B", 1), ("C", 1)])

    def test_cero_saltos_devuelve_solo_el_inicio(self):
        self.assertEqual(bfs(self.g, "A", max_saltos=0), [("A", 0)])

    def test_no_sale_de_su_grupo(self):
        visitados = [v for v, _ in bfs(self.g, "A")]
        self.assertNotIn("F", visitados)

    def test_vertice_inexistente(self):
        with self.assertRaises(ValueError):
            bfs(self.g, "Z")

    def test_saltos_entre_dos_vertices(self):
        self.assertEqual(bfs_saltos_entre(self.g, "A", "E"), 3)
        self.assertEqual(bfs_saltos_entre(self.g, "E", "A"), 3)  # no dirigido
        self.assertEqual(bfs_saltos_entre(self.g, "A", "A"), 0)

    def test_saltos_sin_camino(self):
        self.assertIsNone(bfs_saltos_entre(self.g, "A", "F"))

    def test_saltos_con_vertice_inexistente(self):
        with self.assertRaises(ValueError):
            bfs_saltos_entre(self.g, "A", "Z")

    def test_camino_corto_gana_sobre_el_de_menor_peso(self):
        # Un atajo con peso alto sigue siendo 1 salto: BFS cuenta aristas, no pesos.
        self.g.agregar_arista("A", "E", 0.9)
        self.assertEqual(bfs_saltos_entre(self.g, "A", "E"), 1)


class TestDFS(unittest.TestCase):
    def setUp(self):
        self.g = armar_grafo()

    def test_orden_en_profundidad(self):
        # Desde A va primero por B (el más parecido) y se mete hasta el fondo.
        self.assertEqual(dfs(self.g, "A"), ["A", "B", "D", "E", "C"])

    def test_visita_todo_el_grupo_sin_repetir(self):
        orden = dfs(self.g, "A")
        self.assertEqual(sorted(orden), ["A", "B", "C", "D", "E"])
        self.assertEqual(len(orden), len(set(orden)))

    def test_grafo_con_ciclo_no_se_cuelga(self):
        self.g.agregar_arista("C", "E", 0.4)  # cierra un ciclo A-B-D-E-C-A
        self.assertEqual(sorted(dfs(self.g, "A")), ["A", "B", "C", "D", "E"])

    def test_vertice_aislado(self):
        self.g.agregar_vertice("H")
        self.assertEqual(dfs(self.g, "H"), ["H"])

    def test_vertice_inexistente(self):
        with self.assertRaises(ValueError):
            dfs(self.g, "Z")

    def test_bfs_y_dfs_alcanzan_los_mismos_vertices(self):
        self.assertEqual(sorted(dfs(self.g, "A")),
                         sorted(v for v, _ in bfs(self.g, "A")))


class TestComponentes(unittest.TestCase):
    def test_separa_los_grupos(self):
        componentes = componentes_conexas(armar_grafo())
        self.assertEqual([len(c) for c in componentes], [5, 2])
        self.assertEqual(sorted(componentes[1]), ["F", "G"])

    def test_vertice_aislado_es_su_propio_grupo(self):
        g = armar_grafo()
        g.agregar_vertice("H")
        self.assertEqual(len(componentes_conexas(g)), 3)

    def test_grafo_vacio(self):
        self.assertEqual(componentes_conexas(Grafo()), [])


if __name__ == "__main__":
    unittest.main()
