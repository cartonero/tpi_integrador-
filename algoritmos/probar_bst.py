"""Script de prueba del árbol binario de búsqueda (TP3).

Corre independiente del menú, usando el catálogo real de Juegoteca.
La salida de este script se pega en docs/07-analisis-tp3.md como
evidencia de que el árbol funciona.
"""
from estructuras.arbol_binario import ArbolBST
from servicios.cargador_datos import cargar_catalogo


def main():
    catalogo = cargar_catalogo()
    juegos = catalogo.listar()

    arbol = ArbolBST()
    for juego in juegos:
        arbol.insertar(juego, clave=lambda j: j.get_nombre().lower())

    print(f"Juegos cargados: {len(juegos)}")
    print("Altura del árbol:", arbol.altura())

    print("\n--- inorder (primeros 10, ordenado alfabéticamente) ---")
    for juego in arbol.inorder()[:10]:
        print(" ", juego.get_nombre())

    print("\n--- preorder (primeros 10) ---")
    for juego in arbol.preorder()[:10]:
        print(" ", juego.get_nombre())

    print("\n--- postorder (primeros 10) ---")
    for juego in arbol.postorder()[:10]:
        print(" ", juego.get_nombre())

    print("\n--- búsquedas ---")
    nombre_existente = juegos[0].get_nombre()
    encontrado = arbol.buscar(nombre_existente.lower(), clave=lambda j: j.get_nombre().lower())
    print(f"Buscar '{nombre_existente}':", encontrado)

    no_encontrado = arbol.buscar("juego que no existe zzz", clave=lambda j: j.get_nombre().lower())
    print("Buscar 'juego que no existe zzz':", no_encontrado)


if __name__ == "__main__":
    main()