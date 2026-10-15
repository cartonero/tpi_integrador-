"""
algoritmos/probar_avl.py — Script de pruebas del TP4 (AVL) y TP5 (Árbol General).

Corre todas las pruebas juntas, sin pasar por el menú:
  1. Las 4 rotaciones del AVL, una por una.
  2. Caso de desbalance: 10 elementos ORDENADOS (A..J) en BST vs AVL.
  3. El AVL con el catálogo real de Juegoteca.
  4. El árbol general con la jerarquía de categorías de Steam.

La salida de este script se pega en docs/08-analisis-tp4-tp5.md como
evidencia de que ambas estructuras funcionan.

Correr desde la raíz del proyecto con:
    py -m algoritmos.probar_avl
"""
import textwrap

from estructuras.arbol_binario import ArbolBST
from estructuras.avl import AVL
from servicios.cargador_datos import cargar_catalogo
from servicios.categorias import construir_arbol_categorias


class Elemento:
    """Elemento simple para las pruebas con letras (A..J)."""

    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor

    def __repr__(self):
        return f"{self.nombre}({self.valor})"


def verificar_balance(nodo):
    """Devuelve (esta_balanceado, altura).

    Revisa que en TODOS los nodos la diferencia de alturas entre el hijo
    izquierdo y el derecho sea -1, 0 o +1 (la regla del AVL).
    """
    if nodo is None:
        return True, 0
    ok_izq, alt_izq = verificar_balance(nodo.izquierdo)
    ok_der, alt_der = verificar_balance(nodo.derecho)
    ok = ok_izq and ok_der and abs(alt_izq - alt_der) <= 1
    return ok, 1 + max(alt_izq, alt_der)


def titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


# ==================== 1. ROTACIONES ====================

def probar_rotaciones():
    titulo("1. LAS 4 ROTACIONES DEL AVL")
    print("Cada caso inserta 3 números que desbalancean el árbol. Si la rotación")
    print("funciona, el 2 queda como raíz y el árbol queda con altura 2.\n")

    casos = [
        ("Simple derecha (izquierda-izquierda)", [3, 2, 1]),
        ("Simple izquierda (derecha-derecha)", [1, 2, 3]),
        ("Doble izquierda-derecha", [3, 1, 2]),
        ("Doble derecha-izquierda", [1, 3, 2]),
    ]
    for nombre, orden in casos:
        avl = AVL()
        for numero in orden:
            avl.insertar(numero, clave=lambda x: x)
        assert avl.raiz.dato == 2 and avl.altura() == 2
        print(f"  {nombre:<40} insertar {orden} -> "
              f"raíz {avl.raiz.dato}, preorder {avl.preorder()}, altura {avl.altura()}")
    print("\nVerificación: las 4 rotaciones dejan el árbol balanceado. OK")


# ==================== 2. DESBALANCE: BST vs AVL ====================

def probar_desbalance():
    titulo("2. DATOS ORDENADOS (A..J): BST común vs AVL")
    datos = [Elemento(letra, i) for i, letra in enumerate("ABCDEFGHIJ", start=1)]
    clave = lambda x: x.nombre.lower()

    bst = ArbolBST()
    avl = AVL()
    for dato in datos:
        bst.insertar(dato, clave=clave)
        avl.insertar(dato, clave=clave)

    print(f"Elementos insertados en orden: {[d.nombre for d in datos]}")
    print(f"Altura del BST común : {bst.altura()}  (una cadena: cada nodo tiene un solo hijo)")
    print(f"Altura del AVL       : {avl.altura()}")
    print(f"Nodos del AVL        : {len(avl)}")

    print("\n--- inorder del AVL (tiene que salir ordenado) ---")
    print(" ", avl.inorder())
    print("\n--- preorder del AVL (muestra cómo quedó balanceado) ---")
    print(" ", avl.preorder())

    print("\n--- búsquedas ---")
    print("Buscar 'F':", avl.buscar("f", clave=clave))
    print("Buscar 'Z':", avl.buscar("z", clave=clave))

    balanceado, _ = verificar_balance(avl.raiz)
    assert avl.inorder() == sorted(datos, key=clave)
    assert balanceado and bst.altura() == 10 and avl.altura() == 4
    print("\nVerificación: inorder ordenado y todos los nodos con balance -1/0/+1. OK")


# ==================== 3. AVL CON EL CATÁLOGO REAL ====================

def probar_avl_catalogo():
    titulo("3. AVL CON EL CATÁLOGO REAL DE JUEGOTECA")
    catalogo = cargar_catalogo()
    juegos = catalogo.listar()
    clave = lambda j: j.get_nombre().lower()

    bst = ArbolBST()
    avl = AVL()
    for juego in juegos:
        bst.insertar(juego, clave=clave)
        avl.insertar(juego, clave=clave)

    print(f"Juegos en el catálogo : {len(juegos)}")
    print(f"Altura del BST        : {bst.altura()}")
    print(f"Altura del AVL        : {avl.altura()}")
    print(f"Nodos del AVL         : {len(avl)} (ignora nombres repetidos)")

    print("\n--- inorder del AVL (primeros 5) ---")
    for juego in avl.inorder()[:5]:
        print(" ", juego.get_nombre())

    print("\n--- búsquedas ---")
    existente = juegos[0].get_nombre()
    print(f"Buscar '{existente}':", avl.buscar(existente.lower(), clave=clave))
    print("Buscar 'juego que no existe zzz':",
          avl.buscar("juego que no existe zzz", clave=clave))

    balanceado, _ = verificar_balance(avl.raiz)
    assert balanceado
    print("\nVerificación: todos los nodos con balance -1/0/+1. OK")


# ==================== 4. ÁRBOL GENERAL ====================

def probar_arbol_general():
    titulo("4. ÁRBOL GENERAL: JERARQUÍA DE CATEGORÍAS DE STEAM")
    catalogo = cargar_catalogo()
    arbol = construir_arbol_categorias(catalogo)

    print(arbol)
    print(f"Cantidad de nodos : {arbol.cantidad_nodos()}")
    print(f"Altura            : {arbol.altura()}")

    print("\n--- Recorrido en AMPLITUD (primeros 8) ---")
    print(" ", arbol.amplitud()[:8])

    print("\n--- Recorrido en PROFUNDIDAD preorder (primeros 8) ---")
    print(" ", arbol.profundidad_preorder()[:8])

    print("\n--- Recorrido en PROFUNDIDAD postorder (primeros 8) ---")
    print(" ", arbol.profundidad_postorder()[:8])

    print("\n--- Niveles ---")
    for i, nivel in enumerate(arbol.obtener_niveles()):
        print(f"Nivel {i}:")
        print(textwrap.fill(", ".join(nivel), width=70,
                            initial_indent="  ", subsequent_indent="  "))

    print("\n--- Búsquedas ---")
    juegos = arbol.buscar("Juegos")
    print("Hijos de 'Juegos':", arbol.listar_hijos(juegos))
    print("Buscar 'Indie':", arbol.buscar("Indie"))
    print("Buscar 'Zzz':", arbol.buscar("Zzz"))

    assert arbol.cantidad_nodos() == 31 and arbol.altura() == 3
    assert arbol.buscar("Indie") is not None and arbol.buscar("Zzz") is None
    print("\nVerificación: 31 nodos, altura 3, búsquedas correctas. OK")


def main():
    probar_rotaciones()
    probar_desbalance()
    probar_avl_catalogo()
    probar_arbol_general()
    titulo("TODAS LAS PRUEBAS PASARON")


if __name__ == "__main__":
    main()