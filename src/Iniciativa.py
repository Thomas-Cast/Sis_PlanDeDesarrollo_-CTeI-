"""
Iniciativa.py
Representa un proyecto de innovacion de la apuesta CTeI.
Cada iniciativa tiene un protocolo con 5 pasos y control manual de avance.
"""

import time
from Paso import Paso


PRIORIDADES = {"Alta": 1, "Media": 2, "Baja": 3}


class Iniciativa:
    def __init__(self, codigo, nombre, meta, municipio, actor, grupo, prioridad="Media"):
        self.codigo = codigo
        self.nombre = nombre
        self.meta = meta
        self.municipio = municipio
        self.actor = actor
        self.grupo = grupo
        self.prioridad = prioridad
        self.fecha_ingreso = time.strftime("%Y-%m-%d %H:%M")

        self.pasos = [
            Paso("Radicacion"),
            Paso("Acta de inicio"),
            Paso("Contratacion"),
            Paso("Ejecucion"),
            Paso("Entrega / Final")
        ]
        self.pasos[0].marcar_en_curso()
        self.indice_paso = 0
        self.finalizado = False
        self.fecha_finalizacion = None

    def peso_prioridad(self):
        return PRIORIDADES.get(self.prioridad, 2)

    def paso_actual(self):
        if 0 <= self.indice_paso < len(self.pasos):
            return self.pasos[self.indice_paso]
        return None

    def avanzar_paso(self, observacion=""):
        """Completa el paso actual y pasa al siguiente. Retorna True si finalizó."""
        if self.finalizado:
            return True
        if self.indice_paso >= len(self.pasos):
            return True

        self.pasos[self.indice_paso].completar(observacion)
        self.indice_paso += 1

        if self.indice_paso >= len(self.pasos):
            self.finalizado = True
            self.fecha_finalizacion = time.strftime("%Y-%m-%d %H:%M")
            return True

        self.pasos[self.indice_paso].marcar_en_curso()
        return False

    def retroceder_paso(self):
        """Retrocede al paso anterior. Corrige errores."""
        if self.finalizado:
            self.finalizado = False
            self.fecha_finalizacion = None
            self.pasos[self.indice_paso - 1].marcar_en_curso()
            return True

        if self.indice_paso > 0:
            self.pasos[self.indice_paso].reiniciar()
            self.indice_paso -= 1
            self.pasos[self.indice_paso].reiniciar()
            self.pasos[self.indice_paso].marcar_en_curso()
            return True
        return False

    def forzar_finalizar(self, observacion="Finalizado manualmente"):
        """Fuerza la finalización del proyecto saltando pasos pendientes."""
        while not self.finalizado:
            self.avanzar_paso(observacion)
        return True

    def progreso(self):
        completados = sum(1 for p in self.pasos if p.estado == "Completado")
        return f"{completados}/{len(self.pasos)}"

    def __str__(self):
        return f"{self.codigo} - {self.nombre} [{self.prioridad}]"