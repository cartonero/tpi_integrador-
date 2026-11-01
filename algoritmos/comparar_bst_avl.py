"""
algoritmos/comparar_bst_avl.py — TP4: BST común vs AVL.

Demuestra qué pasa cuando los datos llegan ORDENADOS (el peor caso del
BST): el BST se degenera en una "lista enlazada" y el AVL se mantiene
balanceado gracias a las rotaciones.

Parte 1: nombres de juegos ordenados alfabéticamente, con varios N.
Parte 2: el catálogo real de Juegoteca (2000 juegos, en el orden del JSON).

Los nombres de la Parte 1 se leen del CSV original de Steam (lux/games.csv)
fila por fila. Así no hace falta cargar los ~900 MB del JSON en memoria.

La construcción de los árboles se cronometra aparte (columnas "Construir").
La columna "Buscar" mide solo la búsqueda del PEOR caso: el último nombre
insertado, que en un BST degenerado está al fondo de la cadena.

Correr desde la raíz del proyecto con:
    py -m algoritmos.comparar_bst_avl
"""
import csv
import sys
import time

from estructuras.arbol_binario import ArbolBST
from estructuras.avl import AVL
from algoritmos.medir_tiempos import medir_ms
from servicios.cargador_datos import cargar_catalogo

# El BST degenerado con N datos ordenados tiene N niveles de recursión.
# Python por defecto permite 1000, así que lo subimos para poder medirlo.
sys.setrecursionlimit(30000)

# Algunas celdas del CSV (descripciones) son enormes: subimos el límite.
csv.field_size_limit(2**31 - 1)

RUTA_CSV_STEAM = "lux/games.csv"
TAMANOS = [100, 1_000, 5_000, 10_000]  # cantidades de nombres a probar
REPETICIONES = 100  # búsquedas promediadas por medición


def cargar_nombres_csv(ruta, cantidad_maxima):
    """Lee los nombres de juegos del CSV de Steam, fila por fila.

    La columna 1 del CSV es "Name". Se corta al juntar `cantidad_maxima`.
    """
    nombres = []
    with open(ruta, "r", encoding="utf-8", newline="") as archivo:
        # csv.reader entrega una fila por vez (una lista de columnas), sin
        # cargar el archivo completo en memoria.
        lector = csv.reader(archivo)
        next(lector)  # saltar la cabecera
        for fila in lector:
            if len(fila) < 2:
                continue  # fila vacía o rota: se ignora
            nombre = fila[1].strip()
            if nombre:
                nombres.append(nombre)
            if len(nombres) >= cantidad_maxima:
                break
    return nombres


def construir(arbol, datos, clave):
    """Inserta todos los datos y devuelve cuántos segundos tardó."""
    inicio = time.perf_counter()
    for dato in datos:
        arbol.insertar(dato, clave=clave)
    return time.perf_counter() - inicio


def parte_1_datos_ordenados():
    """Compara BST y AVL con nombres ORDENADOS, el peor caso para el BST."""
    pool = cargar_nombres_csv(RUTA_CSV_STEAM, 20_000)
    # set(...) elimina repetidos (en minúsculas) y sorted(...) los ordena
    # alfabéticamente. Insertar datos ya ordenados es lo que degenera al BST.
    nombres = sorted(set(n.lower() for n in pool))
    print(f"Nombres únicos disponibles (ordenados): {len(nombres)}\n")

    print("=== PARTE 1: nombres ordenados alfabéticamente (peor caso del BST) ===")
    print(f"{'N':>7} | {'Altura BST':>10} | {'Altura AVL':>10} | "
          f"{'Buscar BST (ms)':>15} | {'Buscar AVL (ms)':>15} | "
          f"{'Construir BST (s)':>17} | {'Construir AVL (s)':>17}")
    print("-" * 115)

    # Los datos son textos simples, así que la clave es el propio texto.
    clave = lambda x: x
    for n in TAMANOS:
        if n > len(nombres):
            print(f"{n:>7} | (no hay suficientes datos, se omite)")
            continue

        datos = nombres[:n]  # los primeros n nombres, ya ordenados
        objetivo = datos[-1]  # peor caso: el último insertado

        # Se construyen los dos árboles con exactamente los mismos datos.
        bst = ArbolBST()
        avl = AVL()
        t_cons_bst = construir(bst, datos, clave)
        t_cons_avl = construir(avl, datos, clave)

        # Se mide solo la búsqueda (el árbol ya está armado).
        t_bus_bst = medir_ms(lambda: bst.buscar(objetivo, clave=clave), REPETICIONES)
        t_bus_avl = medir_ms(lambda: avl.buscar(objetivo, clave=clave), REPETICIONES)

        # Resultado esperado: altura BST = n (una cadena) y altura AVL
        # cercana a log2(n).
        print(f"{n:>7} | {bst.altura():>10} | {avl.altura():>10} | "
              f"{t_bus_bst:>15.4f} | {t_bus_avl:>15.4f} | "
              f"{t_cons_bst:>17.2f} | {t_cons_avl:>17.2f}")


def parte_2_catalogo_real():
    """Compara BST y AVL con el catálogo real (juegos en el orden del JSON)."""
    catalogo = cargar_catalogo()
    juegos = catalogo.listar()
    clave = lambda j: j.get_nombre().lower()

    bst = ArbolBST()
    avl = AVL()
    construir(bst, juegos, clave)
    construir(avl, juegos, clave)

    # Acá los datos NO están ordenados, así que la diferencia es más chica
    # que en la parte 1 (27 contra 13), pero el AVL igual queda más bajo.
    print("\n=== PARTE 2: catálogo real de Juegoteca (orden original del JSON) ===")
    print(f"Juegos en el catálogo : {len(juegos)}")
    print(f"Altura del BST        : {bst.altura()}")
    print(f"Altura del AVL        : {avl.altura()}")
    print(f"Nodos del AVL         : {len(avl)} (ignora nombres repetidos)")


def main():
    parte_1_datos_ordenados()
    parte_2_catalogo_real()


# Este bloque solo corre al ejecutar el archivo directamente, no al importarlo.
if __name__ == "__main__":
    main()