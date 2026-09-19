def mostrar_menu():
    print("=" * 40)
    print(" JUEGOTECA — TERMINAL")
    print("=" * 40)
    print("1. Buscar juego")
    print("2. Listar juegos")
    print("3. Filtrar por categoría")
    print("4. Ver recorridos del árbol (inorder / preorder / postorder)")
    print("0. Salir")
    print("-" * 40)


def ejecutar_buscar(arbol):
    """Busca usando el ÁRBOL BINARIO DE BÚSQUEDA (TP3).

    Antes (TP1) esta opción recorría toda la lista del catálogo: O(n).
    Ahora baja por el árbol descartando la mitad en cada paso: O(log n)
    promedio.
    """
    nombre = input("Nombre del juego: ").strip()
    juego = arbol.buscar(nombre.lower(), clave=lambda j: j.get_nombre().lower())
    if juego is None: 
        print(f"No se encontró ningún juego llamado '{nombre}'.")
    else:
        print(juego)


def ejecutar_listar(catalogo):
    juegos = catalogo.listar()
    if not juegos:
        print("El catálogo está vacío.")
        return

    tamano_pagina = 20
    inicio = 0

    while inicio < len(juegos):
        pagina = juegos[inicio:inicio + tamano_pagina]
        for juego in pagina:
            print(juego)

        inicio += tamano_pagina
        if inicio < len(juegos):
            seguir = input(
                f"\nMostrados {inicio} de {len(juegos)}. "
                "Enter para ver más, 'q' para volver al menú: "
            ).strip().lower()
            if seguir == "q":
                break


def ejecutar_filtrar(catalogo):
    categoria = input("Categoría a buscar (ej: Action, Indie, RPG): ").strip()
    resultados = catalogo.filtrar_por_categoria(categoria)
    if not resultados:
        print(f"No se encontraron juegos en la categoría '{categoria}'.")
        return

    print(f"\n{len(resultados)} juego(s) encontrados:")
    for juego in resultados[:20]:
        print(juego)
    if len(resultados) > 20:
        print(f"... y {len(resultados) - 20} más.")


def _formatear_juego(indice, juego, ancho_nombre=45):
    """Formatea una línea 'N. Nombre (Categoría)' con el nombre truncado
    si es muy largo, para que la lista quede alineada en la terminal."""
    nombre = juego.get_nombre()
    if len(nombre) > ancho_nombre:
        nombre = nombre[:ancho_nombre - 3] + "..."
    return f"  {indice:>2}. {nombre:<{ancho_nombre}} ({juego.get_categoria_principal()})"


def ejecutar_recorridos(arbol):
    """Muestra los 3 recorridos del árbol (TP3), limitados a 15 elementos."""
    print("\n--- INORDER (ordenado alfabéticamente) ---")
    for i, juego in enumerate(arbol.inorder()[:15], start=1):
        print(_formatear_juego(i, juego))

    print("\n--- PREORDER ---")
    for i, juego in enumerate(arbol.preorder()[:15], start=1):
        print(_formatear_juego(i, juego))

    print("\n--- POSTORDER ---")
    for i, juego in enumerate(arbol.postorder()[:15], start=1):
        print(_formatear_juego(i, juego))

    print(f"\n(Se muestran los primeros 15 de cada recorrido. Altura del árbol: {arbol.altura()})")


def iniciar(catalogo, arbol):
    while True:
        mostrar_menu()
        opcion = input("Opción: ").strip()

        if opcion == "1":
            ejecutar_buscar(arbol)
        elif opcion == "2":
            ejecutar_listar(catalogo)
        elif opcion == "3":
            ejecutar_filtrar(catalogo)
        elif opcion == "4":
            ejecutar_recorridos(arbol)
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, probá de nuevo.")

        print()  # línea en blanco antes de repetir el menú