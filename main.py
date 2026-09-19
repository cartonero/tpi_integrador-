from servicios.cargador_datos import cargar_catalogo
from estructuras.arbol_binario import ArbolBST
from ui.terminal import iniciar


def construir_arbol(catalogo):
    """Inserta todos los juegos del catálogo en un BST ordenado por nombre.

    Se construye UNA sola vez, al arrancar el programa. Después, cada
    búsqueda del menú aprovecha el árbol ya armado.
    """
    arbol = ArbolBST()
    for juego in catalogo.listar():
        arbol.insertar(juego, clave=lambda j: j.get_nombre().lower())
    return arbol


catalogo = cargar_catalogo()
arbol = construir_arbol(catalogo)

print(f"Catálogo cargado: {catalogo.cantidad()} juegos "
        f"· altura del árbol: {arbol.altura()}")

iniciar(catalogo, arbol)