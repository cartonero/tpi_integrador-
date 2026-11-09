# Diagrama de clases

> Estado: TP5 más las funcionalidades de añadir, comparar y duración. Se actualiza en cada TP con la
> estructura nueva.

```mermaid
classDiagram
    class Juego {
        -appid: str
        -nombre: str
        -generos: list
        -tiempo_min: int
        +get_appid() str
        +get_nombre() str
        +get_generos() list
        +get_categoria_principal() str
        +get_tiempo_min() int
        +tiene_tiempo() bool
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

    Catalogo "1" o-- "*" Juego : contiene
    ArbolBST "1" o-- "*" Juego : ordena por nombre
    AVL "1" o-- "*" Juego : ordena por nombre
    ServiciosJuegos ..> Catalogo : agrega en
    ServiciosJuegos ..> ArbolBST : agrega en
    ServiciosJuegos ..> AVL : agrega en
    ServiciosCategorias ..> ArbolGeneral : construye
```

## Cómo leerlo

- `Juego` es el dato central. Hay **un solo objeto `Juego` por juego**, y lo comparten el catálogo, el BST
  y el AVL. Por eso `agregar_juego` los actualiza a los tres a la vez.
- `Catalogo` guarda los juegos en una lista (para listar y filtrar) y en un diccionario por `appid` (para
  detectar repetidos en O(1)).
- `ArbolBST` y `AVL` reciben una **función clave** (`lambda j: j.get_nombre().lower()`) para saber por qué
  atributo ordenar. Los nodos internos (`NodoArbol`, `NodoAVL`) no se muestran para no recargar el diagrama.
- `ArbolGeneral` guarda solo **nombres de categorías**. Para saber qué juegos tiene un género, la interfaz
  le pregunta al `Catalogo`.
- Los módulos de `servicios/` son funciones sueltas, no clases. Se dibujan como `<<modulo>>` para mostrar
  de qué estructuras dependen.
- La interfaz (`ui/terminal.py`) no se dibuja: recibe todos los objetos por parámetro desde `main.py`.

## Lo que viene

Las estructuras de los próximos TP (heap, grafo) se agregan acá cuando existan, con su relación con
`Catalogo`.
