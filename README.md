# Juegoteca

Sistema de consola para explorar videojuegos de Steam: buscar por nombre, navegar por categorías,
ver cuánto se suele jugar cada título y comparar tiempos. Usa datos reales del **Steam Games Dataset**.

Está pensado para un jugador que quiere decidir a qué jugar sabiendo cuánto tiempo le va a llevar.
Proyecto integrador de Estructuras de Datos (UNAB, Comisión 3, Grupo 10).

## Integrantes

- Rodrigo Cruz Choque
- Ian Martinez
- Milagros Ponce

## Cómo ejecutar

Requiere **Python 3.10 o superior**. No hay que instalar nada más.

```bash
git clone https://github.com/cartonero/tpi_integrador-.git
cd tpi_integrador-
py main.py
```

En Linux o macOS se usa `python3` en lugar de `py`.

Los scripts de `algoritmos/` se ejecutan **como módulo, desde la carpeta raíz**:

```bash
py -m algoritmos.probar_bst
py -m algoritmos.probar_avl
py -m algoritmos.comparar_bst_avl
```

## Qué se puede hacer (menú)

| Opción | Qué hace | Estructura que usa |
|---|---|---|
| 1 | Buscar un juego por nombre | AVL |
| 2 | Listar el catálogo, de a 20 por página | Lista del catálogo |
| 3 | Filtrar por categoría | Lista del catálogo |
| 4 | Ver los recorridos inorder, preorder y postorder | BST |
| 5 | Explorar categorías (navegar, ver el árbol, ver por niveles) | Árbol general |
| 6 | Mostrar la duración estimada de un juego | AVL |
| 7 | Comparar el tiempo de juego de dos o más juegos | AVL |
| 8 | Añadir un juego nuevo (solo en memoria, durante la sesión) | Catálogo, BST y AVL |

La **duración estimada** es el tiempo de juego promedio de los jugadores en Steam. No es el tiempo
necesario para terminar el juego. En la muestra, solo 555 de 2000 juegos tienen ese dato.

## Cómo está organizado el código

| Carpeta | Contenido |
|---|---|
| `modelos/` | Clases del dominio: `Juego` y `Catalogo` |
| `estructuras/` | `ArbolBST`, `AVL` y `ArbolGeneral` |
| `servicios/` | Carga de datos, jerarquía de categorías y reglas para añadir y comparar juegos |
| `ui/` | Menú y pantallas de la terminal |
| `algoritmos/` | Scripts para preparar datos, probar las estructuras y medir tiempos |
| `datos/` | `games.json`: muestra de 2000 juegos del dataset |
| `docs/` | Documentación del proyecto |

La carpeta `lux/` contiene el dataset completo (cerca de 900 MB). No se sube a GitHub.

## Documentación

Conviene leerla en este orden:

1. [Propuesta (TP0)](docs/00-propuesta.md): qué problema resuelve y para quién.
2. [Requerimientos](docs/01-requerimientos.md): qué debe hacer el sistema.
3. [Casos de uso](docs/02-casos-de-uso.md): cómo lo usa una persona.
4. [Diagrama de clases](docs/03-diagrama-clases.md): qué clases hay y cómo se relacionan.
5. [Conexión entre estructuras](docs/04-diagrama-datos.md): cómo viajan los datos por el sistema.
6. [Gestión del proyecto](docs/05-gestion-proyecto.md): tablero, sprints y retrospectivas.
7. [Análisis TP3: BST](docs/07-analisis-tp3.md) y [Análisis TP4 y TP5: AVL y árbol general](docs/08-analisis-tp4-tp5.md).

## Estado del proyecto

| TP | Tema | Estado |
|---|---|---|
| TP0 | Propuesta y repositorio | ✅ |
| TP1 | Modelo de clases y terminal | ✅ |
| TP2 | Análisis de algoritmos | ✅ |
| TP3 | Árbol binario de búsqueda | ✅ |
| TP4 | Árbol AVL | ✅ |
| TP5 | Árbol general | ✅ |
| TP6 en adelante | Heap, grafo, recorridos, caminos mínimos, recomendador | ⏳ |
