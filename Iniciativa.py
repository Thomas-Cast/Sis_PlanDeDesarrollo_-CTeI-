"""
Iniciativa.py
Clase que representa un proyecto de innovación de la apuesta CTeI.
Cada iniciativa tiene: código, nombre, meta numérica, municipio, actor y grupo.
"""

class Iniciativa:
    """Clase que modela una iniciativa de Ciencia, Tecnología e Innovación."""

    def __init__(self, codigo, nombre, meta, municipio, actor, grupo):
        """
        Constructor de la iniciativa.
        :param codigo: str, identificador único (ej. SCT02)
        :param nombre: str, nombre descriptivo del proyecto
        :param meta: int, valor numérico de la meta (ej. 30000)
        :param municipio: str, municipio donde se ejecuta
        :param actor: str, entidad responsable (Gobernación, Universidad, etc.)
        :param grupo: str, área de conocimiento o grupo asociado
        """
        self.codigo = codigo
        self.nombre = nombre
        self.meta = meta
        self.municipio = municipio
        self.actor = actor
        self.grupo = grupo

    def __str__(self):
        """Representación legible para depuración."""
        return f"Iniciativa({self.codigo}, {self.nombre}, meta={self.meta})"

    def to_dict(self):
        """Convierte la iniciativa a diccionario para exportar a JSON."""
        return {
            "id": self.codigo,
            "nombre": self.nombre,
            "meta": self.meta,
            "municipio": self.municipio,
            "actor": self.actor,
            "grupo": self.grupo
        }

    @staticmethod
    def from_dict(dic):
        """Crea una Iniciativa desde un diccionario (para cargar JSON)."""
        return Iniciativa(
            dic.get("id", ""),
            dic.get("nombre", ""),
            dic.get("meta", 0),
            dic.get("municipio", ""),
            dic.get("actor", ""),
            dic.get("grupo", "")
        )