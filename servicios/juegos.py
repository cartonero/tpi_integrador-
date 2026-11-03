"""
servicios/juegos.py — Operaciones sobre juegos (duración, comparación y alta).

Reúne la lógica de las funcionalidades que trabajan con el tiempo de juego,
separada de la interfaz: este módulo no imprime ni pide datos (eso lo hace
ui/terminal.py), solo recibe datos y devuelve resultados.

Funciones:
    - formatear_duracion: convierte minutos a texto legible.
    - comparar_tiempos: separa y ordena juegos según su tiempo de juego.

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


def comparar_tiempos(juegos):
    """Prepara una lista de juegos para compararlos por tiempo de juego.

    Devuelve una tupla (con_datos, sin_datos):
      - con_datos: los juegos que tienen duración, ordenados de MENOR a MAYOR.
      - sin_datos: los juegos sin duración (no se pueden comparar).

    Si dos juegos tienen el mismo tiempo, conservan el orden en que llegaron.
    """
    # Se separan en dos listas según tengan o no tengan dato de duración.
    con_datos = [j for j in juegos if j.tiene_tiempo()]
    sin_datos = [j for j in juegos if not j.tiene_tiempo()]

    # sort() ordena la lista de menor a mayor usando como criterio los
    # minutos de cada juego (key). Es estable: respeta el orden en los empates.
    con_datos.sort(key=lambda j: j.get_tiempo_min())
    return con_datos, sin_datos