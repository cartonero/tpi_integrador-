"""
bfs.py — Búsqueda en anchura sobre el grafo de juegos (TP8).

BFS (Breadth-First Search) explora el grafo POR CAPAS: primero el juego de
partida, después todos sus vecinos directos (1 salto), después los vecinos de
esos vecinos (2 saltos), y así. Para eso usa una COLA: el primero que entra
es el primero que se procesa (FIFO).

Como visita siempre las capas en orden, la primera vez que llega a un juego lo
hace por el camino con MENOS aristas. Por eso BFS sirve para preguntas del tipo
"¿qué tan cerca está?" o "¿cuántos saltos hay de un juego a otro?".

Complejidad: O(V + E). Cada vértice entra una sola vez a la cola y cada arista
se mira una sola vez por extremo. Memoria: O(V) (el conjunto de visitados y la cola).

Usa deque (de la biblioteca estándar) para la cola porque sacar del frente de
una lista común cuesta O(n); con deque cuesta O(1).
"""

from collections import deque


def bfs(grafo, inicio, max_saltos=None):
    """Recorre el grafo por capas desde `inicio`.

    Devuelve una lista de pares (vértice, saltos) en el orden en que BFS los
    visita. El primero es siempre (inicio, 0). Si se pasa `max_saltos`, no se
    avanza más allá de esa cantidad de saltos.

    Lanza ValueError si `inicio` no está en el grafo.
    """
    if not grafo.hay_vertice(inicio):
        raise ValueError("El vértice de partida no está en el grafo.")

    visitados = {inicio}
    cola = deque([(inicio, 0)])
    orden = []

    while cola:
        vertice, saltos = cola.popleft()
        orden.append((vertice, saltos))

        if max_saltos is not None and saltos >= max_saltos:
            continue  # llegamos al límite: no encolamos a sus vecinos

        # vecinos() los devuelve del más parecido al menos parecido, así que
        # dentro de una misma capa los juegos salen en ese orden.
        for vecino, _peso in grafo.vecinos(vertice):
            if vecino not in visitados:
                visitados.add(vecino)  # se marca al ENCOLAR para no encolarlo dos veces
                cola.append((vecino, saltos + 1))
    return orden


def bfs_saltos_entre(grafo, origen, destino):
    """Cuenta cuántos saltos hay entre dos vértices por el camino más corto.

    Un salto es pasar de un juego a otro relacionado directamente. BFS llega a
    cada vértice por el camino con menos aristas, así que el número de la capa
    en que aparece `destino` es la respuesta. Se corta apenas lo encuentra.

    Devuelve 0 si son el mismo vértice, y None si no hay ningún camino (están
    en grupos separados del grafo). Lanza ValueError si algún vértice no existe.
    """
    if not grafo.hay_vertice(origen) or not grafo.hay_vertice(destino):
        raise ValueError("Los dos vértices tienen que estar en el grafo.")

    visitados = {origen}
    cola = deque([(origen, 0)])

    while cola:
        vertice, saltos = cola.popleft()
        if vertice == destino:
            return saltos
        for vecino, _peso in grafo.vecinos(vertice):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, saltos + 1))
    return None
