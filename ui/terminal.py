"""
ui/terminal.py — Interfaz de terminal (menú) de Juegoteca.

Este módulo es la CAPA DE INTERFAZ: se encarga solo de mostrar menús, leer
lo que escribe el usuario (input) y mostrar resultados (print). No guarda
datos ni implementa árboles: recibe las estructuras ya construidas por
main.py y les hace consultas.

Estructuras que usa cada opción del menú:
    1. Buscar juego            -> AVL (búsqueda por nombre, O(log n))
    2. Listar juegos           -> Catalogo (lista completa, paginada)
    3. Filtrar por categoría   -> Catalogo (recorre la lista)
    4. Ver recorridos del BST  -> BST (inorder, preorder, postorder)
    5. Explorar categorías     -> Árbol general (grupos de Steam -> géneros)
    6. Mostrar duración        -> AVL (busca el juego) y su tiempo de juego
    7. Comparar tiempo de juego -> AVL (busca cada juego) y los ordena por tiempo
    8. Añadir un juego         -> Catalogo, BST y AVL (se insertan los tres)

Convención: las funciones que empiezan con guion bajo (_formatear_juego,
_navegar_generos, ...) son auxiliares internas de este módulo; las demás
las usa el menú principal.
"""
import textwrap

from servicios.categorias import generos_validos
from servicios.juegos import (
    formatear_duracion,
    comparar_tiempos,
    parsear_generos,
    horas_a_minutos,
    agregar_juego,
)


# ==================== MENÚ PRINCIPAL ====================

def mostrar_menu():
    """Imprime las opciones del menú principal."""
    print("=" * 40)  # "=" * 40 repite el carácter 40 veces: una línea separadora
    print(" JUEGOTECA — TERMINAL")
    print("=" * 40)
    print("1. Buscar juego")
    print("2. Listar juegos")
    print("3. Filtrar por categoría")
    print("4. Ver recorridos del BST (inorder / preorder / postorder)")
    print("5. Explorar categorías")
    print("6. Mostrar duración estimada de un juego")
    print("7. Comparar tiempo de juego de dos o más juegos")
    print("8. Añadir un juego")
    print("0. Salir")
    print("-" * 40)


# ==================== OPCIÓN 1: BUSCAR (AVL) ====================

def _buscar_juego(avl, nombre):
    """Busca un juego por nombre en el AVL. Devuelve el Juego o None.

    El árbol compara en minúsculas, así que se le pasa el nombre en minúsculas.
    El parámetro "clave" es la MISMA función con la que se insertaron los
    juegos en main.py (nombre en minúsculas): el árbol la usa en cada nodo
    para decidir si seguir por la izquierda (menor) o por la derecha (mayor).
    """
    return avl.buscar(nombre.lower(), clave=lambda j: j.get_nombre().lower())


def ejecutar_buscar(avl):
    """Busca usando el ÁRBOL AVL (TP4).

    Evolución de esta opción:
      - TP1: recorría toda la lista del catálogo: O(n).
      - TP3: BST, O(log n) en promedio pero O(n) si se desbalancea.
      - TP4: AVL, O(log n) garantizado porque se auto-balancea con rotaciones.
    """
    nombre = input("Nombre del juego: ").strip()  # strip() saca espacios de los bordes
    juego = _buscar_juego(avl, nombre)

    # buscar() devuelve el Juego encontrado o None si no existe.
    if juego is None:
        print(f"No se encontró ningún juego llamado '{nombre}'.")
    else:
        print(juego)


# ==================== OPCIÓN 2: LISTAR (CON PAGINADO) ====================

def ejecutar_listar(catalogo):
    """Muestra todos los juegos de a 20 por pantalla (paginado)."""
    juegos = catalogo.listar()
    if not juegos:
        print("El catálogo está vacío.")
        return

    tamano_pagina = 20  # cuántos juegos se muestran por vez
    inicio = 0          # posición del primer juego de la página actual

    while inicio < len(juegos):
        # Slicing: juegos[a:b] toma los elementos desde la posición a hasta b-1.
        pagina = juegos[inicio:inicio + tamano_pagina]
        for juego in pagina:
            print(juego)

        # Avanzamos a la página siguiente.
        inicio += tamano_pagina

        # Si todavía quedan juegos, preguntamos si seguir o volver al menú.
        if inicio < len(juegos):
            seguir = input(
                f"\nMostrados {inicio} de {len(juegos)}. "
                "Enter para ver más, 'q' para volver al menú: "
            ).strip().lower()
            if seguir == "q":
                break


