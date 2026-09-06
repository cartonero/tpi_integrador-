def mostrar_menu():
    print("=" * 40)
    print(" JUEGOTECA — TERMINAL")
    print("=" * 40)
    print("1. Buscar juego")
    print("2. Listar juegos")
    print("3. Filtrar por categoría")
    print("0. Salir")
    print("-" * 40)


def ejecutar_buscar(catalogo):
    nombre = input("Nombre del juego: ").strip()
    juego = catalogo.buscar(nombre)
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


def iniciar(catalogo):
    while True:
        mostrar_menu()
        opcion = input("Opción: ").strip()

        if opcion == "1":
            ejecutar_buscar(catalogo)
        elif opcion == "2":
            ejecutar_listar(catalogo)
        elif opcion == "3":
            ejecutar_filtrar(catalogo)
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, probá de nuevo.")

        print()  # línea en blanco antes de repetir el menú