# Análisis TP8 — Recorridos BFS y DFS sobre la red de juegos

## 1. ¿Qué resolvimos?

Con el grafo del TP7 ya sabemos qué juegos se parecen. Este TP agrega dos formas de **recorrer** esa red y
responder preguntas que el grafo solo no contesta:

- **BFS (en anchura)** responde "¿qué tan cerca está un juego de otro?". Está en `algoritmos/bfs.py`.
- **DFS (en profundidad)** responde "¿qué hay conectado con este juego, en total?". Está en `algoritmos/dfs.py`.

Se usan desde la opción 4 del menú, "Extras", que tiene un submenú con "Explorar la red de juegos".

## 2. Los dos casos de uso

| Consulta del jugador | Algoritmo | Por qué ese |
|---|---|---|
| "¿Cuántos saltos hay entre el juego A y el juego B?" y "¿qué juegos están a 1 o 2 saltos de A?" | **BFS** | Explora por capas: primero los vecinos directos, después los vecinos de esos, y así. La primera vez que llega a un juego lo hace por el camino con menos aristas. |
| "Explorá todos los juegos conectados con A" | **DFS** | Se mete hasta el fondo de cada rama antes de volver. Recorre todo el grupo sin importar la distancia. |

Un ejemplo con datos reales (juego de partida: Crab Game):

- Tiene **7 juegos a 1 salto** y **24 a 2 saltos**.
- Está a **1 salto** de Turbo Tunnel y a **12 saltos** de "镜花饴情 Mirage Sugar Acacia", que es lo más lejos
  que llega (BFS lo visita último).
- El DFS lo conecta con **537 juegos más**, de los 2000 del grafo.
- Con un juego de otro grupo, BFS no encuentra camino y lo informa.

## 3. Cómo funcionan, en simple

**BFS** usa una **cola** (el primero que entra es el primero que sale). Se parte del juego de origen, se
agregan a la cola sus vecinos y se los va sacando de a uno, agregando los vecinos nuevos al final. Como los
más cercanos entran antes, siempre se terminan de visitar las capas más cercanas antes de pasar a las lejanas.
Se anota qué vecinos ya se visitaron para no volver a ellos.

**DFS** usa una **pila** (el último que entra es el primero que sale). Se toma un juego, se visita, y se
apilan sus vecinos; el siguiente en salir es el último apilado, o sea que se sigue por una rama hasta
agotarla y recién después se vuelve a probar otra. Los vecinos se apilan al revés para que el primero en
visitarse sea el más parecido.

Los dos marcan lo visitado (`visitados`), por eso funcionan bien aunque el grafo tenga ciclos: nunca se
quedan dando vueltas.

**Funciones:**

| Función | Qué hace |
|---|---|
| `bfs(grafo, inicio, max_saltos)` | Lista los juegos con sus saltos, por capas. Puede cortar en un máximo de saltos. |
| `bfs_saltos_entre(grafo, origen, destino)` | Cuenta los saltos entre dos juegos, o `None` si no hay camino. |
| `dfs(grafo, inicio)` | Lista, en profundidad, todo lo alcanzable desde un juego. |
| `componentes_conexas(grafo)` | Separa el grafo en grupos que no se conectan entre sí (usa DFS). |

## 4. Complejidad

| Operación | Tiempo | Memoria |
|---|---|---|
| `bfs`, `dfs` | O(V + E) | O(V) |
| `bfs_saltos_entre` | O(V + E) en el peor caso, pero corta al encontrar el destino | O(V) |
| `componentes_conexas` | O(V + E) en total | O(V) |

V es la cantidad de juegos (vértices) y E la de relaciones (aristas). Cada juego entra una sola vez a la
cola o a la pila, y cada relación se mira una vez desde cada extremo. En nuestro grafo V = 2000 y E = 8.782.

**Cola con `deque`:** BFS usa `collections.deque` (biblioteca estándar) y no una lista común, porque sacar el
primer elemento de una lista cuesta O(n) y con `deque` cuesta O(1).

## 5. BFS contra DFS: cuándo conviene cada uno

| | BFS | DFS |
|---|---|---|
| Estructura auxiliar | Cola | Pila |
| Orden de visita | Por capas, de cerca a lejos | Rama por rama, hasta el fondo |
| Camino con menos aristas | **Sí**, lo garantiza | No, puede llegar por un camino largo |
| Sirve para | Distancias y "lo más cercano" | Explorar todo un grupo, detectar grupos separados |
| Complejidad | O(V + E) | O(V + E) |

Los dos cuestan lo mismo. Se elige por la pregunta, no por la velocidad.

**Atención con los saltos:** BFS cuenta **aristas**, no pesos. Dos juegos pueden estar a 1 salto aunque ese
salto sea una relación débil (peso alto). Para el camino de menor **costo** hace falta Dijkstra, que
corresponde al TP9.

## 6. Limitaciones

- **El grafo no es conexo.** Hay 55 grupos de juegos separados (el mayor tiene 538). Por eso BFS puede
  responder "no hay camino" y DFS solo explora el grupo del juego de partida.
- **Hay grupos muy chicos:** los más chicos tienen unos 6 juegos, así que explorar desde ahí muestra poco.
- **La exploración de la red limita lo que muestra** para que la pantalla sea legible: 6 juegos por capa y 15 en el
  recorrido en profundidad. El resto se informa solo como cantidad.
- **DFS no es iterativo por casualidad:** se escribió con pila explícita y no con recursión porque un grupo
  de 538 juegos encadenados podría pasar el límite de recursión de Python.

## 7. Datos y evidencia

Medido sobre la muestra de 2000 juegos, partiendo de Crab Game:

| Medición | Resultado |
|---|---|
| Juegos a 1 salto | 7 |
| Juegos a 2 saltos | 24 |
| Juegos alcanzables (BFS y DFS coinciden) | 538 (él mismo y 537 más) |
| Saltos hasta el juego más lejano | 12 |
| Grupos conectados en todo el grafo | 55 (el mayor con 538, la suma da 2000) |
| Tiempo de BFS o DFS completo | menos de 1 ms |
| Tiempo de separar todo el grafo en grupos | unos 2 ms |

Los tiempos cambian según la computadora. Los conteos no.

**Pruebas:** `tests/test_bfs_dfs.py` (18 pruebas) verifica el orden por capas, el límite de saltos, el
orden en profundidad, los ciclos, los vértices aislados, el caso sin camino y que BFS y DFS alcancen los
mismos juegos.

## 8. Errores o dudas que tuvimos

- <COMPLETAR: problemas reales que hayan tenido al implementar o probar BFS y DFS>
