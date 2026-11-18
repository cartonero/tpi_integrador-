"""
algoritmos/altas_masivas.py — Desafío "agreguen 100.000 elementos y busquen de nuevo".

Agrega muchos juegos inventados (nombres al azar) al sistema y mide:
  - cuánto tarda cada fase (altas, armado del grafo),
  - cuánto tarda buscar ANTES y DESPUÉS (secuencial vs AVL),
  - la altura del BST y del AVL,
  - que el catálogo, el BST y el AVL queden con la misma cantidad de juegos.

Se ejecuta desde la raíz del proyecto:
    py -m algoritmos.altas_masivas            (100.000 juegos)
    py -m algoritmos.altas_masivas 20000      (otra cantidad)

No modifica datos/games.json: todo ocurre en memoria.

Por qué el grafo se arma UNA vez al final y no en cada alta: incorporar un
juego al grafo cuesta O(n) (se compara contra todos los demás). Con 100.000
altas serían unas 10.000 millones de comparaciones. Armar el grafo completo
una sola vez cuesta bastante menos (se agrupan los juegos por combinación
de géneros), y el resultado es el mismo tipo de grafo.
"""
import random
import sys
import time

from servicios.cargador_datos import cargar_catalogo
from servicios.categorias import generos_validos
from servicios.juegos import agregar_juego, clave_nombre
from servicios.relaciones import construir_grafo_relacionados
from estructuras.arbol_binario import ArbolBST
from estructuras.avl import AVL

sys.setrecursionlimit(10_000)  # igual que main.py: el BST es recursivo
REPETICIONES = 200  # búsquedas promediadas


def buscar_secuencial(catalogo, nombre):
    """Recorre el catálogo entero hasta encontrar el nombre. O(n)."""
    for juego in catalogo.listar():
        if juego.get_nombre().lower() == nombre:
            return juego
    return None


def medir_ms(funcion, repeticiones=REPETICIONES):
    """Milisegundos promedio de UNA llamada a `funcion`."""
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        funcion()
    return (time.perf_counter() - inicio) / repeticiones * 1000


def main():
    """Corre el desafío de altas masivas y muestra las mediciones."""
    cantidad = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    azar = random.Random(2026)  # semilla fija: siempre los mismos nombres

    # Estado inicial: lo mismo que arma main.py (sin el árbol de categorías).
    catalogo = cargar_catalogo()
    bst, avl = ArbolBST(), AVL()
    for juego in catalogo.listar():
        bst.insertar(juego, clave_nombre)
        avl.insertar(juego, clave_nombre)
    print(f"Estado inicial: {catalogo.cantidad()} juegos "
          f"· altura BST {bst.altura()} · altura AVL {avl.altura()}")

    objetivo = catalogo.listar()[len(catalogo.listar()) // 2].get_nombre().lower()
    antes_sec = medir_ms(lambda: buscar_secuencial(catalogo, objetivo))
    antes_avl = medir_ms(lambda: avl.buscar(objetivo, clave=clave_nombre))

    # --- Altas: nombres al azar, uno por uno, por el mismo camino que el menú ---
    generos = generos_validos()
    print(f"\nAgregando {cantidad:,} juegos...".replace(",", "."))
    inicio = time.perf_counter()
    for i in range(cantidad):
        nombre = f"Juego {azar.randrange(10**9):09d} {i}"
        agregar_juego(nombre, [azar.choice(generos)], azar.randrange(0, 6000),
                      catalogo, bst, avl)
    t_altas = time.perf_counter() - inicio

    # --- Grafo: se arma una vez con todos los juegos ---
    inicio = time.perf_counter()
    grafo = construir_grafo_relacionados(catalogo)
    t_grafo = time.perf_counter() - inicio

    despues_sec = medir_ms(lambda: buscar_secuencial(catalogo, objetivo))
    despues_avl = medir_ms(lambda: avl.buscar(objetivo, clave=clave_nombre))

    print(f"\n{'Fase':<28}{'Tiempo':>12}")
    print("-" * 40)
    print(f"{'Altas (catálogo+BST+AVL)':<28}{t_altas:>10.2f} s")
    print(f"{'Armar el grafo':<28}{t_grafo:>10.2f} s")
    print(f"\n{'Búsqueda (ms)':<28}{'Antes':>10}{'Después':>12}")
    print("-" * 50)
    print(f"{'Secuencial':<28}{antes_sec:>10.4f}{despues_sec:>12.4f}")
    print(f"{'AVL':<28}{antes_avl:>10.4f}{despues_avl:>12.4f}")
    print(f"\nJuegos en catálogo: {catalogo.cantidad():,}".replace(",", "."))
    print(f"Altura BST: {bst.altura()} · altura AVL: {avl.altura()}")
    vertices = f"{grafo.cantidad_vertices():,}".replace(",", ".")
    aristas = f"{grafo.cantidad_aristas():,}".replace(",", ".")
    print(f"Grafo: {vertices} vértices, {aristas} aristas")

    # Coherencia: el BST guarda todos los juegos (incluso con nombre repetido);
    # el AVL ignora los nombres repetidos, así que tiene un juego por nombre.
    nombres_distintos = len({j.get_nombre().lower() for j in catalogo.listar()})
    coherente = (len(bst.inorder()) == catalogo.cantidad()
                 and len(avl.inorder()) == nombres_distintos)
    print("Catálogo, BST y AVL coherentes:", "SÍ" if coherente else "NO")


if __name__ == "__main__":
    main()
