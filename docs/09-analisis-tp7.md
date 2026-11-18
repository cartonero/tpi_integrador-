# Análisis TP7 — Grafo de juegos relacionados

## 1. ¿Qué resolvimos?

Incorporamos un **grafo** para modelar qué juegos se parecen entre sí. Lo usa la opción 9 del menú,
"Ver juegos relacionados". Antes de implementarlo evaluamos si nos servía; la decisión está en la
sección 2.

## 2. ¿Usamos un grafo o no?

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


## 4. Limitaciones

- **La similitud usa solo géneros.** La muestra no trae desarrolladora, etiquetas ni descripción. Además,
  solo 555 de los 2000 juegos tienen tiempo de juego, así que no lo usamos para relacionar.
- **El grafo no es conexo.** Con 5 vecinos por juego quedan **55 componentes conexas**, la mayor con 538 juegos.
  Aumentar los vecinos ayuda pero no lo resuelve: con 20 por juego siguen 9. Para el camino mínimo (TP9) esto
  significa que entre dos juegos de componentes distintas **no existe camino**, y el sistema tendrá que
  informarlo.
- **Juegos añadidos:** se conectan al grafo con los pesos de géneros actuales, sin recalcular las aristas
  anteriores.

## 5. Datos y evidencia

- Código: `estructuras/grafo.py` y `servicios/relaciones.py`.
- Pruebas: `tests/test_grafo.py` (`py -m unittest discover tests`).
- Material de la cátedra usado como base: `grafo.py` (lista de adyacencia) y clase 11 de grafos.
