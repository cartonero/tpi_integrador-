# Diagrama de clases

> Estado: implementación real (TP1). Boceto original del TP0 reemplazado.

\`\`\`mermaid
classDiagram
    class Juego {
        -appid: str
        -nombre: str
        -generos: list
        -tiempo_estimado_min: float
        -positivos: int
        -negativos: int
        +get_appid() str
        +get_nombre() str
        +get_generos() list
        +get_categoria_principal() str
        +get_tiempo_estimado_horas() float
        +get_rating_porcentaje() float
    }
    class Catalogo {
        -juegos: list
        +agregar(juego) bool
        +buscar(nombre) Juego
        +buscar_por_appid(appid) Juego
        +listar() list
        +filtrar_por_categoria(categoria) list
        +cantidad() int
    }
    Catalogo "1" o-- "*" Juego : contiene
\`\`\`