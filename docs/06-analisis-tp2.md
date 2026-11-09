# Análisis TP2 — Complejidad de la búsqueda

## 1. ¿Qué resolvimos?

Comparamos dos formas de buscar un juego por nombre para saber cuál conviene cuando el catálogo crece:

- **Búsqueda secuencial:** recorre la lista de a un elemento hasta encontrar el nombre.
- **Búsqueda binaria:** parte la lista ordenada a la mitad en cada paso y descarta una de las dos mitades.

## 2. Cómo medimos

- **Script:** `algoritmos/medir_tiempos.py`, que se ejecuta con `py -m algoritmos.medir_tiempos`.
- **Datos:** nombres de juegos del dataset completo de Steam (`lux/games.json`), en el orden del archivo.
- **Qué se mide:** solo la búsqueda. Ordenar la lista para la binaria se hace una vez, antes de medir.
- **Repeticiones:** cada valor es el promedio de 300 búsquedas, porque una sola dura microsegundos y no se puede medir bien.
- **Elemento buscado:** el que está en la mitad de la lista, que siempre existe.

## 3. Resultados

Tiempos reales de nuestra máquina, tomados de la última corrida del script.

| N elementos | Secuencial (ms) | Binaria (ms) |
|---|---:|---:|
| 100 | 0.0010 | 0.0008 |
| 1.000 | 0.0089 | 0.0014 |
| 10.000 | 0.1011 | 0.0018 |
| 100.000 | 5.3894 | 0.0023 |

Lo que se ve en la tabla:

- La secuencial crece con N: de 0.0010 ms con 100 elementos a 5.3894 ms con 100.000.
- La binaria casi no cambia: de 0.0008 a 0.0023 ms mientras la lista se multiplica por 1.000.
- Con 100 elementos casi no hay diferencia. La binaria conviene cuando el catálogo es grande.

## 4. Análisis de complejidad

| Algoritmo | Mejor caso | Peor caso | Condición |
|---|---|---|---|
| Secuencial | O(1) | O(n) | Ninguna |
| Binaria | O(1) | O(log n) | La lista tiene que estar ordenada |

Con n = 100.000, la secuencial puede necesitar hasta 100.000 comparaciones y la binaria, unas 17
(porque 2^17 = 131.072).

Ordenar la lista cuesta O(n log n). Se paga una vez y después conviene si se hacen muchas búsquedas.

## 5. Conclusión

Para un catálogo de miles de juegos, la binaria es la mejor de las dos. Pero tiene un problema que
aparece cuando hay que **añadir juegos**: para mantener la lista ordenada hay que insertar en el lugar
correcto, y eso cuesta O(n). Esto nos llevó a probar un árbol binario de búsqueda en el TP3, que permite
buscar en O(log n) e insertar sin reordenar toda la lista.

## 6. Errores o dudas que tuvimos

- **Tamaño del dataset:** el archivo completo pesa cerca de 900 MB. Por eso el repositorio guarda solo
  una muestra de 2000 juegos (`datos/games.json`) y el dataset completo queda fuera de git (`lux/`).
- <COMPLETAR: otros problemas que hayan tenido al medir y cómo los resolvieron>

## 7. Datos y evidencia

- Script de medición: `algoritmos/medir_tiempos.py`.
- La misma corrida incluye la columna del árbol BST, que se analiza en [docs/07-analisis-tp3.md](07-analisis-tp3.md).
