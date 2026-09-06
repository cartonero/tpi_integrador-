# Diagrama inicial de clases

> Estado: boceto TP0. Se actualiza en TP1 con la implementación real.

\`\`\`mermaid
classDiagram
    class Juego {
        -nombre: str
        -categoria: str
        -tiempo_estimado: float
        -rating: float
        +get_nombre() str
        +get_tiempo_estimado() float
        +get_rating() float
    }
    class Categoria {
        -nombre: str
        -juegos: list
    }
    class Catalogo {
        -juegos: list
        +buscar(nombre) Juego
        +agregar(juego) void
        +listar_por_categoria(categoria) list
    }
    Catalogo "1" o-- "*" Juego : contiene
    Catalogo "1" o-- "*" Categoria : organiza
    Categoria "1" o-- "*" Juego : agrupa
\`\`\`