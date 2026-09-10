"""
ListaCircular.py
Lista circular simple ordenada por prioridad. El ultimo nodo apunta al primero.
"""

from Nodo import Nodo


class ListaCircular:
    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def esta_vacia(self):
        return self.cabeza is None

    def __len__(self):
        return self.tamano

    def insertar_ordenado(self, iniciativa):
        """Inserta manteniendo orden por prioridad (Alta > Media > Baja)."""
        nuevo = Nodo(iniciativa)

        if self.esta_vacia():
            self.cabeza = nuevo
            nuevo.siguiente = nuevo
            self.tamano += 1
            return

        # Prioridad más alta que la cabeza -> al frente
        if iniciativa.peso_prioridad() < self.cabeza.iniciativa.peso_prioridad():
            ultimo = self.cabeza
            while ultimo.siguiente != self.cabeza:
                ultimo = ultimo.siguiente
            ultimo.siguiente = nuevo
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
            self.tamano += 1
            return

        # Buscar posición en el medio
        actual = self.cabeza
        while actual.siguiente != self.cabeza:
            if iniciativa.peso_prioridad() < actual.siguiente.iniciativa.peso_prioridad():
                break
            actual = actual.siguiente

        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo
        self.tamano += 1

    def reordenar_por_prioridad(self):
        items = self.recorrer()
        items.sort(key=lambda x: x.peso_prioridad())
        self.limpiar()
        for it in items:
            self.insertar_ordenado(it)

    def buscar_por_codigo(self, codigo):
        if self.esta_vacia():
            return None
        actual = self.cabeza
        while True:
            if actual.iniciativa.codigo == codigo:
                return actual
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return None

    def eliminar_nodo(self, nodo):
        if self.esta_vacia():
            return None
        if self.tamano == 1:
            self.cabeza = None
            self.tamano = 0
            return nodo.iniciativa

        anterior = self.cabeza
        while anterior.siguiente != nodo:
            anterior = anterior.siguiente
            if anterior == self.cabeza:
                return None
        anterior.siguiente = nodo.siguiente
        if nodo == self.cabeza:
            self.cabeza = nodo.siguiente
        self.tamano -= 1
        nodo.siguiente = None
        return nodo.iniciativa

    def eliminar_por_codigo(self, codigo):
        nodo = self.buscar_por_codigo(codigo)
        if nodo:
            return self.eliminar_nodo(nodo)
        return None

    def obtener_actual(self):
        if self.esta_vacia():
            return None
        return self.cabeza.iniciativa

    def avanzar_turno_actual(self, observacion=""):
        """
        Aplica el siguiente paso al proyecto en turno (round-robin).
        Si finaliza, se elimina del ciclo.
        """
        if self.esta_vacia():
            return None, "Lista vacia", False

        actual = self.cabeza
        ini = actual.iniciativa
        paso_nombre = ini.paso_actual().nombre if ini.paso_actual() else "-"

        finalizado = ini.avanzar_paso(observacion)

        if finalizado:
            self.eliminar_nodo(actual)
            return ini, f"{ini.codigo}: '{paso_nombre}' completado -> PROYECTO FINALIZADO", True
        else:
            self.cabeza = self.cabeza.siguiente
            nuevo_paso = ini.paso_actual().nombre if ini.paso_actual() else "-"
            return ini, f"{ini.codigo}: '{paso_nombre}' completado -> pasa a '{nuevo_paso}'", False

    def mover_cabeza_a(self, codigo):
        """Coloca la cabeza en el nodo con ese codigo (para 'siguiente turno')."""
        nodo = self.buscar_por_codigo(codigo)
        if nodo:
            self.cabeza = nodo
            return True
        return False

    def recorrer(self):
        resultado = []
        if self.esta_vacia():
            return resultado
        actual = self.cabeza
        while True:
            resultado.append(actual.iniciativa)
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return resultado

    def limpiar(self):
        self.cabeza = None
        self.tamano = 0