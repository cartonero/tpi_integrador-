# Análisis TP4 + TP5 — AVL y Árbol General

## 1. ¿Qué resolvimos?

En esta etapa incorporamos dos estructuras de datos que resuelven problemas
distintos dentro de Juegoteca:

| Estructura | Problema que resuelve | Dónde se usa |
|---|---|---|
| AVL | Que la búsqueda por nombre de juego sea siempre rápida (O(log n)), incluso si los datos llegan ordenados | Opción "Buscar juego" del menú |
| Árbol General | Representar la jerarquía de categorías del dominio (grupos de Steam y sus géneros) | Opción "Explorar categorías" del menú |

El BST del TP3 sigue funcionando: se mantiene para la opción "Ver recorridos"
y para comparar su altura contra la del AVL.

## 2. TP4 — Árbol AVL

### 2.1 ¿Por qué AVL y no un BST común?

Un BST común se desbalancea cuando los datos se insertan ordenados (por
ejemplo, nombres en orden alfabético): cada nodo queda con un solo hijo y el
árbol se convierte en una lista enlazada, con búsqueda O(n). El AVL resuelve
esto con rotaciones automáticas que mantienen la altura en O(log n) sin
importar el orden de inserción.

Con nuestros datos reales se ve el efecto: con los 2000 juegos del catálogo,
en el orden en que vienen en el JSON, el BST quedó con altura **27** y el AVL
con altura **13** (lo mínimo posible sería 11).

### 2.2 Rotaciones implementadas

| Rotación | Caso | Cuándo se aplica |
|---|---|---|
| Simple derecha | Izquierda-Izquierda | Factor de balance > 1 y el nuevo dato va a la izquierda del hijo izquierdo |
| Simple izquierda | Derecha-Derecha | Factor de balance < -1 y el nuevo dato va a la derecha del hijo derecho |
| Doble izquierda-derecha | Izquierda-Derecha | Factor de balance > 1 pero el hijo izquierdo está cargado hacia la derecha |
| Doble derecha-izquierda | Derecha-Izquierda | Factor de balance < -1 pero el hijo derecho está cargado hacia la izquierda |

El factor de balance de un nodo es `altura(izquierdo) - altura(derecho)`. En
un AVL tiene que valer siempre -1, 0 o +1.

### 2.3 Casos de desbalance generados

Probamos dos escenarios que rompen a un BST común:

1. **10 elementos ordenados (A, B, C, ..., J)**: el BST queda con altura 10 (una
   cadena) y el AVL con altura 4.
2. **Hasta 10.000 nombres de juegos reales ordenados alfabéticamente**
   (script `algoritmos/comparar_bst_avl.py`): el BST queda con altura igual a
   la cantidad de datos y el AVL con altura 14.

Además, `algoritmos/probar_avl.py` fuerza cada una de las 4 rotaciones con 3
inserciones y verifica que el árbol quede balanceado.

### 2.4 Comparación BST vs AVL

Datos reales medidos con `py -m algoritmos.comparar_bst_avl`, con nombres de
juegos del dataset de Steam **ordenados alfabéticamente** (el peor caso del BST).
La búsqueda mide el peor caso (el último nombre insertado) y es el promedio de
100 repeticiones. La construcción se cronometra aparte.

| N | Altura BST | Altura AVL | Buscar BST (ms) | Buscar AVL (ms) | Construir BST (s) | Construir AVL (s) |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | 100 | 7 | 0.0146 | 0.0010 | 0.00 | 0.00 |
| 1.000 | 1.000 | 10 | 0.2112 | 0.0013 | 0.10 | 0.01 |
| 5.000 | 5.000 | 13 | 1.1580 | 0.0017 | 2.94 | 0.04 |
| 10.000 | 10.000 | 14 | 2.9792 | 0.0018 | 12.98 | 0.08 |

Resumen de métricas:

| Métrica | BST común | AVL |
|---|---|---|
| Altura con 10 elementos ordenados (A..J) | 10 | 4 |
| Altura con 10.000 nombres ordenados | 10.000 | 14 |
| Búsqueda (peor caso) con 10.000 datos ordenados | 2.9792 ms | 0.0018 ms |
| Construcción con 10.000 datos ordenados | 12.98 s | 0.08 s |
| Altura con el catálogo real (2000 juegos, orden del JSON) | 27 | 13 |
| Complejidad de búsqueda en el peor caso | O(n) | O(log n) |
| Complejidad de inserción | O(log n) promedio, O(n) peor caso | O(log n) |

