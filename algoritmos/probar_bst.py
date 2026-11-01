"""Script de prueba del árbol binario de búsqueda (TP3).

Corre independiente del menú, usando el catálogo real de Juegoteca.
La salida de este script se pega en docs/07-analisis-tp3.md como
evidencia de que el árbol funciona.

Qué prueba, en orden:
  1. Arma un BST con los 2000 juegos y muestra su altura.
  2. Muestra los tres recorridos (inorder, preorder, postorder).
  3. Busca un juego que existe y uno que no existe.

Correr desde la raíz del proyecto con:
    py -m algoritmos.probar_bst
"""
from estructuras.arbol_binario import ArbolBST
from servicios.cargador_datos import cargar_catalogo


def main():
    # Cargamos el catálogo real (JSON -> objetos Juego).
    catalogo = cargar_catalogo()
    juegos = catalogo.listar()

    # Armamos el árbol ordenado por nombre en minúsculas.
    arbol = ArbolBST()
    for juego in juegos:
        arbol.insertar(juego, clave=lambda j: j.get_nombre().lower())

    print(f"Juegos cargados: {len(juegos)}")
    print("Altura del árbol:", arbol.altura())

    # Cada recorrido devuelve todos los juegos; mostramos solo los 10
    # primeros con [:10]. Inorder sale ordenado alfabéticamente.
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
    # Búsqueda que tiene que ENCONTRAR: usamos un juego que sabemos que está
    # (el primero del catálogo).
    nombre_existente = juegos[0].get_nombre()
    encontrado = arbol.buscar(nombre_existente.lower(), clave=lambda j: j.get_nombre().lower())
    print(f"Buscar '{nombre_existente}':", encontrado)

    # Búsqueda que tiene que devolver None (el nombre no existe).
    no_encontrado = arbol.buscar("juego que no existe zzz", clave=lambda j: j.get_nombre().lower())
    print("Buscar 'juego que no existe zzz':", no_encontrado)


# Este bloque solo corre al ejecutar el archivo directamente, no al importarlo.
if __name__ == "__main__":
    main()