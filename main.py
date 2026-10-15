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
    clave = lambda j: j.get_nombre().lower()
    bst = ArbolBST()
    avl = AVL()
    for juego in catalogo.listar():
        bst.insertar(juego, clave=clave)
        avl.insertar(juego, clave=clave)
    return bst, avl


catalogo = cargar_catalogo()
bst, avl = construir_arboles(catalogo)
arbol_categorias = construir_arbol_categorias(catalogo)  # árbol general (TP5)

print(f"Catálogo cargado: {catalogo.cantidad()} juegos "
        f"· altura BST: {bst.altura()} · altura AVL: {avl.altura()} "
        f"· árbol de categorías: {arbol_categorias.cantidad_nodos()} nodos")

iniciar(catalogo, bst, avl, arbol_categorias)