**Justificación:** con 10.000 datos ordenados, buscar en el AVL es unas 1.650
veces más rápido que en el BST, y construirlo es unas 160 veces más rápido. La
diferencia crece con N: con 100 datos es de unas 15 veces y con 1.000 de unas
160. El tiempo de búsqueda del AVL casi no cambia (de 0.0010 a 0.0018 ms)
porque crece con log n.

### 2.5 Prueba del AVL

Salida de `py -m algoritmos.probar_avl` (secciones 1 a 3):

```text
======================================================================
1. LAS 4 ROTACIONES DEL AVL
======================================================================
Cada caso inserta 3 números que desbalancean el árbol. Si la rotación
funciona, el 2 queda como raíz y el árbol queda con altura 2.

  Simple derecha (izquierda-izquierda)     insertar [3, 2, 1] -> raíz 2, preorder [2, 1, 3], altura 2
  Simple izquierda (derecha-derecha)       insertar [1, 2, 3] -> raíz 2, preorder [2, 1, 3], altura 2
  Doble izquierda-derecha                  insertar [3, 1, 2] -> raíz 2, preorder [2, 1, 3], altura 2
  Doble derecha-izquierda                  insertar [1, 3, 2] -> raíz 2, preorder [2, 1, 3], altura 2

Verificación: las 4 rotaciones dejan el árbol balanceado. OK

======================================================================
2. DATOS ORDENADOS (A..J): BST común vs AVL
======================================================================
Elementos insertados en orden: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
Altura del BST común : 10  (una cadena: cada nodo tiene un solo hijo)
Altura del AVL       : 4
Nodos del AVL        : 10

--- inorder del AVL (tiene que salir ordenado) ---
  [A(1), B(2), C(3), D(4), E(5), F(6), G(7), H(8), I(9), J(10)]

--- preorder del AVL (muestra cómo quedó balanceado) ---
  [D(4), B(2), A(1), C(3), H(8), F(6), E(5), G(7), I(9), J(10)]

--- búsquedas ---
Buscar 'F': F(6)
Buscar 'Z': None

Verificación: inorder ordenado y todos los nodos con balance -1/0/+1. OK

======================================================================
3. AVL CON EL CATÁLOGO REAL DE JUEGOTECA
======================================================================
Juegos en el catálogo : 2000
Altura del BST        : 27
Altura del AVL        : 13
Nodos del AVL         : 1999 (ignora nombres repetidos)

--- inorder del AVL (primeros 5) ---
  ...
  .Decluster & .Decluster Zero
  /R - A Neurodivergent Thriller
  100 hidden birds 2
  100 Men VS Gorilla

--- búsquedas ---
Buscar 'A Drop of Hope': A Drop of Hope (Action)
Buscar 'juego que no existe zzz': None

Verificación: todos los nodos con balance -1/0/+1. OK
```

Una observación: el AVL tiene 1999 nodos y el catálogo 2000 juegos porque hay un
nombre repetido (ignorando mayúsculas) y el AVL no inserta duplicados. El BST
del TP3 sí los guarda.

### 2.6 Código del AVL

Archivo: `estructuras/avl.py`

- `NodoAVL`: nodo con dato, hijos izquierdo y derecho, y su altura.
- `AVL`: inserción balanceada, búsqueda, recorridos (inorder, preorder,
  postorder), altura y cantidad de nodos.
- Rotaciones: `_rotacion_izquierda`, `_rotacion_derecha`,
  `_rotacion_izquierda_derecha`, `_rotacion_derecha_izquierda`.

## 3. TP5 — Árbol General (N-ario)

### 3.1 ¿Qué es un árbol general?

A diferencia del árbol binario, donde cada nodo tiene como máximo 2 hijos, en
un árbol general cada nodo puede tener cualquier cantidad de hijos. Eso lo
hace ideal para representar jerarquías naturales.

### 3.2 Jerarquía elegida del dominio

El dataset de Steam trae 26 géneros distintos, pero no son todos del mismo
tipo: hay géneros de juegos, modalidades de acceso, software y etiquetas de
contenido para adultos. Los agrupamos siguiendo la forma en que la tienda de
Steam los clasifica (los nombres de los grupos son nuestros):

```text
Juegoteca
├── Juegos
│   ├── Action · Adventure · Casual · Indie · RPG
│   └── Simulation · Strategy · Sports · Racing · Massively Multiplayer
├── Modalidad de acceso
│   └── Early Access · Free To Play
├── Software y herramientas
│   └── Utilities · Audio Production · Game Development · Photo Editing
│       · Design & Illustration · Animation & Modeling · Video Production
│       · Software Training · Education · Web Publishing
└── Contenido para adultos
    └── Violent · Gore · Nudity · Sexual Content
```

**¿Por qué esta jerarquía?**

