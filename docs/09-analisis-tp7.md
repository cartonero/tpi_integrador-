# Análisis TP7 — Grafo de juegos relacionados

## 1. ¿Qué resolvimos?

Incorporamos un **grafo** para modelar qué juegos se parecen entre sí. Lo usa la opción 9 del menú,
"Ver juegos relacionados". Antes de implementarlo evaluamos si nos servía; la decisión está en la
sección 2.

## 2. ¿Usamos un grafo o no?

El profe pidió que evaluáramos si el grafo aporta a nuestro dominio y, si no, que lo justificáramos.

**Decidimos usarlo.** Razones:

- **Es la estructura natural para "relacionados".** Una relación entre pares de juegos no se representa
  bien con un árbol: un juego puede parecerse a varios, y esos varios entre sí.
- **Habilita lo que sigue del proyecto:** recorridos BFS y DFS, camino de menor costo entre dos juegos y
  un recomendador. Sin grafo, esas etapas quedan sin estructura de apoyo.
- **Mejora la experiencia del jugador.** Quien busca "Hollow Knight" y quiere algo parecido hoy tendría que
  filtrar por género y recorrer cientos de juegos a mano.

**Qué habríamos argumentado para no usarlo:** que nuestras cinco funcionalidades iniciales (buscar, añadir,
comparar tiempos, explorar categorías y duración) se resuelven con árboles y la lista del catálogo. Es cierto,
pero deja afuera "relacionados", un caso de uso básico de un sistema de recomendaciones, y las etapas de
recorridos y caminos.

## 3. Modelo del grafo

| Elemento | Decisión |
|---|---|
| **Vértice** | Un juego |
| **Arista** | Une dos juegos parecidos: cada juego se une a sus 5 juegos más similares por géneros |
| **Tipo** | **No dirigido**: si A se parece a B, B se parece a A |
| **Pesado** | **Sí.** El peso es la **distancia** = 1 − similitud. Vale 0 si dos juegos tienen los mismos géneros y 1 si no comparten ninguno |
| **Representación** | **Lista de adyacencia** (diccionario de diccionarios) |

### Por qué lista de adyacencia y no matriz

Con 2000 juegos, una matriz tendría 4.000.000 de casillas, y de ellas solo 17.564 (2 × 8.782 aristas)
tendrían una relación. La densidad del grafo es del **0,44%**: es muy ralo. La lista guarda solo las
aristas que existen, y preguntar si dos juegos están unidos sigue costando O(1) gracias al diccionario.

### Por qué no unir todos los juegos que comparten un género

Probamos primero la regla más simple y la medimos sobre la muestra:

| Regla de arista | Aristas | Densidad |
|---|---:|---:|
| Comparten al menos 1 género | 1.499.903 | 75% |
| Comparten al menos 2 géneros | 685.843 | 34% |

Con la segunda regla, además, 289 juegos quedaban aislados y cada juego tenía en promedio 685 vecinos. Un
grafo así no distingue nada. El motivo es que "Indie" aparece en 1.449 de los 2000 juegos.

## 4. Cómo se calcula la similitud

Es un índice de Jaccard con pesos por género:

similitud = peso de los géneros que comparten ÷ peso de todos los géneros que tienen entre los dos

El peso de un género es `log(1 + N / cantidad de juegos con ese género)`: **cuanto más raro es un género,
más pesa**. Compartir "Strategy" dice más que compartir "Indie".

Cada juego se une a sus 5 más parecidos. Como el grafo es no dirigido, un juego puede terminar con más de 5
vecinos si otros lo eligen.

## 5. Resultados medidos

Con la muestra de 2000 juegos (`py main.py`):

| Métrica | Valor |
|---|---:|
| Vértices | 2.000 |
| Aristas | 8.782 |
| Densidad | 0,44% |
| Grado mínimo, medio y máximo | 2, 8,8 y 15 |
| Juegos aislados | 0 |
| Tiempo de construcción | 0,34 s |
| Combinaciones distintas de géneros | 361 |

Ejemplo real, juegos relacionados con "Crab Game" (Action, Casual, Free To Play, Indie, Racing):
"Turbo Tunnel" (75%), "Demon Truck" (70%) y "Make Way" (70%).

## 6. Análisis de complejidad

| Operación | Costo | Explicación |
|---|---|---|
| Agregar vértice o arista | O(1) | Inserción en diccionario |
| ¿Hay arista entre A y B? / peso | O(1) | Búsqueda en diccionario |
| Vecinos de un juego | O(g log g) | g = grado; se ordenan por peso |
| Cantidad de aristas | O(V) | Suma de grados ÷ 2 |
| Construir el grafo | O(S² + n·K) | S = combinaciones distintas de géneros (361), n = juegos, K = vecinos por juego |
| Añadir un juego al grafo | O(n) | Se compara con todos los demás |

Para construirlo no comparamos los 2000 × 2000 pares. Agrupamos los juegos con exactamente los mismos
géneros y calculamos la similitud una vez por par de grupos: unas 130.000 comparaciones en lugar de
cerca de 2 millones. El tiempo de arranque queda en 0,34 s.

## 7. Integración con la aplicación

- `servicios/relaciones.py` arma el grafo al arrancar (`main.py`).
- La opción 9 busca el juego en el AVL y pide al grafo sus vecinos, del más parecido al menos parecido.
- Al añadir un juego (opción 8), también se incorpora al grafo.

## 8. Limitaciones

- **La similitud usa solo géneros.** La muestra no trae desarrolladora, etiquetas ni descripción. Además,
  solo 555 de los 2000 juegos tienen tiempo de juego, así que no lo usamos para relacionar.
- **El grafo no es conexo.** Con 5 vecinos por juego quedan **55 componentes conexas**, la mayor con 538 juegos.
  Aumentar los vecinos ayuda pero no lo resuelve: con 20 por juego siguen 9. Para el camino mínimo (TP9) esto
  significa que entre dos juegos de componentes distintas **no existe camino**, y el sistema tendrá que
  informarlo.
- **Juegos añadidos:** se conectan al grafo con los pesos de géneros actuales, sin recalcular las aristas
  anteriores.

## 9. Errores o dudas que tuvimos

- **Primera idea descartada:** unir todos los juegos que comparten un género. Daba un grafo con 1,5 millones
  de aristas (sección 3).
- <COMPLETAR: problemas reales que hayan tenido al integrarlo o al probarlo>

## 10. Datos y evidencia

- Código: `estructuras/grafo.py` y `servicios/relaciones.py`.
- Pruebas: `tests/test_grafo.py` (`py -m unittest discover tests`).
- Material de la cátedra usado como base: `grafo.py` (lista de adyacencia) y clase 11 de grafos.
