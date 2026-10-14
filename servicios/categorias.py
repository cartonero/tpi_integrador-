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
"""
from estructuras.arbol_general import ArbolGeneral

# Grupo -> géneros que contiene (según la clasificación de Steam).
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


def construir_arbol_categorias(catalogo):
    """Devuelve un ArbolGeneral con la jerarquía de categorías.

    Si el catálogo tiene algún género que no figura en GRUPOS (por ejemplo,
    si se agregan juegos nuevos), se cuelga de un grupo extra llamado "Otros"
    para que no se pierda ninguna categoría.
    """
    arbol = ArbolGeneral()
    raiz = arbol.insertar_raiz("Juegoteca")

    conocidos = set()
    for grupo, generos in GRUPOS.items():
        nodo_grupo = arbol.agregar_hijo(raiz, grupo)
        for genero in generos:
            arbol.agregar_hijo(nodo_grupo, genero)
            conocidos.add(genero)

    generos_catalogo = {g for juego in catalogo.listar() for g in juego.get_generos()}
    otros = sorted(generos_catalogo - conocidos)
    if otros:
        nodo_otros = arbol.agregar_hijo(raiz, "Otros")
        for genero in otros:
            arbol.agregar_hijo(nodo_otros, genero)

    return arbol