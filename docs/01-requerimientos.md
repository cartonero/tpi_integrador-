# Juegoteca — Propuesta (TP0)

Sistema de recomendación de videojuegos que ayuda a un jugador a decidir qué
jugar a continuación, teniendo en cuenta el tiempo estimado que le llevará
completarlo.

## 1. Nombre del proyecto y dominio elegido (con justificación)

**Nombre:** Juegoteca

**Dominio:** Videojuegos.

**Justificación:** Decidimos centrarnos en el universo de los videojuegos
porque Steam tiene a libre disposición una base de datos acerca de los
productos (videojuegos) de la plataforma, lo que nos da datos reales y
suficientes para toda la cursada. El dominio permite ordenar por nombre o
rating (BST/AVL), agrupar por categoría/género (árbol general), rankear por
tiempo de juego o rating (heap) y relacionar juegos entre sí (grafo).

## 2. Problema que resuelve y usuario objetivo

**Problema:** Un jugador tiene a disposición una enorme cantidad de
videojuegos y no sabe cuál elegir, ni cuánto tiempo real le va a insumir
completarlo.

**Usuario objetivo:** Videojugadores/gamers que buscan recomendaciones de
videojuegos, teniendo a su disposición los tiempos estimados en completarlos
para tener una mejor noción del contenido y el tiempo que invertirán.

## 3. Funcionalidades iniciales

| ID | Funcionalidad |
|---|---|
| F1 | Buscar juego (por nombre) |
| F2 | Añadir juegos (al catálogo) |
| F3 | Comparar tiempo de juego (entre dos o más juegos) |
| F4 | Explorar categorías (géneros, jerarquía) |
| F5 | Mostrar duración del juego (estimada) |

## 4. Boceto de la interfaz de terminal

\`\`\`text
========================================
 JUEGOTECA — TERMINAL
========================================
1. Buscar juego
2. Añadir juegos
3. Comparar tiempo de juego
4. Explorar categorías
5. Mostrar duración del juego (estimada)
0. Salir
----------------------------------------
Opción: 1
Nombre del juego: Hollow Knight

╔══════════════════════════════════════╗
║ 🎮 JUEGOTECA                          ║
╠══════════════════════════════════════╣
║ HOLLOW KNIGHT                         ║
║ Categoría: Metroidvania               ║
║ Duración estimada: 27 hs              ║
║ Rating: ⭐ 9.0                         ║
║                                        ║
║ Si te gustó, quizás te interesen:     ║
║  1. Ori and the Blind Forest ⭐ 8.8    ║
║  2. Dead Cells ⭐ 8.6                  ║
╚══════════════════════════════════════╝
\`\`\`