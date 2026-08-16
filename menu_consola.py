"""
menu_consola.py
Menu interactivo por consola (alternativa sin interfaz grafica).
"""
from linked_list import DoublyCircularLinkedList


def mostrar_menu():
    print("\n" + "="*60)
    print("   SISTEMA DE GESTION DE INICIATIVAS CTeI - CUNDINAMARCA")
    print("="*60)
    print("1. Insertar iniciativa al frente")
    print("2. Insertar iniciativa al final")
    print("3. Buscar iniciativa por codigo")
    print("4. Eliminar iniciativa por codigo")
    print("5. Listar todas las iniciativas")
    print("6. Estadisticas")
    print("7. Guardar datos (JSON)")
    print("8. Cargar datos (JSON)")
    print("9. Guardar en SQLite")
    print("10. Cargar desde SQLite")
    print("11. Limpiar lista")
    print("12. Salir")
    print("="*60)


def leer_datos():
    print("\nIngrese los datos de la iniciativa:")
    id_proy = input("Codigo (obligatorio): ").strip()
    if not id_proy:
        print("El codigo es obligatorio.")
        return None
    nombre = input("Nombre: ").strip() or "(sin nombre)"
    meta_str = input("Meta (numero): ").strip()
    try:
        meta = int(meta_str) if meta_str else 0
    except ValueError:
        meta = 0
    municipio = input("Municipio: ").strip()
    actor = input("Actor: ").strip()
    grupo = input("Grupo: ").strip()
    return {
        "id": id_proy,
        "nombre": nombre,
        "meta": meta,
        "municipio": municipio,
        "actor": actor,
        "grupo": grupo
    }


def listar_iniciativas(lst):
    if lst.is_empty():
        print("No hay iniciativas registradas.")
        return
    print("\n--- LISTA DE INICIATIVAS ---")
    for i, item in enumerate(lst.to_list_forward(), 1):
        print(f"{i}. ID: {item.get('id')} | Nombre: {item.get('nombre')} | Meta: {item.get('meta')} | "
              f"Municipio: {item.get('municipio')} | Actor: {item.get('actor')} | Grupo: {item.get('grupo')}")
    print(f"Total: {len(lst)} iniciativas.\n")


def estadisticas(lst):
    if lst.is_empty():
        print("No hay datos para estadisticas.")
        return
    items = lst.to_list_forward()
    grupos = {}
    metas_por_municipio = {}
    actores = {}
    for it in items:
        g = it.get('grupo') or 'Sin grupo'
        grupos[g] = grupos.get(g, 0) + 1
        m = it.get('municipio') or 'Sin municipio'
        try:
            meta_val = int(it.get('meta') or 0)
        except:
            meta_val = 0
        metas_por_municipio[m] = metas_por_municipio.get(m, 0) + meta_val
        a = it.get('actor') or 'Sin actor'
        actores[a] = actores.get(a, 0) + 1
    print("\n--- ESTADISTICAS ---")
    print("Conteo por grupo:")
    for g, cnt in grupos.items():
        print(f"  {g}: {cnt}")
    print("\nSuma de metas por municipio:")
    for m, total in metas_por_municipio.items():
        print(f"  {m}: {total}")
    print("\nDistribucion por actor:")
    for a, cnt in actores.items():
        print(f"  {a}: {cnt}")
    print(f"Total de iniciativas: {len(lst)}\n")


def main():
    lst = DoublyCircularLinkedList()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "1":
            data = leer_datos()
            if data:
                lst.push_front(data)
                print(f"Iniciativa {data['id']} insertada al frente.")
        elif opcion == "2":
            data = leer_datos()
            if data:
                lst.push_back(data)
                print(f"Iniciativa {data['id']} insertada al final.")
        elif opcion == "3":
            codigo = input("Ingrese el codigo a buscar: ").strip()
            if not codigo:
                print("Codigo vacio.")
                continue
            node = lst.find(lambda d: d and d.get('id') == codigo)
            if node:
                print(f"Encontrado: {node.data}")
            else:
                print(f"No encontrado: {codigo}")
        elif opcion == "4":
            codigo = input("Ingrese el codigo a eliminar: ").strip()
            if not codigo:
                print("Codigo vacio.")
                continue
            node = lst.find(lambda d: d and d.get('id') == codigo)
            if node:
                eliminado = lst.remove_node(node)
                print(f"Eliminado: {eliminado.get('id')}")
            else:
                print(f"No se encontro el codigo {codigo}")
        elif opcion == "5":
            listar_iniciativas(lst)
        elif opcion == "6":
            estadisticas(lst)
        elif opcion == "7":
            path = input("Nombre del archivo JSON: ").strip() or "datos.json"
            try:
                lst.save_to_json(path)
                print(f"Datos guardados en {path}")
            except Exception as e:
                print(f"Error: {e}")
        elif opcion == "8":
            path = input("Nombre del archivo JSON a cargar: ").strip()
            if not path:
                continue
            try:
                lst.load_from_json(path)
                print(f"Datos cargados desde {path}")
            except Exception as e:
                print(f"Error: {e}")
        elif opcion == "9":
            path = input("Nombre del archivo SQLite: ").strip() or "ctei.db"
            try:
                lst.save_to_sqlite(path)
                print(f"Datos guardados en SQLite: {path}")
            except Exception as e:
                print(f"Error: {e}")
        elif opcion == "10":
            path = input("Nombre del archivo SQLite a cargar: ").strip()
            if not path:
                continue
            try:
                lst.load_from_sqlite(path)
                print(f"Datos cargados desde SQLite: {path}")
            except Exception as e:
                print(f"Error: {e}")
        elif opcion == "11":
            lst.clear()
            print("Lista limpiada.")
        elif opcion == "12":
            print("Saliendo...")
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()