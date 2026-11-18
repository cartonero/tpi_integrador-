# Diagrama de clases

> Estado: TP8 (BFS y DFS), más las funcionalidades de añadir, comparar y duración. Se actualiza en cada TP con la
> estructura nueva.

```mermaid
classDiagram
    class Juego {
        -appid: str
        -nombre: str
        -generos: list
        -tiempo_min: int
        -positivos: int
        -negativos: int
        +get_appid() str
        +get_nombre() str
        +get_generos() list
        +get_categoria_principal() str
        +get_tiempo_min() int
        +tiene_tiempo() bool
        +get_rating() float
        +get_votos() int
    }

    class Catalogo {
        -juegos: list
        -por_appid: dict
        +agregar(juego) bool
        +buscar(nombre) Juego
        +buscar_por_appid(appid) Juego
        +listar() list
        +filtrar_por_categoria(categoria) list
        +cantidad() int
    }

    class ArbolBST {
        -raiz: NodoArbol
        +insertar(dato, clave) None
        +buscar(valor, clave) Juego
        +inorder() list
        +preorder() list
        +postorder() list
        +altura() int
    }

    class AVL {
        -raiz: NodoAVL
        +insertar(dato, clave) None
        +buscar(valor, clave) Juego
        +inorder() list
        +altura() int
    }

    class ArbolGeneral {
        -raiz: NodoGeneral
        +insertar_raiz(dato) NodoGeneral
        +agregar_hijo(padre, dato) NodoGeneral
        +buscar(valor) NodoGeneral
        +amplitud() list
        +profundidad_preorder() list
        +obtener_niveles() list
    }

    class Grafo {
        -adyacencia: dict
        +agregar_vertice(v) None
        +agregar_arista(a, b, peso) None
        +hay_arista(a, b) bool
        +peso(a, b) float
        +vecinos(v) list
        +grado(v) int
        +cantidad_vertices() int
        +cantidad_aristas() int
    }

    class ServiciosJuegos {
        <<modulo>>
        +agregar_juego(nombre, generos, tiempo, catalogo, bst, avl)
        +comparar_tiempos(juegos) list
        +formatear_duracion(minutos) str
    }

    class ServiciosCategorias {
        <<modulo>>
        +construir_arbol_categorias(catalogo) ArbolGeneral
        +generos_validos() list
    }

    class ServiciosRelaciones {
        <<modulo>>
        +construir_grafo_relacionados(catalogo) Grafo
        +incorporar_juego(grafo, catalogo, juego) int
        +juegos_relacionados(grafo, juego) list
        +similitud(generos_a, generos_b, pesos) float
    }

    class RecorridosBFS {
        <<modulo>>
        +bfs(grafo, inicio, max_saltos) list
        +bfs_saltos_entre(grafo, origen, destino) int
    }

    class RecorridosDFS {
        <<modulo>>
        +dfs(grafo, inicio) list
        +componentes_conexas(grafo) list
    }

    Catalogo "1" o-- "*" Juego : contiene
    ArbolBST "1" o-- "*" Juego : ordena por nombre
    AVL "1" o-- "*" Juego : ordena por nombre
    ServiciosJuegos ..> Catalogo : agrega en
    ServiciosJuegos ..> ArbolBST : agrega en
    ServiciosJuegos ..> AVL : agrega en
    ServiciosCategorias ..> ArbolGeneral : construye
    ServiciosRelaciones ..> Grafo : construye
    ServiciosRelaciones ..> Catalogo : lee
    Grafo "1" o-- "*" Juego : un vértice por juego
    RecorridosBFS ..> Grafo : recorre
    RecorridosDFS ..> Grafo : recorre
```

## Cómo leerlo

- `Juego` es el dato central. Hay **un solo objeto `Juego` por juego**, y lo comparten el catálogo, el BST,
  el AVL y el grafo. `agregar_juego` actualiza el catálogo y los dos árboles; después `incorporar_juego`
  lo suma al grafo.
- `Catalogo` guarda los juegos en una lista (para listar y filtrar) y en un diccionario por `appid` (para
  detectar repetidos en O(1)).
- `ArbolBST` y `AVL` reciben una **función clave** (`lambda j: j.get_nombre().lower()`) para saber por qué
  atributo ordenar. Los nodos internos (`NodoArbol`, `NodoAVL`) no se muestran para no recargar el diagrama.
- `ArbolGeneral` guarda solo **nombres de categorías**. Para saber qué juegos tiene un género, la interfaz
  le pregunta al `Catalogo`.
- Los módulos de `servicios/` son funciones sueltas, no clases. Se dibujan como `<<modulo>>` para mostrar
  de qué estructuras dependen.
- `Grafo` es no dirigido y pesado, con lista de adyacencia. Cada vértice es un `Juego`; el peso de cada arista
  es la distancia entre dos juegos (0 = mismos géneros, 1 = nada en común). Ver `docs/09-analisis-tp7.md`.
- `RecorridosBFS` y `RecorridosDFS` (`algoritmos/bfs.py` y `dfs.py`) son funciones sueltas que reciben el
  `Grafo` por parámetro y no lo modifican. BFS usa una cola y DFS una pila. Ver `docs/10-analisis-tp8.md`.
- La interfaz (`ui/terminal.py`) no se dibuja: recibe todos los objetos por parámetro desde `main.py`.

## Lo que viene

Las estructuras de los próximos TP (heap y camino mínimo) se agregan acá cuando existan, con su relación con
`Catalogo`.
