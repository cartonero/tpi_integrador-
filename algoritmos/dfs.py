"""
dfs.py — Búsqueda en profundidad sobre el grafo de juegos (TP8).

DFS (Depth-First Search) se mete lo más hondo posible por un camino antes de
volver y probar otro. Para eso usa una PILA: el último que entra es el primero
que se procesa (LIFO).

BFS responde "¿qué tan cerca?"; DFS responde "¿qué hay en total conectado
con esto?". Como llega hasta el fondo de cada rama, es la forma natural de
explorar un grupo completo de juegos relacionados.

Complejidad: O(V + E), igual que BFS. Memoria: O(V).

Se escribe con una pila explícita (una lista) y no con recursión, porque un
grupo de juegos conectados puede ser muy largo y la recursión de Python tiene
un límite de profundidad.
"""


def _dfs_desde(grafo, inicio, visitados):
    """DFS desde `inicio`, saltando lo que ya esté en `visitados` (se actualiza).

    Devuelve la lista de vértices en el orden en que se visitaron.
    """
    orden = []
    pila = [inicio]
    while pila:
        vertice = pila.pop()
        if vertice in visitados:
            continue  # pudo entrar a la pila dos veces por caminos distintos
        visitados.add(vertice)
        orden.append(vertice)
        # Se apilan al revés para que el PRIMERO en salir sea el vecino más
        # parecido (vecinos() viene del más parecido al menos parecido).
        for vecino, _peso in reversed(grafo.vecinos(vertice)):
            if vecino not in visitados:
                pila.append(vecino)
    return orden


def dfs(grafo, inicio):
    """Explora en profundidad todo lo alcanzable desde `inicio`.

    Devuelve la lista de vértices en el orden de visita (el primero es `inicio`).
    Lanza ValueError si `inicio` no está en el grafo.
    """
    if not grafo.hay_vertice(inicio):
        raise ValueError("El vértice de partida no está en el grafo.")
    return _dfs_desde(grafo, inicio, set())


def componentes_conexas(grafo):
    """Separa el grafo en grupos de vértices que se alcanzan entre sí.

    Devuelve una lista de listas, de la más grande a la más chica. Dos juegos
    están en el mismo grupo si hay algún camino de relaciones que los une.
    Sirve para saber si entre dos juegos puede haber un camino o no.

    Costo total O(V + E): cada vértice se visita una sola vez en todo el proceso.
    """
    visitados = set()
    componentes = []
    for vertice in grafo.vertices():
        if vertice not in visitados:
            componentes.append(_dfs_desde(grafo, vertice, visitados))
    componentes.sort(key=len, reverse=True)
    return componentes
