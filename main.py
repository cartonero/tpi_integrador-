"""
main.py — Punto de entrada de Juegoteca.

Se ejecuta desde la raíz del proyecto con:
    py main.py

Qué hace, en orden:
  1. Carga los juegos desde datos/games.json y arma el Catalogo.
  2. Construye dos árboles de búsqueda con esos juegos, ordenados por nombre:
       - BST (TP3): árbol binario de búsqueda común.
       - AVL (TP4): árbol binario auto-balanceado. Lo usa la opción "Buscar".
  3. Construye el árbol general (TP5) con la jerarquía de categorías
     (grupos de Steam -> géneros). Lo usa la opción "Explorar categorías".
  4. Muestra un resumen y abre el menú de la terminal (ui/terminal.py).

Las estructuras se construyen UNA sola vez al arrancar; después cada consulta
del menú las reutiliza sin volver a armarlas.

Nota: este archivo se ejecuta de arriba hacia abajo al correrlo.
"""
from servicios.cargador_datos import cargar_catalogo
from servicios.categorias import construir_arbol_categorias
from estructuras.arbol_binario import ArbolBST
from estructuras.avl import AVL
from ui.terminal import iniciar


def construir_arboles(catalogo):
    """Inserta todos los juegos del catálogo en dos árboles, ordenados por nombre.

    - BST (TP3): árbol de búsqueda común. Se mantiene para los recorridos
    y para poder comparar su altura contra la del AVL.
    - AVL (TP4): árbol auto-balanceado. Es el que usa la opción "Buscar".

    Se construyen UNA sola vez, al arrancar el programa.
    """
    # La "clave" es la función que le dice a los árboles POR QUÉ CAMPO
    # ordenar: el nombre del juego en minúsculas. Así "Portal" y "portal"
    # se tratan como el mismo nombre.
    clave = lambda j: j.get_nombre().lower()

    bst = ArbolBST()
    avl = AVL()

    # Cada juego se inserta en los dos árboles. El AVL se rebalancea solo
    # con rotaciones; el BST no, por eso termina más alto (ver altura abajo).
    for juego in catalogo.listar():
        bst.insertar(juego, clave=clave)
        avl.insertar(juego, clave=clave)
    return bst, avl


# 1) Carga de datos: JSON -> objetos Juego -> Catalogo.
catalogo = cargar_catalogo()

# 2) Árboles de búsqueda por nombre (BST del TP3 y AVL del TP4).
bst, avl = construir_arboles(catalogo)

# 3) Árbol general de categorías (TP5).
arbol_categorias = construir_arbol_categorias(catalogo)  # árbol general (TP5)

# 4) Resumen de arranque. La altura de un árbol es la cantidad de niveles:
#    cuanto más baja, más rápido se busca. Con los mismos datos el AVL queda
#    más bajo que el BST.
print(f"Catálogo cargado: {catalogo.cantidad()} juegos "
        f"· altura BST: {bst.altura()} · altura AVL: {avl.altura()} "
        f"· árbol de categorías: {arbol_categorias.cantidad_nodos()} nodos")

# 5) Abre el menú interactivo. Recibe las estructuras ya construidas.
iniciar(catalogo, bst, avl, arbol_categorias)