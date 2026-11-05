"""
servicios/categorias.py — Jerarquía de categorías de Juegoteca (TP5).

Arma el ÁRBOL GENERAL (n-ario) con la forma en que Steam agrupa sus géneros:

    Juegoteca
    ├── Juegos                    (10 géneros jugables)
    ├── Modalidad de acceso       (2)
    ├── Software y herramientas   (10)
    └── Contenido para adultos    (4)

Se usa un árbol general (y no uno binario) porque cada grupo tiene una
cantidad distinta de hijos: 10, 2, 10 y 4.

Los nodos del árbol guardan solo NOMBRES de categorías (texto), no juegos.
Para saber qué juegos tiene un género, el menú le pregunta al Catalogo
(filtrar_por_categoria). Este módulo se usa en la opción "Explorar categorías" y
para validar los géneros al añadir un juego (opción 8).
"""
from estructuras.arbol_general import ArbolGeneral

# Define la jerarquía: grupo -> géneros que contiene (según Steam).
# Es un diccionario común de Python; cada clave es un grupo (nodo de nivel 1)
# y su lista contiene los géneros (nodos de nivel 2, las hojas del árbol).
# Para cambiar o ampliar la jerarquía solo hay que editar este diccionario.
GRUPOS = {
    "Juegos": [
        "Action", "Adventure", "Casual", "Indie", "RPG",
        "Simulation", "Strategy", "Sports", "Racing", "Massively Multiplayer",
    ],
    "Modalidad de acceso": [
        "Early Access", "Free To Play",
    ],
    "Software y herramientas": [
        "Utilities", "Audio Production", "Game Development", "Photo Editing",
        "Design & Illustration", "Animation & Modeling", "Video Production",
        "Software Training", "Education", "Web Publishing",
    ],
    "Contenido para adultos": [
        "Violent", "Gore", "Nudity", "Sexual Content",
    ],
}


def generos_validos():
    """Devuelve la lista de todos los géneros de la jerarquía (los de GRUPOS), en orden.

    Son los únicos géneros que se aceptan al añadir un juego nuevo.
    """
    # Recorre cada lista de géneros de cada grupo y las junta en una sola lista.
    return [genero for generos in GRUPOS.values() for genero in generos]


def construir_arbol_categorias(catalogo):
    """Devuelve un ArbolGeneral con la jerarquía de categorías.

    Si el catálogo tiene algún género que no figura en GRUPOS (por ejemplo,
    si se agregan juegos nuevos), se cuelga de un grupo extra llamado "Otros"
    para que no se pierda ninguna categoría.
    """
    arbol = ArbolGeneral()

    # Paso 1: la raíz del árbol (nivel 0).
    raiz = arbol.insertar_raiz("Juegoteca")

    # Paso 2: por cada grupo creamos un hijo de la raíz (nivel 1) y, colgando
    # de él, un hijo por cada género (nivel 2). Mientras tanto anotamos en
    # "conocidos" todos los géneros que ya quedaron ubicados en el árbol.
    conocidos = set()
    for grupo, generos in GRUPOS.items():
        nodo_grupo = arbol.agregar_hijo(raiz, grupo)
        for genero in generos:
            arbol.agregar_hijo(nodo_grupo, genero)
            conocidos.add(genero)

    # Paso 3: buscamos géneros que existan en el catálogo pero no estén en
    # GRUPOS. Se arma un conjunto con todos los géneros de todos los juegos
    # y se le resta el conjunto de los conocidos.
    generos_catalogo = {g for juego in catalogo.listar() for g in juego.get_generos()}
    otros = sorted(generos_catalogo - conocidos)

    # Paso 4: si sobró alguno, se agrupan bajo "Otros" para no perderlos.
    # Con los datos actuales este grupo no se crea (los 26 géneros están en GRUPOS).
    if otros:
        nodo_otros = arbol.agregar_hijo(raiz, "Otros")
        for genero in otros:
            arbol.agregar_hijo(nodo_otros, genero)

    return arbol