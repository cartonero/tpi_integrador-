from servicios.cargador_datos import cargar_catalogo
from ui.terminal import iniciar

catalogo = cargar_catalogo()
iniciar(catalogo)