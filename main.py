from servicios.cargador_datos import cargar_catalogo

catalogo = cargar_catalogo()

print(f"Juegos cargados: {catalogo.cantidad()}")

# Prueba: buscar un juego (poné acá el nombre de algún juego real que sepas
# que está en tu muestra de datos/games.json)
resultado = catalogo.buscar("Portal 2")
print(resultado)

print(catalogo.filtrar_por_categoria("Action")[:5])  # primeros 5 de acción