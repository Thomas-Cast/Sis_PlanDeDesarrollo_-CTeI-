"""
linked_list.py
Prototipo de lista doblemente enlazada circular con centinela.
Incluye operaciones basicas y persistencia (opcional).
"""

import csv
import json
import sqlite3
from typing import Any, Callable, Optional, Iterator, List


class Node:
    def __init__(self, data: Any = None):
        self.data = data
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None


class DoublyCircularLinkedList:
    """Lista doblemente enlazada circular con nodo centinela."""

    def __init__(self):
        self.sentinel = Node()
        self.sentinel.next = self.sentinel
        self.sentinel.prev = self.sentinel
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def _insert_between(self, data: Any, left: Node, right: Node) -> Node:
        node = Node(data)
        node.prev = left
        node.next = right
        left.next = node
        right.prev = node
        self._size += 1
        return node

    def push_front(self, data: Any) -> Node:
        return self._insert_between(data, self.sentinel, self.sentinel.next)

    def push_back(self, data: Any) -> Node:
        return self._insert_between(data, self.sentinel.prev, self.sentinel)

    def find(self, predicate: Callable[[Any], bool]) -> Optional[Node]:
        cur = self.sentinel.next
        while cur is not self.sentinel:
            if predicate(cur.data):
                return cur
            cur = cur.next
        return None

    def remove_node(self, node: Node) -> Any:
        if node is self.sentinel:
            raise ValueError("No se puede eliminar el nodo centinela")
        node.prev.next = node.next
        node.next.prev = node.prev
        data = node.data
        node.prev = node.next = node.data = None
        self._size -= 1
        return data

    def remove_first(self) -> Any:
        if self.is_empty():
            raise IndexError("remove_first from empty list")
        return self.remove_node(self.sentinel.next)

    def remove_last(self) -> Any:
        if self.is_empty():
            raise IndexError("remove_last from empty list")
        return self.remove_node(self.sentinel.prev)

    def to_list_forward(self) -> list:
        res = []
        cur = self.sentinel.next
        while cur is not self.sentinel:
            res.append(cur.data)
            cur = cur.next
        return res

    def to_list_backward(self) -> list:
        res = []
        cur = self.sentinel.prev
        while cur is not self.sentinel:
            res.append(cur.data)
            cur = cur.prev
        return res

    def __iter__(self) -> Iterator[Any]:
        cur = self.sentinel.next
        while cur is not self.sentinel:
            yield cur.data
            cur = cur.next

    def clear(self) -> None:
        self.sentinel.next = self.sentinel.prev = self.sentinel
        self._size = 0

    # --- Persistencia (opcional, se mantiene por si se necesita) ---
    def save_to_json(self, path: str) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_list_forward(), f, ensure_ascii=False, indent=2)

    def load_from_json(self, path: str) -> None:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.clear()
        for item in data:
            self.push_back(item)

    def save_to_sqlite(self, db_path: str, table: str = 'Iniciativa_CTeI') -> None:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id TEXT PRIMARY KEY,
                nombre TEXT,
                meta INTEGER,
                municipio TEXT,
                actor TEXT,
                grupo TEXT
            )
        """)
        for item in self.to_list_forward():
            vals = (
                str(item.get('id', '')),
                item.get('nombre', ''),
                int(item.get('meta', 0)) if str(item.get('meta', '')).isdigit() else 0,
                item.get('municipio', ''),
                item.get('actor', ''),
                item.get('grupo', ''),
            )
            cur.execute(f"INSERT OR REPLACE INTO {table} (id,nombre,meta,municipio,actor,grupo) VALUES (?,?,?,?,?,?)", vals)
        conn.commit()
        conn.close()

    def load_from_sqlite(self, db_path: str, table: str = 'Iniciativa_CTeI') -> None:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f"SELECT id,nombre,meta,municipio,actor,grupo FROM {table}")
        rows = cur.fetchall()
        conn.close()
        self.clear()
        for r in rows:
            item = {
                'id': r[0],
                'nombre': r[1],
                'meta': int(r[2]) if r[2] and str(r[2]).isdigit() else r[2],
                'municipio': r[3],
                'actor': r[4],
                'grupo': r[5],
            }
            self.push_back(item)


# --- Demostracion por consola (opcional) ---
def step_by_step_demo():
    print("Demostracion: Lista doblemente enlazada circular con centinela")
    lst = DoublyCircularLinkedList()
    iniciativas = [
        {"id": "SCT02", "nombre": "Investigacion capacidades CTel", "meta": 1,
         "municipio": "Bogota", "actor": "Gobernacion", "grupo": "Ciencias Sociales"},
        {"id": "SCT03", "nombre": "Red centros innovacion", "meta": 1,
         "municipio": "Soacha", "actor": "Universidad", "grupo": "Ingenieria"},
        {"id": "STI02", "nombre": "Capacitar en IA y blockchain", "meta": 30000,
         "municipio": "Zipaquira", "actor": "Empresa privada", "grupo": "Tecnologia"},
        {"id": "SCT08", "nombre": "Proyectos agropecuarios CTel", "meta": 2000,
         "municipio": "Facatativa", "actor": "Asociacion campesina", "grupo": "Agro"},
    ]
    for ini in iniciativas:
        lst.push_back(ini)
        print(f"Insertado: {ini['id']}")
    print("Lista actual:", lst.to_list_forward())
    print("Demostracion finalizada.")


if __name__ == '__main__':
    step_by_step_demo()