"""
Nodo.py
Define el nodo de la lista doblemente enlazada.
Cada nodo contiene una Iniciativa y punteros al anterior y siguiente.
"""

from Iniciativa import Iniciativa

class Nodo:
    """Nodo de una lista doblemente enlazada."""

    def __init__(self, iniciativa):
        """
        Constructor del nodo.
        :param iniciativa: objeto de tipo Iniciativa.
        """
        self.iniciativa = iniciativa   # Dato almacenado (objeto Iniciativa)
        self.anterior = None           # Apuntador al nodo previo
        self.siguiente = None          # Apuntador al nodo siguiente