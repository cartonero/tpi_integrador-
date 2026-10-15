import textwrap


def mostrar_menu():
    print("=" * 40)
    print(" JUEGOTECA — TERMINAL")
    print("=" * 40)
    print("1. Buscar juego")
    print("2. Listar juegos")
    print("3. Filtrar por categoría")
    print("4. Ver recorridos del BST (inorder / preorder / postorder)")
    print("5. Explorar categorías")
    print("0. Salir")
    print("-" * 40)


def ejecutar_buscar(avl):
    """Busca usando el ÁRBOL AVL (TP4).

    Evolución de esta opción:
      - TP1: recorría toda la lista del catálogo: O(n).
      - TP3: BST, O(log n) en promedio pero O(n) si se desbalancea.
      - TP4: AVL, O(log n) garantizado porque se auto-balancea con rotaciones.
    """
    nombre = input("Nombre del juego: ").strip()
    juego = avl.buscar(nombre.lower(), clave=lambda j: j.get_nombre().lower())
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


def ejecutar_recorridos(bst, avl):
    """Muestra los 3 recorridos del BST (TP3), limitados a 15 elementos,
    y compara la altura del BST contra la del AVL (TP4)."""
    print("\n--- INORDER (ordenado alfabéticamente) ---")
    for i, juego in enumerate(bst.inorder()[:15], start=1):
        print(_formatear_juego(i, juego))

    print("\n--- PREORDER ---")
    for i, juego in enumerate(bst.preorder()[:15], start=1):
        print(_formatear_juego(i, juego))

    print("\n--- POSTORDER ---")
    for i, juego in enumerate(bst.postorder()[:15], start=1):
        print(_formatear_juego(i, juego))

    print("\n(Se muestran los primeros 15 de cada recorrido.)")
    print(f"Altura del BST: {bst.altura()} | Altura del AVL: {avl.altura()} "
          f"(el AVL se balancea solo con rotaciones)")


# ==================== EXPLORAR CATEGORÍAS (TP5, árbol general) ====================

def _contar_juegos(catalogo, genero):
    return len(catalogo.filtrar_por_categoria(genero))


def _texto_juegos(cantidad):
    """'1 juego' / '5 juegos' (singular o plural según la cantidad)."""
    return f"{cantidad} juego" if cantidad == 1 else f"{cantidad} juegos"


def _elegir_nodo(nodos, texto):
    """Devuelve el nodo elegido por número (1..N), o None si no es válido."""
    if not texto.isdigit():
        return None
    indice = int(texto)
    if 1 <= indice <= len(nodos):
        return nodos[indice - 1]
    return None


def _mostrar_juegos_de_genero(genero, catalogo, maximo=20):
    juegos = catalogo.filtrar_por_categoria(genero)
    if not juegos:
        print(f"\nNo hay juegos de '{genero}' en el catálogo.")
        return

    print(f"\n{len(juegos)} juego(s) de '{genero}':")
    for i, juego in enumerate(juegos[:maximo], start=1):
        print(_formatear_juego(i, juego))
    if len(juegos) > maximo:
        print(f"... y {len(juegos) - maximo} más.")


def _navegar_generos(grupo, catalogo):
    """Segundo nivel: los géneros (hijos) de un grupo."""
    while True:
        print(f"\n--- {grupo.dato.upper()} ---")
        for i, genero in enumerate(grupo.hijos, start=1):
            cantidad = _contar_juegos(catalogo, genero.dato)
            print(f"  {i:>2}. {genero.dato:<25} {_texto_juegos(cantidad):>12}")

        eleccion = input("Elegí un género para ver sus juegos (0 para volver): ").strip()
        if eleccion == "0":
            return
        genero = _elegir_nodo(grupo.hijos, eleccion)
        if genero is None:
            print("Opción inválida, probá de nuevo.")
            continue
        _mostrar_juegos_de_genero(genero.dato, catalogo)


def _navegar_categorias(arbol_categorias, catalogo):
    """Primer nivel: los grupos (hijos de la raíz del árbol general)."""
    grupos = arbol_categorias.raiz.hijos
    while True:
        print("\n--- GRUPOS DE CATEGORÍAS ---")
        for i, grupo in enumerate(grupos, start=1):
            print(f"  {i}. {grupo.dato} ({len(grupo.hijos)} géneros)")

        eleccion = input("Elegí un grupo (0 para volver): ").strip()
        if eleccion == "0":
            return
        grupo = _elegir_nodo(grupos, eleccion)
        if grupo is None:
            print("Opción inválida, probá de nuevo.")
            continue
        _navegar_generos(grupo, catalogo)


def _imprimir_arbol(nodo, catalogo, nivel=0):
    """Recorrido en PROFUNDIDAD (preorder): imprime el nodo y después sus
    hijos, con sangría según el nivel. Las hojas (géneros) muestran cuántos
    juegos tienen."""
    sangria = "    " * nivel
    if not nodo.hijos and nivel > 0:
        cantidad = _contar_juegos(catalogo, nodo.dato)
        print(f"{sangria}- {nodo.dato} ({_texto_juegos(cantidad)})")
    else:
        print(f"{sangria}{nodo.dato}")
    for hijo in nodo.hijos:
        _imprimir_arbol(hijo, catalogo, nivel + 1)


def _imprimir_por_niveles(arbol_categorias):
    """Recorrido en AMPLITUD (BFS): nivel por nivel, de arriba hacia abajo."""
    for i, nivel in enumerate(arbol_categorias.obtener_niveles()):
        print(f"\nNivel {i}:")
        print(textwrap.fill(", ".join(nivel), width=70,
                            initial_indent="  ", subsequent_indent="  "))


def ejecutar_explorar_categorias(arbol_categorias, catalogo):
    """Explorar categorías (TP5): usa el ÁRBOL GENERAL con la jerarquía de
    categorías (grupos de Steam -> géneros)."""
    while True:
        print("\n--- EXPLORAR CATEGORÍAS ---")
        print("1. Navegar por grupos y géneros")
        print("2. Ver el árbol completo (recorrido en profundidad)")
        print("3. Ver el árbol por niveles (recorrido en amplitud)")
        print("0. Volver al menú principal")

        opcion = input("Opción: ").strip()
        if opcion == "1":
            _navegar_categorias(arbol_categorias, catalogo)
        elif opcion == "2":
            print()
            _imprimir_arbol(arbol_categorias.raiz, catalogo)
        elif opcion == "3":
            _imprimir_por_niveles(arbol_categorias)
        elif opcion == "0":
            return
        else:
            print("Opción inválida, probá de nuevo.")


def iniciar(catalogo, bst, avl, arbol_categorias):
    while True:
        mostrar_menu()
        opcion = input("Opción: ").strip()

        if opcion == "1":
            ejecutar_buscar(avl)
        elif opcion == "2":
            ejecutar_listar(catalogo)
        elif opcion == "3":
            ejecutar_filtrar(catalogo)
        elif opcion == "4":
            ejecutar_recorridos(bst, avl)
        elif opcion == "5":
            ejecutar_explorar_categorias(arbol_categorias, catalogo)
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, probá de nuevo.")

        print()  # línea en blanco antes de repetir el menú