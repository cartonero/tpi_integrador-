# Análisis TP3 — Árbol Binario de Búsqueda

## 1. ¿Qué resolvimos?

Incorporamos un **árbol binario de búsqueda (BST)** para resolver la
búsqueda por **nombre de juego** de forma más eficiente que recorrer
la lista completa del catálogo.

## 2. Clave de ordenamiento

Ordenamos el árbol por **nombre del juego** (`nombre.lower()`) porque
es el criterio por el cual el usuario busca en la app: cuando alguien
usa la opción "Buscar juego" en el menú de Juegoteca, escribe el
nombre, no la categoría ni el rating. Ordenar por ese mismo campo hace
que la búsqueda en el árbol sea directa.

## 3. Prueba del árbol

Salida de `py -m algoritmos.probar_bst`:

```text
Juegos cargados: 2000
Altura del árbol: 27

--- inorder (primeros 10, ordenado alfabéticamente) ---
  ...
  .Decluster & .Decluster Zero
  /R - A Neurodivergent Thriller
  100 hidden birds 2
  100 Men VS Gorilla
  100% Challenge
  100% Plasma Vitae
  13 WOOD ST
  13F
  1942: The Pacific Air War

--- preorder (primeros 10) ---
  A Drop of Hope
  1982
  13 WOOD ST
  /R - A Neurodivergent Thriller
  ...
  .Decluster & .Decluster Zero
  100 hidden birds 2
  100 Men VS Gorilla
  100% Plasma Vitae
  100% Challenge

--- postorder (primeros 10) ---
  .Decluster & .Decluster Zero
  ...
  100% Challenge
  100% Plasma Vitae
  100 Men VS Gorilla
  100 hidden birds 2
  /R - A Neurodivergent Thriller
  1942: The Pacific Air War
  13F
  13 WOOD ST

--- búsquedas ---
Buscar 'A Drop of Hope': A Drop of Hope (Action)
Buscar 'juego que no existe zzz': None
```

## 4. Comparación de tiempos

Los tiempos son **reales**, sacados con `algoritmos/medir_tiempos.py`.
Cada valor es el promedio de 300 búsquedas repetidas, midiendo solo la
búsqueda (la construcción de la estructura no se cronometra).

Usamos hasta **80.000** elementos en vez de 100.000: el dataset
completo de Steam (`lux/games.json`, 125.855 juegos) tiene esa
cantidad de juegos con nombre válido cargado, así que es el máximo
real disponible sin inventar datos de más.

| N elementos | Secuencial (ms) | Binaria (ms) | Árbol BST (ms) |
|---|---:|---:|---:|
| 100 | 0.0010 | 0.0008 | 0.0014 |
| 1.000 | 0.0091 | 0.0015 | 0.0019 |
| 10.000 | 0.1062 | 0.0018 | 0.0020 |
| 80.000 | 3.5766 | 0.0018 | 0.0022 |

## 5. Análisis de complejidad

- **Búsqueda secuencial:** O(n). Recorre toda la lista en el peor caso.
- **Búsqueda binaria:** O(log n), pero exige lista ordenada (ordenar
  cuesta O(n log n) una sola vez, no se mide en cada búsqueda).
- **Búsqueda en árbol:** O(log n) promedio si el árbol está
  balanceado; O(n) en el peor caso si está degenerado (como una lista
  enlazada).
- **Inserción en árbol:** O(log n) promedio, O(n) peor caso.
- **Recorridos (inorder, preorder, postorder):** O(n), porque visitan
  cada nodo una vez.

## 6. Conclusión

Con 80.000 elementos, la búsqueda secuencial tarda **3.5766 ms** contra
**0.0018 ms** de la binaria y **0.0022 ms** del árbol: casi **1.630
veces más rápido** el árbol que la secuencial. La diferencia crece con
N porque la secuencial es lineal y el árbol/binaria son logarítmicos.

Elegimos quedarnos con el **árbol BST** en la app (y no con la
binaria) porque, además de buscar rápido, el árbol permite **insertar
nuevos juegos sin tener que reordenar toda la lista** (algo que la
búsqueda binaria sí exigiría, ya que necesita la lista siempre
ordenada). Como Juegoteca va a sumar la funcionalidad de "Añadir
juegos" más adelante, el árbol es la estructura que mejor acompaña esa
necesidad.

Un punto a mejorar: la altura del árbol quedó en **27** para 2000
juegos, cuando lo ideal balanceado sería ≈11 (log₂ 2000). Esto pasa
porque insertamos los juegos en el orden en que vienen en el JSON, no
aleatorio ni balanceado. Es justamente el problema que vamos a resolver
en el TP4 con un árbol AVL.

## 7. Errores o dudas que tuvimos

- Al principio corrimos `algoritmos/probar_bst.py` como
  `py algoritmos/probar_bst.py` y nos tiraba `ModuleNotFoundError: No
  module named 'estructuras'`. El problema era que, al ejecutar un
  script dentro de una subcarpeta, Python busca los módulos desde esa
  subcarpeta y no desde la raíz del proyecto. Lo resolvimos corriendo
  el script como módulo desde la raíz: `py -m algoritmos.probar_bst`.
- El dataset original de Steam pesa ~900 MB, así que lo excluimos del
  repositorio con `.gitignore` (carpeta `lux/`) y generamos una
  muestra reducida (`datos/games.json`, 2000 juegos) que sí se
  versiona, para no romper el límite de tamaño de GitHub.