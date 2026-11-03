"""
servicios/juegos.py — Operaciones sobre juegos (duración, comparación y alta).

Reúne la lógica de las funcionalidades que trabajan con el tiempo de juego,
separada de la interfaz: este módulo no imprime ni pide datos (eso lo hace
ui/terminal.py), solo recibe datos y devuelve resultados.

"Duración estimada" es el tiempo de juego PROMEDIO que registra Steam para
cada juego (en minutos). No es el tiempo que lleva completarlo, y muchos
juegos no tienen el dato (figuran con 0).
"""


def formatear_duracion(minutos):
    """Convierte minutos a un texto legible: '45 min', '3 h' o '3 h 52 min'.

    Si no hay datos (0 minutos o menos) devuelve 'sin datos'.
    """
    if minutos <= 0:
        return "sin datos"

    # divmod(a, b) devuelve (cociente, resto): minutos // 60 y minutos % 60.
    horas, resto = divmod(minutos, 60)
    if horas == 0:
        return f"{resto} min"
    if resto == 0:
        return f"{horas} h"
    return f"{horas} h {resto} min"