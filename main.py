from modelos.juego import Juego
from modelos.catalogo import Catalogo

catalogo = Catalogo()
catalogo.agregar(Juego("400", "Portal", ["Puzzle", "Sci-fi"], 300, 9000, 100))
catalogo.agregar(Juego("620", "Portal 2", ["Puzzle", "Sci-fi"], 600, 15000, 80))

print(catalogo.buscar("Portal"))
print(catalogo.filtrar_por_categoria("Puzzle"))