# ==================== OPCIÓN 3: FILTRAR POR CATEGORÍA ====================

def ejecutar_filtrar(catalogo):
    """Muestra los juegos que pertenecen a una categoría (género) escrita por el usuario."""
    categoria = input("Categoría a buscar (ej: Action, Indie, RPG): ").strip()

    # El filtrado lo hace el Catalogo (recorre la lista y compara géneros).
    resultados = catalogo.filtrar_por_categoria(categoria)
    if not resultados:
        print(f"No se encontraron juegos en la categoría '{categoria}'.")
        return

    # Se muestran solo los primeros 20 para no llenar la pantalla.
    print(f"\n{len(resultados)} juego(s) encontrados:")
    for juego in resultados[:20]:
        print(juego)
    if len(resultados) > 20:
        print(f"... y {len(resultados) - 20} más.")


# ==================== FORMATO DE LÍNEAS ====================

def _recortar(texto, ancho):
    """Corta el texto si es más largo que `ancho` y le agrega '...' al final."""
    # Se le resta 3 al ancho para que entren los tres puntos.
    if len(texto) > ancho:
        return texto[:ancho - 3] + "..."
    return texto


def _formatear_juego(indice, juego, ancho_nombre=45):
    """Formatea una línea 'N. Nombre (Categoría)' con el nombre truncado
    si es muy largo, para que la lista quede alineada en la terminal."""
    # Si el nombre es más largo que el ancho permitido, se corta con "...".
    nombre = _recortar(juego.get_nombre(), ancho_nombre)

    # Formato de la línea:
    #   {indice:>2}              -> número alineado a la derecha, 2 de ancho
    #   {nombre:<{ancho_nombre}} -> nombre alineado a la izquierda, rellenado
    #                               con espacios hasta el ancho indicado
    return f"  {indice:>2}. {nombre:<{ancho_nombre}} ({juego.get_categoria_principal()})"


# ==================== OPCIÓN 4: RECORRIDOS DEL BST ====================

def ejecutar_recorridos(bst, avl):
    """Muestra los 3 recorridos del BST (TP3), limitados a 15 elementos,
    y compara la altura del BST contra la del AVL (TP4)."""
    # Cada recorrido devuelve una lista con TODOS los juegos del árbol
    # (2000), pero mostramos solo los primeros 15 con [:15].
    # enumerate(..., start=1) numera las líneas desde 1.

    # INORDER (izquierda -> raíz -> derecha): sale ORDENADO alfabéticamente.
    print("\n--- INORDER (ordenado alfabéticamente) ---")
    for i, juego in enumerate(bst.inorder()[:15], start=1):
        print(_formatear_juego(i, juego))

    # PREORDER (raíz -> izquierda -> derecha): primero el nodo, después sus
    # hijos. Sirve para ver la forma del árbol: el primero es la raíz.
    print("\n--- PREORDER ---")
    for i, juego in enumerate(bst.preorder()[:15], start=1):
        print(_formatear_juego(i, juego))

    # POSTORDER (izquierda -> derecha -> raíz): primero los hijos y al
    # final el nodo. Los primeros que salen son hojas.
    print("\n--- POSTORDER ---")
    for i, juego in enumerate(bst.postorder()[:15], start=1):
        print(_formatear_juego(i, juego))

    print("\n(Se muestran los primeros 15 de cada recorrido.)")

    # Comparación de alturas: con los mismos juegos, el AVL queda más bajo
    # (más balanceado) que el BST, y por eso busca más rápido.
    print(f"Altura del BST: {bst.altura()} | Altura del AVL: {avl.altura()} "
          f"(el AVL se balancea solo con rotaciones)")


# ==================== OPCIÓN 5: EXPLORAR CATEGORÍAS (TP5, árbol general) ====================
# La jerarquía tiene 3 niveles:  Juegoteca (raíz) -> grupos -> géneros.
# Las funciones de abajo bajan de a un nivel: primero se elige un grupo
# (_navegar_categorias), después un género (_navegar_generos) y por último se
# muestran los juegos de ese género (_mostrar_juegos_de_genero).

