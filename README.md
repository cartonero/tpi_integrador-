# JuegoTeca

Sistema de recomendación de videojuegos que permite buscar, listar y filtrar
juegos por categoría, usando datos reales del **Steam Games Dataset**

## Integrantes

- Rodrigo Cruz Choque
- Ian Martinez
- Milagros Ponce 

## Instalación 

```bash 
git clone https://github.com/cartonero/tpi_integrador-.git 
cd juegoteca
python3 --version   # requiere Python 3.10+ 
``` 

## Ejecución 

```bash 
py main.py 
``` 

## Estructura del repositorio 

| Carpeta | Contenido | 
|---|---|
| `modelos/` | Clases del dominio (`Juego`, `Catalogo`) | 
| `algoritmos/` | Búsquedas, BFS/DFS, caminos mínimos | 
| `datos/` | Datasets de prueba (JSON) | 
| `servicios/` | Lógica de negocio (recomendador) | 
| `ui/` | Interfaz de terminal | 
| `docs/` | Documentación del proyecto | 

## Documentación

- [Requerimientos](docs/01-requerimientos.md) - [Casos de uso](docs/02-casos-de-uso.md) - [Diagrama de clases](docs/03-diagrama-clases.md) - [Conexión entre estructuras](docs/04-diagrama-datos.md) - [Gestión del proyecto](docs/05-gestion-proyecto.md) 

## Estado del proyecto 

✅ TP0 · ✅ TP1 
