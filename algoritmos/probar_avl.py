"""
algoritmos/probar_avl.py — Script de pruebas del TP4 (AVL) y TP5 (Árbol General).

Corre todas las pruebas juntas, sin pasar por el menú:
    1. Las 4 rotaciones del AVL, una por una.
    2. Caso de desbalance: 10 elementos ORDENADOS (A..J) en BST vs AVL.
    3. El AVL con el catálogo real de Juegoteca.
    4. El árbol general con la jerarquía de categorías de Steam.

La salida de este script se pega en docs/08-analisis-tp4-tp5.md como
evidencia de que ambas estructuras funcionan.

Las pruebas usan `assert`: si una condición es falsa el programa se detiene
con un AssertionError. Si termina mostrando "TODAS LAS PRUEBAS PASARON",
todas las condiciones se cumplieron.

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
        # Texto al imprimir: por ejemplo "A(1)"
        return f"{self.nombre}({self.valor})"


def verificar_balance(nodo):
    """Devuelve (esta_balanceado, altura).

    Revisa que en TODOS los nodos la diferencia de alturas entre el hijo
    izquierdo y el derecho sea -1, 0 o +1 (la regla del AVL).
    """
    # Un árbol vacío está balanceado y tiene altura 0.
    if nodo is None:
        return True, 0
    # Se revisa recursivamente cada subárbol (cada uno devuelve su estado y su altura).
    ok_izq, alt_izq = verificar_balance(nodo.izquierdo)
    ok_der, alt_der = verificar_balance(nodo.derecho)
    # El nodo está bien si ambos subárboles están bien Y sus alturas difieren
    # en 1 como máximo.
    ok = ok_izq and ok_der and abs(alt_izq - alt_der) <= 1
    return ok, 1 + max(alt_izq, alt_der)


def titulo(texto):
    """Imprime un título entre dos líneas de '=' para separar las secciones."""
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


# ==================== 1. ROTACIONES ====================

def probar_rotaciones():
    """Fuerza cada una de las 4 rotaciones con solo 3 inserciones."""
    titulo("1. LAS 4 ROTACIONES DEL AVL")
    print("Cada caso inserta 3 números que desbalancean el árbol. Si la rotación")
    print("funciona, el 2 queda como raíz y el árbol queda con altura 2.\n")

    # Cada caso es (nombre, orden de inserción). Con 3 números, el orden
    # determina qué desbalance se produce y por lo tanto qué rotación hace falta.
    casos = [
        ("Simple derecha (izquierda-izquierda)", [3, 2, 1]),
        ("Simple izquierda (derecha-derecha)", [1, 2, 3]),
        ("Doble izquierda-derecha", [3, 1, 2]),
        ("Doble derecha-izquierda", [1, 3, 2]),
    ]
    for nombre, orden in casos:
        avl = AVL()
        for numero in orden:
            # La clave es el número mismo (x -> x).
            avl.insertar(numero, clave=lambda x: x)
        # Sin rotación, el 3-2-1 sería una cadena de altura 3 con el 3 (o el 1)
        # arriba. Si la rotación funcionó, el 2 queda en la raíz y la altura es 2.
        assert avl.raiz.dato == 2 and avl.altura() == 2 # type: ignore
        print(f"  {nombre:<40} insertar {orden} -> "
                f"raíz {avl.raiz.dato}, preorder {avl.preorder()}, altura {avl.altura()}") # type: ignore
    print("\nVerificación: las 4 rotaciones dejan el árbol balanceado. OK")


# ==================== 2. DESBALANCE: BST vs AVL ====================

def probar_desbalance():
    """Inserta A..J en orden y compara cómo queda el BST contra el AVL."""
    titulo("2. DATOS ORDENADOS (A..J): BST común vs AVL")
    # enumerate(..., start=1) numera las letras desde 1: A(1), B(2), ..., J(10).
    datos = [Elemento(letra, i) for i, letra in enumerate("ABCDEFGHIJ", start=1)]
    clave = lambda x: x.nombre.lower()

    # Se insertan los MISMOS datos, en el mismo orden, en los dos árboles.
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

    # Verificaciones automáticas: el inorder tiene que coincidir con la lista
    # ordenada, el AVL tiene que cumplir la regla de balance en todos los
    # nodos, y las alturas tienen que ser las esperadas (10 y 4).
    balanceado, _ = verificar_balance(avl.raiz)
    assert avl.inorder() == sorted(datos, key=clave)
    assert balanceado and bst.altura() == 10 and avl.altura() == 4
    print("\nVerificación: inorder ordenado y todos los nodos con balance -1/0/+1. OK")


# ==================== 3. AVL CON EL CATÁLOGO REAL ====================

def probar_avl_catalogo():
    """Arma el AVL con los 2000 juegos reales y busca un juego."""
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
    # El AVL no guarda nombres repetidos, por eso tiene un nodo menos que juegos.
    print(f"Nodos del AVL         : {len(avl)} (ignora nombres repetidos)")

    print("\n--- inorder del AVL (primeros 5) ---")
    for juego in avl.inorder()[:5]:
        print(" ", juego.get_nombre())

    print("\n--- búsquedas ---")
    existente = juegos[0].get_nombre()
    print(f"Buscar '{existente}':", avl.buscar(existente.lower(), clave=clave))
    print("Buscar 'juego que no existe zzz':",
          avl.buscar("juego que no existe zzz", clave=clave))

    # Comprueba que el AVL real cumple la regla de balance en TODOS sus nodos.
    balanceado, _ = verificar_balance(avl.raiz)
    assert balanceado
    print("\nVerificación: todos los nodos con balance -1/0/+1. OK")


# ==================== 4. ÁRBOL GENERAL ====================

def probar_arbol_general():
    """Arma el árbol de categorías y prueba sus recorridos y búsquedas."""
    titulo("4. ÁRBOL GENERAL: JERARQUÍA DE CATEGORÍAS DE STEAM")
    catalogo = cargar_catalogo()
    arbol = construir_arbol_categorias(catalogo)

    print(arbol)
    print(f"Cantidad de nodos : {arbol.cantidad_nodos()}")
    print(f"Altura            : {arbol.altura()}")

    # Se muestran solo los primeros 8 elementos de cada recorrido ([:8]).
    # Amplitud = nivel por nivel; preorder/postorder = en profundidad.
    print("\n--- Recorrido en AMPLITUD (primeros 8) ---")
    print(" ", arbol.amplitud()[:8])

    print("\n--- Recorrido en PROFUNDIDAD preorder (primeros 8) ---")
    print(" ", arbol.profundidad_preorder()[:8])

    print("\n--- Recorrido en PROFUNDIDAD postorder (primeros 8) ---")
    print(" ", arbol.profundidad_postorder()[:8])

    print("\n--- Niveles ---")
    for i, nivel in enumerate(arbol.obtener_niveles()):
        print(f"Nivel {i}:")
        # textwrap.fill parte la lista larga de géneros en renglones de 70 caracteres.
        print(textwrap.fill(", ".join(nivel), width=70,
                            initial_indent="  ", subsequent_indent="  "))

    print("\n--- Búsquedas ---")
    juegos = arbol.buscar("Juegos")
    print("Hijos de 'Juegos':", arbol.listar_hijos(juegos))
    print("Buscar 'Indie':", arbol.buscar("Indie"))
    print("Buscar 'Zzz':", arbol.buscar("Zzz"))

    # 31 nodos = 1 raíz + 4 grupos + 26 géneros; altura 3 = raíz, grupos, géneros.
    assert arbol.cantidad_nodos() == 31 and arbol.altura() == 3
    assert arbol.buscar("Indie") is not None and arbol.buscar("Zzz") is None
    print("\nVerificación: 31 nodos, altura 3, búsquedas correctas. OK")


def main():
    probar_rotaciones()
    probar_desbalance()
    probar_avl_catalogo()
    probar_arbol_general()
    titulo("TODAS LAS PRUEBAS PASARON")


# Este bloque solo corre al ejecutar el archivo directamente, no al importarlo.
if __name__ == "__main__":
    main()