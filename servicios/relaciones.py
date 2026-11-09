"""
servicios/relaciones.py — Arma el grafo de juegos relacionados (TP7).

Define CUÁNDO dos juegos están relacionados y construye el Grafo con esa regla.

SIMILITUD entre dos juegos (número de 0 a 1):
    Es un índice de Jaccard con pesos sobre sus géneros:
        similitud = (peso de los géneros que comparten) / (peso de todos los géneros que tienen)
    El peso de un género es mayor cuanto MÁS RARO es: compartir "Metroidvania"
    dice más que compartir "Indie", que está en casi todos los juegos. Sin esto
    el grafo no serviría: con un género común todos quedarían unidos entre sí
    (en la muestra, 1.499.903 de 1.999.000 pares posibles, un 75%).

ARISTAS:
    Cada juego se une con sus K juegos más parecidos (K = 5 por defecto). Como
    el grafo es no dirigido, si A elige a B entonces B también queda unido a A,
    por lo que un juego puede terminar con más de K vecinos. El resultado es un
    grafo RALO: unas 5 a 10 aristas por vértice en lugar de cientos.
    El PESO de la arista es la distancia = 1 - similitud (0 = idénticos).

Limitación que declaramos: la muestra solo trae géneros, tiempo de juego y
votos (no hay desarrolladora ni etiquetas), así que la similitud se basa
únicamente en géneros.
"""
import math

from estructuras.grafo import Grafo

VECINOS_POR_JUEGO = 5


def pesos_de_generos(juegos):
    """Devuelve {genero: peso}. Cuanto menos juegos tienen un género, más pesa.

    peso = log(1 + N / cantidad_de_juegos_con_ese_genero). Siempre es mayor
    que 0, y es chico para los géneros muy comunes.
    """
    total = len(juegos)
    frecuencia = {}
    for juego in juegos:
        for genero in set(juego.get_generos()):
            frecuencia[genero] = frecuencia.get(genero, 0) + 1
    return {g: math.log(1 + total / cantidad) for g, cantidad in frecuencia.items()}


def similitud(generos_a, generos_b, pesos):
    """Similitud (0 a 1) entre dos conjuntos de géneros, con pesos por género.

    Devuelve 0 si no comparten ningún género o si ambos están vacíos.
    """
    union = generos_a | generos_b
    if not union:
        return 0.0
    comunes = sum(pesos.get(g, 0) for g in generos_a & generos_b)
    total = sum(pesos.get(g, 0) for g in union)
    return comunes / total if total else 0.0


def construir_grafo_relacionados(catalogo, vecinos_por_juego=VECINOS_POR_JUEGO):
    """Arma el Grafo de juegos relacionados a partir del catálogo.

    Para no comparar todos los pares (2000 x 2000), se agrupan los juegos que
    tienen EXACTAMENTE el mismo conjunto de géneros: dentro de la muestra hay
    unos pocos cientos de combinaciones distintas. La similitud se calcula una
    vez por par de combinaciones, no por par de juegos.
    """
    juegos = catalogo.listar()
    pesos = pesos_de_generos(juegos)

    grafo = Grafo()
    for juego in juegos:
        grafo.agregar_vertice(juego)

    # grupos: {combinacion_de_generos: [juegos con esa combinacion, ordenados por nombre]}
    grupos = {}
    for juego in juegos:
        grupos.setdefault(frozenset(juego.get_generos()), []).append(juego)
    for miembros in grupos.values():
        miembros.sort(key=lambda j: j.get_nombre().lower())

    # Para cada combinación, el orden de combinaciones de la más parecida a la
    # menos parecida (ella misma primero, con similitud 1). Se calcula UNA vez
    # por combinación.
    combinaciones = list(grupos)
    orden_por_combinacion = {}
    for propia in combinaciones:
        ranking = []
        for otra in combinaciones:
            s = similitud(propia, otra, pesos)
            if s > 0:
                ranking.append((-s, sorted(otra), otra))  # sorted(): desempate estable
        ranking.sort(key=lambda t: (t[0], t[1]))
        orden_por_combinacion[propia] = [(-neg, otra) for neg, _, otra in ranking]

    for propia, miembros in grupos.items():
        for posicion, juego in enumerate(miembros):
            elegidos = 0
            for sim, otra in orden_por_combinacion[propia]:
                candidatos = grupos[otra]
                # Se arranca en una posición distinta para cada juego, así los
                # vecinos se reparten y no todos eligen al mismo (evita "hubs").
                inicio = posicion % len(candidatos)
                for paso in range(len(candidatos)):
                    candidato = candidatos[(inicio + paso) % len(candidatos)]
                    if candidato is juego:
                        continue
                    grafo.agregar_arista(juego, candidato, round(1 - sim, 6))
                    elegidos += 1
                    if elegidos == vecinos_por_juego:
                        break
                if elegidos == vecinos_por_juego:
                    break
    return grafo


def incorporar_juego(grafo, catalogo, juego, vecinos_por_juego=VECINOS_POR_JUEGO):
    """Agrega un juego nuevo al grafo, unido a sus K juegos más parecidos.

    Se usa al añadir un juego desde el menú. Compara el juego nuevo contra los
    demás (O(n)). Devuelve la cantidad de aristas creadas.
    """
    juegos = [j for j in catalogo.listar() if j is not juego]
    pesos = pesos_de_generos(catalogo.listar())
    generos = frozenset(juego.get_generos())

    grafo.agregar_vertice(juego)
    puntuados = []
    for otro in juegos:
        s = similitud(generos, frozenset(otro.get_generos()), pesos)
        if s > 0:
            puntuados.append((s, otro.get_nombre().lower(), otro))
    puntuados.sort(key=lambda t: (-t[0], t[1]))

    for s, _, otro in puntuados[:vecinos_por_juego]:
        grafo.agregar_arista(juego, otro, round(1 - s, 6))
    return min(vecinos_por_juego, len(puntuados))


def juegos_relacionados(grafo, juego, maximo=10):
    """Devuelve hasta `maximo` tuplas (juego_vecino, similitud_en_0_a_1).

    Los vecinos vienen del más parecido al menos parecido.
    """
    return [(vecino, 1 - peso) for vecino, peso in grafo.vecinos(juego)[:maximo]]
