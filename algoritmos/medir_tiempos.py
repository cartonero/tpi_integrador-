"""
algoritmos/medir_tiempos.py — TP3: comparación de tiempos de búsqueda.

Compara 3 estrategias de búsqueda por nombre de juego:
  - Secuencial (recorre la lista, O(n))
  - Binaria (sobre lista ordenada, O(log n))
  - Árbol BST (estructura del TP3, O(log n) promedio)

IMPORTANTE: la construcción de cada estructura (ordenar la lista para
binaria, insertar en el árbol) se hace UNA sola vez por tamaño y NO se
mide. Solo se cronometra la búsqueda en sí, promediada sobre varias
repeticiones para tener un tiempo estable.

Correr desde la raíz del proyecto con:
    py -m algoritmos.medir_tiempos

Nota: lee lux/games.json (~900 MB) con json.load, que lo carga entero en
memoria. En una computadora con poca RAM libre puede fallar con MemoryError
(en comparar_bst_avl.py se resolvió leyendo el CSV fila por fila).
"""
import json
import time

from estructuras.arbol_binario import ArbolBST


RUTA_DATASET_COMPLETO = "lux/games.json"
TAMANOS = [100, 1_000, 10_000, 100_000]  # cantidades de elementos a probar
REPETICIONES = 300  # búsquedas promediadas para un tiempo estable


def cargar_pool_de_juegos(ruta, cantidad_maxima):
    """Carga nombres de juegos válidos desde el dataset completo de Steam."""
    print("Cargando dataset completo (puede tardar)...")
    with open(ruta, "r", encoding="utf-8") as archivo:
        dataset = json.load(archivo)

    # Recorremos los juegos y juntamos los nombres hasta llegar a la cantidad
    # que necesitamos (el tamaño más grande de TAMANOS).
    nombres = []
    for datos in dataset.values():
        nombre = datos.get("name", "").strip()
        if nombre:
            nombres.append(nombre)
        if len(nombres) >= cantidad_maxima:
            break

    return nombres


def busqueda_secuencial(lista, objetivo):
    """Recorre la lista de a un elemento hasta encontrar el objetivo. O(n)."""
    for elemento in lista:
        if elemento == objetivo:
            return elemento
    return None


def busqueda_binaria(lista_ordenada, objetivo):
    """Busca en una lista ORDENADA descartando la mitad en cada paso. O(log n).

    Requiere que la lista esté ordenada; si no, no funciona.
    """
    # inicio y fin marcan la zona de la lista donde todavía puede estar el objetivo.
    inicio, fin = 0, len(lista_ordenada) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2  # posición central (// es división entera)
        if lista_ordenada[medio] == objetivo:
            return lista_ordenada[medio]
        elif lista_ordenada[medio] < objetivo:
            inicio = medio + 1  # el objetivo está en la mitad de la derecha
        else:
            fin = medio - 1     # el objetivo está en la mitad de la izquierda
    return None  # la zona quedó vacía: no está


def medir_ms(funcion, repeticiones=REPETICIONES):
    """Devuelve cuántos milisegundos tarda, en promedio, UNA llamada a `funcion`.

    Una sola búsqueda tarda microsegundos y es muy difícil medirla bien, así
    que se repite varias veces y se divide el tiempo total por la cantidad.
    `funcion` es una función sin parámetros (por eso abajo se usa lambda).
    """
    inicio = time.perf_counter()  # cronómetro de alta precisión
    for _ in range(repeticiones):
        funcion()
    fin = time.perf_counter()
    # (tiempo total / repeticiones) está en segundos; * 1000 lo pasa a milisegundos.
    return ((fin - inicio) / repeticiones) * 1000  # ms promedio por búsqueda


def main():
    pool_completo = cargar_pool_de_juegos(RUTA_DATASET_COMPLETO, max(TAMANOS))
    print(f"Juegos disponibles para la prueba: {len(pool_completo)}\n")

    print(f"{'N elementos':>12} | {'Secuencial (ms)':>16} | {'Binaria (ms)':>14} | {'Árbol BST (ms)':>15}")
    print("-" * 68)

    for n in TAMANOS:
        # Si el dataset tiene menos nombres que el tamaño pedido, se saltea.
        if n > len(pool_completo):
            print(f"{n:>12} | (no hay suficientes datos, se omite)")
            continue

        lista = pool_completo[:n]  # los primeros n nombres
        objetivo = lista[n // 2]  # siempre buscamos un elemento que SÍ existe

        # --- Preparación (NO se mide) ---
        # La binaria necesita la lista ordenada; el árbol se arma insertando
        # los nombres (en la clave se usa el texto tal cual: x -> x).
        lista_ordenada = sorted(lista)
        arbol = ArbolBST()
        for nombre in lista:
            arbol.insertar(nombre, clave=lambda x: x)

        # --- Medición (SÍ se mide, solo la búsqueda) ---
        # lambda: ... crea una función sin parámetros que ejecuta la búsqueda,
        # que es lo que medir_ms necesita para poder repetirla.
        t_secuencial = medir_ms(lambda: busqueda_secuencial(lista, objetivo))
        t_binaria = medir_ms(lambda: busqueda_binaria(lista_ordenada, objetivo))
        t_arbol = medir_ms(lambda: arbol.buscar(objetivo, clave=lambda x: x))

        print(f"{n:>12} | {t_secuencial:>16.4f} | {t_binaria:>14.4f} | {t_arbol:>15.4f}")


# Este bloque solo corre al ejecutar el archivo directamente, no al importarlo.
if __name__ == "__main__":
    main()