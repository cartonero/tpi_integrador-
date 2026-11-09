# Requerimientos — Juegoteca

## Alcance

Juegoteca es un sistema de consola que permite buscar videojuegos de Steam por nombre, navegar por
categorías, consultar cuánto se suele jugar cada título y comparar tiempos entre juegos. Está pensado
para videojugadores que quieren decidir a qué jugar sabiendo cuánto tiempo les va a llevar.

## Requerimientos funcionales (RF)

| ID | Requerimiento | Estado |
|---|---|---|
| RF01 | El sistema debe permitir buscar un juego por nombre, sin distinguir mayúsculas | ✅ TP1, TP4 |
| RF02 | El sistema debe permitir listar los juegos del catálogo, paginados | ✅ TP1 |
| RF03 | El sistema debe permitir filtrar los juegos por categoría | ✅ TP1 |
| RF04 | El sistema debe mostrar los juegos en orden alfabético y en los otros recorridos del árbol | ✅ TP3 |
| RF05 | El sistema debe permitir explorar las categorías como una jerarquía de grupos y géneros | ✅ TP5 |
| RF06 | El sistema debe mostrar la duración estimada de un juego | ✅ |
| RF07 | El sistema debe permitir comparar el tiempo de juego de dos o más juegos | ✅ |
| RF08 | El sistema debe permitir añadir un juego nuevo al catálogo durante la sesión | ✅ |
| RF09 | El sistema debe mostrar los N juegos con más tiempo de juego | ⏳ TP6 |
| RF10 | El sistema debe mostrar los juegos relacionados con uno dado | ⏳ TP7 |
| RF11 | El sistema debe encontrar el camino de menor costo entre dos juegos | ⏳ TP9 |
| RF12 | El sistema debe sugerir juegos a partir de uno dado | ⏳ TP10 |

### Criterios de aceptación

> **RF01 — Buscar por nombre**
> - "Crab Game", "crab game" y "CRAB GAME" devuelven el mismo juego.
> - Si el juego no existe, el sistema lo informa y vuelve al menú.
> - Responde en menos de 1 segundo con 10.000 juegos.

> **RF07 — Comparar tiempos**
> - Se ingresan los nombres uno por línea; una línea vacía termina la lista.
> - Se necesitan al menos 2 juegos encontrados.
> - Los juegos sin dato de tiempo se informan aparte y no entran en la comparación.

> **RF08 — Añadir un juego**
> - El nombre no puede estar vacío ni repetirse.
> - Los géneros deben pertenecer a la jerarquía de categorías.
> - El juego nuevo se puede buscar de inmediato, sin reiniciar el programa.

## Requerimientos no funcionales (RNF)

| ID | Requerimiento | Verificación |
|---|---|---|
| RNF01 | La búsqueda por nombre debe ser logarítmica sobre el total de juegos | AVL, TP4. Ver `docs/08-analisis-tp4-tp5.md` |
| RNF02 | El sistema debe soportar al menos 10.000 juegos sin degradar la respuesta | TP2 y TP4: con 10.000 nombres el AVL tiene altura 14 y busca en 0.0018 ms |
| RNF03 | La interfaz debe ser usable por alguien que no conoce la implementación | Menú numerado y mensajes de error que explican qué corregir |
| RNF04 | El proyecto debe ejecutarse con Python 3.10 o superior, sin instalar librerías | README |
| RNF05 | Los datos de un juego deben estar encapsulados y accederse solo por getters | `modelos/juego.py` |

## Fuera de alcance

- Autenticación o perfiles de usuario.
- Persistencia de preferencias personales.
- Persistencia de los juegos añadidos: viven solo en memoria durante la sesión.
- Interfaz gráfica: todo es consola.

## Observaciones

- **Dos árboles de búsqueda a propósito.** Se conserva el BST del TP3 (opción 4) y se usa el AVL para
  buscar (opción 1). Así se puede mostrar en la defensa la diferencia entre un árbol que se degenera y
  uno que se balancea.
- **"Duración estimada" no es el tiempo para terminar el juego.** Es el tiempo de juego promedio de los
  jugadores en Steam (`average_playtime_forever`). Solo 555 de los 2000 juegos de la muestra tienen
  ese dato, y el sistema avisa que no hay datos de duración en los demás.
- **Muestra de 2000 juegos.** El dataset completo pesa cerca de 900 MB, así que se versiona una muestra
  (`datos/games.json`). Nombres repetidos dentro de la muestra se ignoran en el AVL.
- **Trazabilidad con el TP0.** Las cinco funcionalidades iniciales corresponden a: F1 → RF01,
  F2 → RF08, F3 → RF07, F4 → RF05, F5 → RF06.