- Los géneros son una clasificación natural del dominio, y salen de datos
  reales (los 26 géneros de nuestro catálogo entran todos en la jerarquía).
- Cada grupo tiene una cantidad distinta de hijos (10, 2, 10 y 4), que es
  justo lo que un árbol binario no permite. Por eso hace falta un árbol general.
- Se conecta con el AVL: el AVL busca un juego por nombre, y el árbol general
  organiza la navegación por categoría. Al elegir un género, la app lista los
  juegos de ese género usando el catálogo.

### 3.3 Recorridos implementados

| Recorrido | Descripción | Complejidad |
|---|---|---|
| Amplitud (BFS) | Nivel por nivel, de arriba hacia abajo | O(n) |
| Profundidad preorder | Nodo → hijos de izquierda a derecha | O(n) |
| Profundidad postorder | Hijos → nodo | O(n) |

En la app, la opción "Explorar categorías" usa el preorder para mostrar el
árbol completo con sangría y la amplitud para mostrarlo por niveles.

### 3.4 Prueba del árbol general

Salida de `py -m algoritmos.probar_avl` (sección 4):

```text
======================================================================
4. ÁRBOL GENERAL: JERARQUÍA DE CATEGORÍAS DE STEAM
======================================================================
Árbol General (raíz: Juegoteca, altura: 3)
Cantidad de nodos : 31
Altura            : 3

--- Recorrido en AMPLITUD (primeros 8) ---
  ['Juegoteca', 'Juegos', 'Modalidad de acceso', 'Software y herramientas', 'Contenido para adultos', 'Action', 'Adventure', 'Casual']

--- Recorrido en PROFUNDIDAD preorder (primeros 8) ---
  ['Juegoteca', 'Juegos', 'Action', 'Adventure', 'Casual', 'Indie', 'RPG', 'Simulation']

--- Recorrido en PROFUNDIDAD postorder (primeros 8) ---
  ['Action', 'Adventure', 'Casual', 'Indie', 'RPG', 'Simulation', 'Strategy', 'Sports']

--- Niveles ---
Nivel 0:
  Juegoteca
Nivel 1:
  Juegos, Modalidad de acceso, Software y herramientas, Contenido para
  adultos
Nivel 2:
  Action, Adventure, Casual, Indie, RPG, Simulation, Strategy, Sports,
  Racing, Massively Multiplayer, Early Access, Free To Play,
  Utilities, Audio Production, Game Development, Photo Editing, Design
  & Illustration, Animation & Modeling, Video Production, Software
  Training, Education, Web Publishing, Violent, Gore, Nudity, Sexual
  Content

--- Búsquedas ---
Hijos de 'Juegos': ['Action', 'Adventure', 'Casual', 'Indie', 'RPG', 'Simulation', 'Strategy', 'Sports', 'Racing', 'Massively Multiplayer']
Buscar 'Indie': Nodo(Indie)
Buscar 'Zzz': None

Verificación: 31 nodos, altura 3, búsquedas correctas. OK
```

### 3.5 Código del árbol general

- `estructuras/arbol_general.py`: `NodoGeneral` (dato y lista de hijos) y
  `ArbolGeneral` con `insertar_raiz`, `agregar_hijo`, `buscar`, `amplitud`,
  `profundidad_preorder`, `profundidad_postorder`, `obtener_niveles`,
  `altura` y `cantidad_nodos`.
- `servicios/categorias.py`: define la jerarquía (grupos y géneros) y arma el
  árbol con `construir_arbol_categorias(catalogo)`. Si el catálogo tuviera un
  género que no está en la jerarquía, lo cuelga de un grupo "Otros".

## 4. Integración con la aplicación


┌──────────────────────────────────────────────────────────────┐
│                     Interfaz de terminal                     │
├──────────────┬───────────────┬──────────────┬────────────────┤
│  1. Buscar   │ 4. Recorridos │ 5. Explorar  │ 2. Listar      │
│              │    del BST    │   categorías │ 3. Filtrar     │
│  usa: AVL    │  usa: BST     │ usa: Árbol   │ usa: Catálogo  │
│              │  (y compara   │   General    │   (lista)      │
│              │   con el AVL) │              │                │
└──────────────┴───────────────┴──────────────┴────────────────┘
```

### 4.2 Código de integración

En `main.py`, al arrancar se construyen las tres estructuras (una sola vez):

```python
catalogo = cargar_catalogo()
bst, avl = construir_arboles(catalogo)
arbol_categorias = construir_arbol_categorias(catalogo)  # árbol general (TP5)