def _contar_juegos(catalogo, genero):
    """Cantidad de juegos del catálogo que tienen ese género."""
    return len(catalogo.filtrar_por_categoria(genero))


def _texto_juegos(cantidad):
    """'1 juego' / '5 juegos' (singular o plural según la cantidad)."""
    return f"{cantidad} juego" if cantidad == 1 else f"{cantidad} juegos"


def _elegir_nodo(nodos, texto):
    """Devuelve el nodo elegido por número (1..N), o None si no es válido."""
    # isdigit() es True solo si el texto son únicamente dígitos ("3" sí, "x" no).
    if not texto.isdigit():
        return None
    indice = int(texto)
    # El usuario ve la lista numerada desde 1, pero la lista de Python
    # empieza en 0: por eso se accede con indice - 1.
    if 1 <= indice <= len(nodos):
        return nodos[indice - 1]
    return None


def _mostrar_juegos_de_genero(genero, catalogo, maximo=20):
    """Lista los juegos de un género (hasta `maximo`) usando el catálogo."""
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

        # grupo.hijos es la lista de nodos hijos del grupo en el árbol general:
        # cada hijo es un género. Mostramos cuántos juegos tiene cada uno.
        for i, genero in enumerate(grupo.hijos, start=1):
            cantidad = _contar_juegos(catalogo, genero.dato)
            print(f"  {i:>2}. {genero.dato:<25} {_texto_juegos(cantidad):>12}")

        eleccion = input("Elegí un género para ver sus juegos (0 para volver): ").strip()
        if eleccion == "0":
            return  # vuelve al nivel de los grupos
        genero = _elegir_nodo(grupo.hijos, eleccion)
        if genero is None:
            print("Opción inválida, probá de nuevo.")
            continue  # vuelve a mostrar la lista de géneros
        _mostrar_juegos_de_genero(genero.dato, catalogo)


def _navegar_categorias(arbol_categorias, catalogo):
    """Primer nivel: los grupos (hijos de la raíz del árbol general)."""
    # Los hijos de la raíz son los 4 grupos (Juegos, Modalidad de acceso, ...).
    grupos = arbol_categorias.raiz.hijos
    while True:
        print("\n--- GRUPOS DE CATEGORÍAS ---")
        for i, grupo in enumerate(grupos, start=1):
            print(f"  {i}. {grupo.dato} ({len(grupo.hijos)} géneros)")

        eleccion = input("Elegí un grupo (0 para volver): ").strip()
        if eleccion == "0":
            return  # vuelve al submenú de Explorar categorías
        grupo = _elegir_nodo(grupos, eleccion)
        if grupo is None:
            print("Opción inválida, probá de nuevo.")
            continue
        _navegar_generos(grupo, catalogo)  # baja un nivel: los géneros del grupo


def _imprimir_arbol(nodo, catalogo, nivel=0):
    """Recorrido en PROFUNDIDAD (preorder): imprime el nodo y después sus
    hijos, con sangría según el nivel. Las hojas (géneros) muestran cuántos
    juegos tienen."""
    # Sangría: 4 espacios por cada nivel de profundidad (raíz = 0 espacios).
    sangria = "    " * nivel

    # Una HOJA es un nodo sin hijos. Las hojas son los géneros, así que
    # mostramos cuántos juegos tienen. (nivel > 0 evita tratar la raíz
    # como hoja si el árbol estuviera vacío de hijos.)
    if not nodo.hijos and nivel > 0:
        cantidad = _contar_juegos(catalogo, nodo.dato)
        print(f"{sangria}- {nodo.dato} ({_texto_juegos(cantidad)})")
    else:
        print(f"{sangria}{nodo.dato}")

    # RECURSIÓN: la función se llama a sí misma para cada hijo, uno nivel
    # más abajo. Así se recorre el árbol entero: nodo, luego su primer hijo
    # completo (con todos sus descendientes), luego el segundo, etc.
    for hijo in nodo.hijos:
        _imprimir_arbol(hijo, catalogo, nivel + 1)


