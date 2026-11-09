"""
grafo.py — Grafo no dirigido y pesado (TP7), con lista de adyacencia.

Un GRAFO es un conjunto de VÉRTICES (nodos) unidos por ARISTAS. En Juegoteca:
    - cada vértice es un juego;
    - cada arista une dos juegos "relacionados" (ver servicios/relaciones.py);
    - el PESO de la arista es la DISTANCIA entre los dos juegos: 0 si son
      idénticos y 1 si no tienen nada en común. Cuanto menor el peso, más
      parecidos son. Un peso nunca negativo permite usar Dijkstra más adelante.

Decisiones de diseño (se explican en docs/09-analisis-tp7.md):
    - NO DIRIGIDO: si A está relacionado con B, B lo está con A (relación simétrica).
    - PESADO: no alcanza con saber que dos juegos se relacionan; importa cuánto.
    - LISTA DE ADYACENCIA: cada vértice guarda solo sus vecinos. El grafo es
      RALO (cada juego tiene unos 10 vecinos entre 2000), y una matriz de
      2000 x 2000 desperdiciaría memoria en casillas vacías.

Se implementa con un diccionario de diccionarios:
    {vertice: {vecino: peso, vecino2: peso2, ...}, ...}
Así preguntar "¿hay arista entre A y B?" o "¿cuál es su peso?" cuesta O(1).

Esta clase parte del grafo base que dio la cátedra (grafo.py: lista de
adyacencia con add_vertex / add_edge) y le suma pesos y aristas no dirigidas.

Uso:
    g = Grafo()
    g.agregar_vertice("A"); g.agregar_vertice("B")
    g.agregar_arista("A", "B", 0.3)
    g.vecinos("A")   # -> [("B", 0.3)]
"""


class Grafo:
    """Grafo no dirigido y pesado, representado con lista de adyacencia."""

    def __init__(self):
        # vertice -> {vecino: peso}. Se guarda en un atributo "privado" (_).
        self._adyacencia = {}

    # ==================== VÉRTICES ====================

    def agregar_vertice(self, vertice):
        """Agrega un vértice. Si ya existía, no hace nada. O(1)."""
        if vertice not in self._adyacencia:
            self._adyacencia[vertice] = {}

    def hay_vertice(self, vertice):
        """Devuelve True si el vértice está en el grafo. O(1)."""
        return vertice in self._adyacencia

    def vertices(self):
        """Devuelve la lista de todos los vértices. O(V)."""
        return list(self._adyacencia)

    # ==================== ARISTAS ====================

    def agregar_arista(self, origen, destino, peso=1):
        """Une dos vértices con una arista de un peso dado. O(1).

        Como el grafo es no dirigido, la arista se guarda en los dos sentidos.
        Si la arista ya existía, se actualiza su peso.
        Lanza ValueError si algún vértice no existe, si se intenta unir un
        vértice consigo mismo o si el peso es negativo.
        """
        if origen not in self._adyacencia or destino not in self._adyacencia:
            raise ValueError("Vértice inválido: hay que agregarlo antes de unirlo.")
        if origen == destino:
            raise ValueError("No se admiten aristas de un vértice consigo mismo.")
        if peso < 0:
            raise ValueError("El peso no puede ser negativo.")
        self._adyacencia[origen][destino] = peso
        self._adyacencia[destino][origen] = peso

    def hay_arista(self, origen, destino):
        """Devuelve True si los dos vértices están unidos. O(1)."""
        return destino in self._adyacencia.get(origen, {})

    def peso(self, origen, destino):
        """Devuelve el peso de la arista, o None si no existe. O(1)."""
        return self._adyacencia.get(origen, {}).get(destino)

    # ==================== CONSULTAS ====================

    def vecinos(self, vertice):
        """Devuelve los vecinos de un vértice como lista de (vecino, peso).

        Vienen ordenados del más cercano (peso menor) al más lejano. Si el
        vértice no existe devuelve una lista vacía. O(g log g), con g = grado.
        """
        vecinos = self._adyacencia.get(vertice, {})
        return sorted(vecinos.items(), key=lambda par: par[1])

    def grado(self, vertice):
        """Cantidad de aristas que tiene un vértice. O(1)."""
        return len(self._adyacencia.get(vertice, {}))

    def cantidad_vertices(self):
        """Cantidad de vértices del grafo. O(1)."""
        return len(self._adyacencia)

    def cantidad_aristas(self):
        """Cantidad de aristas del grafo. O(V).

        Cada arista aparece dos veces (una por cada extremo), por eso la suma
        de los grados se divide por 2.
        """
        return sum(len(vecinos) for vecinos in self._adyacencia.values()) // 2

    def __repr__(self):
        return (f"Grafo({self.cantidad_vertices()} vértices, "
                f"{self.cantidad_aristas()} aristas)")