iniciar(catalogo, bst, avl, arbol_categorias)
```

Opción "Buscar juego" (en `ui/terminal.py`), ahora con el AVL:

```python
juego = avl.buscar(nombre.lower(), clave=lambda j: j.get_nombre().lower())
```

Opción "Explorar categorías": navega los hijos de cada nodo (grupos y
géneros), y muestra el árbol completo en profundidad (`_imprimir_arbol`) y por
niveles en amplitud (`arbol_categorias.obtener_niveles()`).

## 5. Análisis de complejidad

| Operación | AVL | Árbol General |
|---|---|---|
| Inserción | O(log n) | O(1) (agregar un hijo a un nodo ya conocido) |
| Búsqueda | O(log n) | O(n) (recorre el árbol hasta encontrar el nodo) |
| Recorridos (inorder, preorder, postorder / amplitud) | O(n) | O(n) |
| Altura (peor caso) | O(log n) | O(n) en un árbol degenerado (en el nuestro es 3) |

**¿Por qué el AVL es O(log n)?** Porque mantiene el factor de balance entre -1
y +1 en cada nodo, y eso garantiza que la altura sea proporcional a log₂(n). En
nuestros datos: con 10.000 nodos el AVL tiene altura 14 (log₂ 10.000 ≈ 13,3),
mientras que el BST con los mismos datos ordenados tiene altura 10.000. Cada
búsqueda baja un nivel por paso, así que cuesta como mucho la altura del árbol.

**¿Por qué el árbol general no se auto-balancea?** Porque no tiene un criterio
de orden: su estructura refleja una jerarquía natural (grupo → género), no un
orden numérico o alfabético. El costo de búsqueda O(n) es aceptable porque
tiene 31 nodos y la cantidad de categorías suele ser pequeña.

**Nota sobre la amplitud:** la implementación del recorrido en amplitud usa una
lista como cola y saca el primer elemento con `pop(0)`, que cuesta O(n) por
operación. Con `collections.deque` sería O(1) y el recorrido quedaría O(n)
estricto. Con 31 nodos no se nota.

## 6. Conclusión

- El AVL garantiza búsquedas eficientes sin importar el orden de inserción:
  con 10.000 nombres ordenados buscar es unas 1.650 veces más rápido que en el
  BST común, y construir el árbol unas 160 veces más rápido.
- Con los datos reales del catálogo (sin ordenar) la diferencia es más
  moderada pero existe: altura 13 contra 27.
- El árbol general permite organizar el dominio en una jerarquía significativa
  (grupos de Steam y sus géneros) y mejora la experiencia del usuario al
  explorar categorías.
- Las dos estructuras se complementan: el AVL resuelve la búsqueda por nombre y
  el árbol general organiza la navegación por categoría.
- Ninguna se usó "por cumplir": el AVL resuelve un problema real (el
  desbalance que medimos) y el árbol general resuelve otro (la jerarquización
  del dominio, con cantidad variable de hijos).
- El BST del TP3 se mantiene y sigue funcionando (opción 4 del menú).

## 7. Errores o dudas que tuvimos

- **`comparar_bst_vs_avl` fallaba:** la función del `avl.py` que recibimos
  buscaba un archivo `arboles.py`, pero nuestro BST está en
  `estructuras/arbol_binario.py`. Cambiamos el import para que apunte ahí.
- **`SyntaxError: invalid escape sequence`:** los dibujos de las rotaciones
  dentro de los docstrings usaban barras invertidas. Pasamos esos docstrings a
  modo "raw" (`r"""`).
- **`MemoryError` al cargar el dataset:** `json.load` intentaba meter los
  ~900 MB de `lux/games.json` en memoria. Lo resolvimos leyendo los nombres de
  `lux/games.csv` fila por fila con `csv.reader`, sin cargar el archivo entero.
- **Límite de recursión de Python:** un BST con más de ~1000 datos ordenados
  supera los 1000 niveles de recursión que Python permite por defecto. En
  `comparar_bst_avl.py` subimos el límite con `sys.setrecursionlimit` para poder
  medir el BST degenerado.
- **`ModuleNotFoundError` / `No such file or directory`:** corríamos los
  comandos con la terminal en la carpeta de afuera del proyecto, o ejecutábamos
  scripts de `algoritmos/` con `py algoritmos/script.py`. Hay que correr desde
  la raíz del proyecto y con `py -m algoritmos.nombre_del_script`.
- **`ImportError: cannot import name 'construir_arbol_categorias'`:** habíamos
  pegado el código en `categorias.py` pero no lo habíamos guardado, así que en
  disco el archivo seguía vacío. Guardar antes de ejecutar.

## 8. Datos y evidencia

- Script de prueba del AVL y del árbol general: `algoritmos/probar_avl.py`
- Script de comparación BST vs AVL: `algoritmos/comparar_bst_avl.py`
