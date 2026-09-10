"""
Paso.py
Representa un paso del protocolo de un proyecto.
Estados: Pendiente -> En curso -> Completado
"""

import time


class Paso:
    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = "Pendiente"
        self.fecha = None
        self.observacion = ""

    def marcar_en_curso(self):
        self.estado = "En curso"

    def completar(self, observacion=""):
        self.estado = "Completado"
        self.fecha = time.strftime("%Y-%m-%d %H:%M")
        self.observacion = observacion

    def reiniciar(self):
        self.estado = "Pendiente"
        self.fecha = None
        self.observacion = ""

    def __str__(self):
        return f"{self.nombre} [{self.estado}]"