"""
ListaEnlazada.py
Implementación de una lista doblemente enlazada circular con nodo centinela.
Almacena objetos de tipo Iniciativa.
Incluye todos los métodos necesarios para el prototipo.
"""

from Nodo import Nodo
from Iniciativa import Iniciativa

class ListaEnlazada:
    """Lista doblemente enlazada circular con centinela."""

    def __init__(self):
        """Crea la lista vacía con un nodo centinela."""
        self.centinela = Nodo(None)        # Nodo centinela sin datos
        self.centinela.siguiente = self.centinela
        self.centinela.anterior = self.centinela
        self.tamano = 0

    def esta_vacia(self):
        """Retorna True si la lista no contiene elementos."""
        return self.tamano == 0

    def __len__(self):
        return self.tamano

    def insertar_al_frente(self, iniciativa):
        """
        Inserta una iniciativa al inicio (después del centinela).
        Complejidad: O(1)
        """
        nuevo = Nodo(iniciativa)
        # Enlazar nuevo entre centinela y el primer nodo
        nuevo.siguiente = self.centinela.siguiente
        nuevo.anterior = self.centinela
        self.centinela.siguiente.anterior = nuevo
        self.centinela.siguiente = nuevo
        self.tamano += 1

    def insertar_al_final(self, iniciativa):
        """
        Inserta una iniciativa al final (antes del centinela).
        Complejidad: O(1)
        """
        nuevo = Nodo(iniciativa)
        # Enlazar nuevo entre el último nodo y el centinela
        nuevo.anterior = self.centinela.anterior
        nuevo.siguiente = self.centinela
        self.centinela.anterior.siguiente = nuevo
        self.centinela.anterior = nuevo
        self.tamano += 1

    def buscar_por_codigo(self, codigo):
        """
        Busca un nodo cuya iniciativa tenga el código dado.
        Retorna el nodo o None si no se encuentra.
        Complejidad: O(n)
        """
        actual = self.centinela.siguiente
        while actual != self.centinela:
            if actual.iniciativa.codigo == codigo:
                return actual
            actual = actual.siguiente
        return None

    def eliminar_nodo(self, nodo):
        """
        Elimina un nodo específico de la lista.
        Retorna la iniciativa eliminada.
        Complejidad: O(1)
        """
        if nodo == self.centinela:
            raise ValueError("No se puede eliminar el centinela")
        # Desconectar el nodo
        nodo.anterior.siguiente = nodo.siguiente
        nodo.siguiente.anterior = nodo.anterior
        self.tamano -= 1
        iniciativa = nodo.iniciativa
        # Limpiar referencias del nodo para el recolector de basura
        nodo.anterior = None
        nodo.siguiente = None
        nodo.iniciativa = None
        return iniciativa

    def eliminar_primero(self):
        """Elimina el primer nodo (después del centinela)."""
        if self.esta_vacia():
            raise IndexError("Lista vacía")
        return self.eliminar_nodo(self.centinela.siguiente)

    def eliminar_ultimo(self):
        """Elimina el último nodo (antes del centinela)."""
        if self.esta_vacia():
            raise IndexError("Lista vacía")
        return self.eliminar_nodo(self.centinela.anterior)

    def recorrer_adelante(self):
        """
        Retorna una lista de iniciativas en orden de adelante hacia atrás.
        Útil para mostrar en la tabla y en el lienzo.
        """
        resultado = []
        actual = self.centinela.siguiente
        while actual != self.centinela:
            resultado.append(actual.iniciativa)
            actual = actual.siguiente
        return resultado

    def recorrer_atras(self):
        """
        Retorna una lista de iniciativas en orden inverso.
        Demuestra la capacidad bidireccional de la lista.
        """
        resultado = []
        actual = self.centinela.anterior
        while actual != self.centinela:
            resultado.append(actual.iniciativa)
            actual = actual.anterior
        return resultado

    def limpiar(self):
        """Elimina todos los nodos (deja la lista vacía)."""
        self.centinela.siguiente = self.centinela
        self.centinela.anterior = self.centinela
        self.tamano = 0