def _imprimir_por_niveles(arbol_categorias):
    """Recorrido en AMPLITUD (BFS): nivel por nivel, de arriba hacia abajo."""
    # obtener_niveles() devuelve una lista de listas:
    # [[raíz], [los 4 grupos], [los 26 géneros]]
    for i, nivel in enumerate(arbol_categorias.obtener_niveles()):
        print(f"\nNivel {i}:")
        # textwrap.fill parte el texto en renglones de hasta 70 caracteres
        # para que la lista larga de géneros no se salga de la pantalla.
        print(textwrap.fill(", ".join(nivel), width=70,
                            initial_indent="  ", subsequent_indent="  "))


def ejecutar_explorar_categorias(arbol_categorias, catalogo):
    """Explorar categorías (TP5): usa el ÁRBOL GENERAL con la jerarquía de
    categorías (grupos de Steam -> géneros)."""
    # Submenú con su propio bucle: se repite hasta que el usuario elige 0.
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
            return  # sale de esta función y vuelve al menú principal
        else:
            print("Opción inválida, probá de nuevo.")


# ==================== OPCIÓN 6: MOSTRAR DURACIÓN (F5) ====================

def ejecutar_duracion(avl):
    """Muestra la duración estimada de un juego.

    La duración es el tiempo de juego PROMEDIO que registra Steam, no el
    tiempo que lleva completarlo. Muchos juegos no tienen ese dato.
    """
    nombre = input("Nombre del juego: ").strip()
    juego = _buscar_juego(avl, nombre)  # búsqueda O(log n) en el AVL

    if juego is None:
        print(f"No se encontró ningún juego llamado '{nombre}'.")
    elif not juego.tiene_tiempo():
        print(f"{juego.get_nombre()}: no hay datos de duración para este juego.")
    else:
        print(f"{juego.get_nombre()}: duración estimada "
              f"{formatear_duracion(juego.get_tiempo_min())} "
              "(tiempo de juego promedio en Steam)")


# ==================== OPCIÓN 7: COMPARAR TIEMPO DE JUEGO (F3) ====================

def _linea_comparacion(posicion, juego, minutos_base, ancho_nombre=40):
    """Una línea del ranking: posición, nombre, tiempo y diferencia con el más corto."""
    nombre = _recortar(juego.get_nombre(), ancho_nombre)
    tiempo = formatear_duracion(juego.get_tiempo_min())

    # Diferencia respecto del juego MÁS CORTO (el primero de la lista ordenada).
    diferencia = juego.get_tiempo_min() - minutos_base
    if posicion == 1:
        extra = "(el más corto)"
    elif diferencia == 0:
        extra = "(igual que el más corto)"
    else:
        extra = f"(+{formatear_duracion(diferencia)})"

    return f"  {posicion:>2}. {nombre:<{ancho_nombre}} {tiempo:>12}  {extra}"


def ejecutar_comparar(avl):
    """Compara el tiempo de juego de dos o más juegos.

    Los nombres se piden de a uno por línea (y no separados por coma)
    porque algunos nombres de juegos llevan comas, por ejemplo
    "Ready, Steady, Ship!".
    """
    print("Ingresá los juegos a comparar, uno por línea.")
    print("Enter vacío para terminar (mínimo 2 juegos).")

    juegos = []  # juegos encontrados, sin repetir
    while True:
        numero = len(juegos) + 1
        # Del tercer juego en adelante se avisa cómo terminar.
        pedido = f"Juego {numero}: " if numero <= 2 else f"Juego {numero} (Enter para terminar): "
        nombre = input(pedido).strip()

        if nombre == "":
            break  # Enter vacío: terminó de cargar nombres

        juego = _buscar_juego(avl, nombre)  # búsqueda O(log n) en el AVL
        if juego is None:
            print(f"  No se encontró ningún juego llamado '{nombre}'. Probá con otro.")
        elif juego in juegos:
            # El AVL devuelve siempre el mismo objeto para el mismo nombre,
            # así que "in" detecta si ya lo habíamos ingresado.
            print(f"  '{juego.get_nombre()}' ya está en la comparación.")
        else:
            juegos.append(juego)

    if len(juegos) < 2:
        print("Hacen falta al menos 2 juegos para comparar.")
        return

    # La lógica de ordenar y separar está en servicios/juegos.py.
    con_datos, sin_datos = comparar_tiempos(juegos)

    if len(con_datos) < 2:
        print("\nNo se puede comparar: hacen falta al menos 2 juegos con datos de duración.")
    else:
        print("\n--- COMPARACIÓN DE TIEMPO DE JUEGO (de menor a mayor) ---")
        minutos_base = con_datos[0].get_tiempo_min()
        for i, juego in enumerate(con_datos, start=1):
            print(_linea_comparacion(i, juego, minutos_base))

        mas_corto, mas_largo = con_datos[0], con_datos[-1]
        if mas_corto.get_tiempo_min() == mas_largo.get_tiempo_min():
            print("\nTodos tienen el mismo tiempo de juego.")
        else:
            print(f"\nEl más corto es {mas_corto.get_nombre()} "
                  f"y el más largo es {mas_largo.get_nombre()}.")

    # Los juegos sin dato no entran en el ranking, pero se avisa cuáles son.
    if sin_datos:
        nombres = ", ".join(j.get_nombre() for j in sin_datos)
        print(f"Sin datos de duración (no se pueden comparar): {nombres}")


