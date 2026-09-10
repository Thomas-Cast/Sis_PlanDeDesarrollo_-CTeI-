"""
Etapa.py
Define las etapas del ciclo de vida (protocolo) de un proyecto de innovación.
Se implementa como una enumeración para tener valores controlados.
"""

from enum import Enum


class Etapa(Enum):
    """Enumeración de las etapas del protocolo de un proyecto."""
    CONCEPCION   = "Concepcion"
    FORMULACION  = "Formulacion"
    EVALUACION   = "Evaluacion"
    CONTRATACION = "Contratacion"
    EJECUCION    = "Ejecucion"
    CIERRE       = "Cierre"
    COMPLETADO   = "Completado"

    def __str__(self):
        """Permite imprimir la etapa como texto legible."""
        return self.value

    @staticmethod
    def orden():
        """Retorna la lista de etapas en orden secuencial."""
        return [
            Etapa.CONCEPCION,
            Etapa.FORMULACION,
            Etapa.EVALUACION,
            Etapa.CONTRATACION,
            Etapa.EJECUCION,
            Etapa.CIERRE,
            Etapa.COMPLETADO
        ]