# Juegoteca — contexto para Claude Code

Proyecto integrador de Estructuras de Datos (UNAB, Comisión 3, Grupo 10). Sistema de consola en Python sobre el
Steam Games Dataset. Integrantes: Rodrigo Cruz Choque, Ian Martinez, Milagros Ponce.

**Prioridad del proyecto:** que se entienda y se pueda defender, no la cantidad de líneas. Cada estructura tiene
que poder responder "¿por qué esta estructura?". No agregar estructuras de forma artificial.

## Cómo ejecutar

Siempre desde la carpeta raíz (la que tiene `main.py`). En Windows se usa `py`, no `python`.

```powershell
py main.py                                # programa
py -m unittest discover tests             # pruebas
py -m algoritmos.probar_avl               # prueba del AVL con salida
py -m algoritmos.altas_masivas            # desafío de 100.000 altas
py -m algoritmos.medir_tiempos            # necesita la carpeta lux/
```

Solo Python estándar. No instalar librerías externas.

## Estructura

- `modelos/`: `Juego` (con rating y duración) y `Catalogo` (lista + diccionario por appid).
- `estructuras/`: `arbol_binario.py` (BST), `avl.py`, `arbol_general.py`, `grafo.py` (no dirigido, pesado, lista de adyacencia).
- `servicios/`: `cargador_datos.py`, `categorias.py`, `juegos.py` (añadir, comparar), `relaciones.py` (similitud y grafo).
- `ui/terminal.py`: menú 0 a 10 y la tarjeta de búsqueda.
- `algoritmos/`: `bfs.py` y `dfs.py` (se usan en la opción 10) y scripts de prueba y medición que no forman parte del menú.
- `tests/`: pruebas con `unittest`.
- `datos/games.json`: muestra de 2000 juegos. `docs/`: documentación 00 a 09.

## Reglas importantes

- **No volver a correr `algoritmos/preparar_datos.py`**: regenera la muestra al azar y cambia todos los números de la documentación.
- `lux/` (dataset completo, 900 MB) está en `.gitignore`. No subirlo ni leerlo entero en memoria.
- Atributos privados con `_` y getters. Un solo objeto `Juego` compartido por catálogo, BST, AVL y grafo.
- `agregar_juego` valida antes de modificar, para no dejar las estructuras incoherentes. El BST es recursivo:
  `main.py` sube el límite de recursión a 10.000.
- Cada alta en el grafo cuesta O(n). Para cargas masivas, armar el grafo una sola vez al final.
- "Duración estimada" es el tiempo de juego promedio en Steam, no el tiempo para completar. Solo 555 de 2000 juegos lo tienen.
- Todos los números de la documentación (alturas, tiempos, densidades) son mediciones reales. No inventar ni
  redondear números: si se cambia el código, volver a medir y actualizar los docs.
- Cada TP actualiza `docs/03-diagrama-clases.md` y `docs/04-diagrama-datos.md`. Los diagramas son Mermaid.
- No usar emojis en la terminal: desalinean el borde de la tarjeta.

## Cómo trabajar con el equipo

- Español informal. Una funcionalidad por vez, con pasos claros.
- Entregar archivos completos, no diffs.
- Hacer commit después de cada cambio, con mensaje claro. Rama `main`.
- Si algo del código no se puede justificar en la defensa, avisar en lugar de agregarlo.

## Estado

Hecho: TP0 a TP5, TP7 (grafo), TP8 (BFS y DFS, opción 10), añadir juego, comparar tiempos, duración, tarjeta con relacionados, docs 00 a 10.

Pendiente, en este orden de importancia para la demo:
1. **Heap (TP6)** para el Top 10.
2. **Camino mínimo (TP9)**, con Dijkstra. Ojo: el grafo no es conexo (55 componentes con 5 vecinos), hay que informar "no hay camino" (`bfs_saltos_entre` ya lo hace).
3. Recomendador y cierre (TP10).
4. Completar los `<COMPLETAR>` de `docs/05` (retros), `docs/06`, `docs/09` y `docs/10`.
5. Actualizar `docs/01`, `docs/02`, `docs/03`, `docs/04` y el README con cada etapa nueva.