# ==================== OPCIÓN 8: AÑADIR UN JUEGO (F2) ====================

def ejecutar_agregar(catalogo, bst, avl):
    """Añade un juego nuevo al catálogo y a los dos árboles.

    Los juegos añadidos viven solo en memoria: se pierden al cerrar el
    programa (datos/games.json no se modifica).
    """
    print("--- AÑADIR UN JUEGO ---")
    nombre = input("Nombre del juego (Enter vacío para cancelar): ").strip()
    if nombre == "":
        print("Cancelado.")
        return

    # Aviso temprano: si el nombre ya existe no hace falta pedir lo demás.
    existente = _buscar_juego(avl, nombre)  # búsqueda O(log n) en el AVL
    if existente is not None:
        print(f"Ya existe un juego llamado '{existente.get_nombre()}'.")
        return

    # Géneros: solo se aceptan los de la jerarquía de categorías. Se repite
    # hasta que todos los que escribió sean válidos.
    validos = generos_validos()
    print("Géneros disponibles:")
    print(textwrap.fill(", ".join(validos), width=70,
                        initial_indent="  ", subsequent_indent="  "))
    while True:
        entrada = input("Géneros (separados por coma, Enter vacío para cancelar): ")
        if entrada.strip() == "":
            print("Cancelado.")
            return
        generos, invalidos = parsear_generos(entrada, validos)
        if invalidos:
            print(f"  Géneros no válidos: {', '.join(invalidos)}. Probá de nuevo.")
        elif not generos:
            print("  Hace falta al menos un género.")  # por ejemplo si solo escribió comas
        else:
            break

    # Duración: es opcional. Enter vacío significa "no la sé" (sin datos).
    while True:
        entrada = input("Duración en horas (Enter si no la sabés): ")
        try:
            minutos = horas_a_minutos(entrada)
            break
        except ValueError as error:
            print(f"  {error}")

    # La lógica de alta (catálogo + BST + AVL) está en servicios/juegos.py.
    try:
        juego = agregar_juego(nombre, generos, minutos, catalogo, bst, avl)
    except ValueError as error:
        print(error)
        return

    print(f"\nSe agregó '{juego.get_nombre()}' ({', '.join(generos)}), "
          f"duración: {formatear_duracion(minutos)}.")
    print(f"El catálogo tiene ahora {catalogo.cantidad()} juegos. "
          f"Altura del AVL: {avl.altura()}.")


# ==================== BUCLE PRINCIPAL ====================

def iniciar(catalogo, bst, avl, arbol_categorias):
    """Bucle principal del programa: muestra el menú y ejecuta la opción elegida.

    Recibe las estructuras ya construidas (las arma main.py) y se las pasa a
    la función que corresponde a cada opción.
    """
    while True:  # se repite hasta que el usuario elige "0. Salir"
        mostrar_menu()
        opcion = input("Opción: ").strip()

        # Despachamos según la opción elegida.
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
        elif opcion == "6":
            ejecutar_duracion(avl)
        elif opcion == "7":
            ejecutar_comparar(avl)
        elif opcion == "8":
            ejecutar_agregar(catalogo, bst, avl)
        elif opcion == "0":
            print("¡Hasta luego!")
            break  # corta el while True y termina el programa
        else:
            print("Opción inválida, probá de nuevo.")

        print()  # línea en blanco antes de repetir el menú