"""
app_gui.py
Interfaz grafica con tres paneles:
- Izquierda: formulario de entrada (con autocompletado al seleccionar codigo)
- Centro: lienzo con zoom y desplazamiento para visualizar la lista enlazada
- Derecha: pestañas para tabla de datos (con los codigos reales) y registro de eventos
Ademas incluye graficos, exportacion/importacion, alertas y demo paso a paso.

Autor: Estudiante
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import importlib

from linked_list import DoublyCircularLinkedList

# ------------------------------------------------------------
# Datos de referencia para autocompletar (basados en las tablas)
# ------------------------------------------------------------
DATOS_REFERENCIA = {
    "SCT02": {
        "nombre": "Investigacion sobre capacidades CTel de las provincias",
        "meta": 1,
        "municipio": "Bogota",
        "actor": "Gobernacion",
        "grupo": "Ciencias Sociales"
    },
    "SCT03": {
        "nombre": "Consolidar red de centros de innovacion y emprendimientos",
        "meta": 1,
        "municipio": "Soacha",
        "actor": "Universidad",
        "grupo": "Ingenieria"
    },
    "SCT04": {
        "nombre": "Apoyar proyecto para Parque Regional de Innovacion",
        "meta": 1,
        "municipio": "Zipaquira",
        "actor": "Gobernacion",
        "grupo": "Ciencias Sociales"
    },
    "SCT05": {
        "nombre": "Implementar red de Mentores para emprendedores",
        "meta": 1,
        "municipio": "Facatativa",
        "actor": "Empresa privada",
        "grupo": "Innovacion social"
    },
    "SCT06": {
        "nombre": "Beneficiar empresas con proyectos CTel para sofisticacion",
        "meta": 200,
        "municipio": "Bogota",
        "actor": "Gobernacion",
        "grupo": "Ciencias Sociales"
    },
    "SCT08": {
        "nombre": "Proyectos agropecuarios con CTel para produccion sostenible",
        "meta": 2000,
        "municipio": "Facatativa",
        "actor": "Asociacion campesina",
        "grupo": "Agro"
    },
    "SCT09": {
        "nombre": "Incorporar tecnologias ambientales y renovables",
        "meta": 180,
        "municipio": "Girardot",
        "actor": "ONG",
        "grupo": "Tecnologia"
    },
    "SCT10": {
        "nombre": "Becas de formacion doctoral",
        "meta": 20,
        "municipio": "Bogota",
        "actor": "Universidad",
        "grupo": "Ciencias Sociales"
    },
    "SCT11": {
        "nombre": "Becas de formacion para maestrias",
        "meta": 100,
        "municipio": "Bogota",
        "actor": "Universidad",
        "grupo": "Ciencias Sociales"
    },
    "SCT13": {
        "nombre": "Impulsar semilleros de investigacion temprana",
        "meta": 15,
        "municipio": "Zipaquira",
        "actor": "Alcaldia",
        "grupo": "Innovacion social"
    },
    "SCT14": {
        "nombre": "Registro de productos de investigacion o propiedad industrial",
        "meta": 90,
        "municipio": "Bogota",
        "actor": "Gobernacion",
        "grupo": "Ciencias Sociales"
    },
    "STI02": {
        "nombre": "Capacitar en IA, Blockchain y habilidades digitales",
        "meta": 30000,
        "municipio": "Zipaquira",
        "actor": "Empresa privada",
        "grupo": "Tecnologia"
    },
    "STI07": {
        "nombre": "Participar en desarrollo de centros de inteligencia artificial",
        "meta": 3,
        "municipio": "Bogota",
        "actor": "Universidad",
        "grupo": "Tecnologia"
    }
}

# ------------------------------------------------------------
# Configuracion del dibujo
# ------------------------------------------------------------
NODE_WIDTH = 200
NODE_HEIGHT = 80
PADDING_X = 40
PADDING_Y = 60
ZOOM_FACTOR = 1.1


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Gestor de Iniciativas CTeI - Cundinamarca")
        root.geometry("1300x800")

        self.lst = DoublyCircularLinkedList()

        # ---------- Panel izquierdo: formulario ----------
        left_frame = ttk.LabelFrame(root, text="Datos de la iniciativa", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        # Codigo (con evento para autocompletar)
        ttk.Label(left_frame, text="Codigo:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.code_var = tk.StringVar()
        self.code_entry = ttk.Entry(left_frame, textvariable=self.code_var, width=15)
        self.code_entry.grid(row=0, column=1, pady=3)
        self.code_entry.bind("<KeyRelease>", self.on_code_change)  # autocompletar al escribir

        # Nombre
        ttk.Label(left_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.name_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.name_var, width=30).grid(row=1, column=1, pady=3)

        # Meta
        ttk.Label(left_frame, text="Meta (numero):").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.meta_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.meta_var, width=10).grid(row=2, column=1, pady=3, sticky=tk.W)

        # Municipio (combo)
        ttk.Label(left_frame, text="Municipio:").grid(row=3, column=0, sticky=tk.W, pady=3)
        self.municipio_var = tk.StringVar()
        municipios = ["Bogota", "Soacha", "Zipaquira", "Facatativa", "Girardot",
                      "Chia", "Cajica", "Fusagasuga", "Otro"]
        self.municipio_combo = ttk.Combobox(left_frame, textvariable=self.municipio_var,
                                            values=municipios, width=20, state="readonly")
        self.municipio_combo.grid(row=3, column=1, pady=3)
        self.municipio_combo.current(0)

        # Actor (combo)
        ttk.Label(left_frame, text="Actor:").grid(row=4, column=0, sticky=tk.W, pady=3)
        self.actor_var = tk.StringVar()
        actores = ["Gobernacion", "Universidad", "Empresa privada", "Asociacion campesina",
                   "Alcaldia", "ONG", "Otro"]
        self.actor_combo = ttk.Combobox(left_frame, textvariable=self.actor_var,
                                        values=actores, width=20, state="readonly")
        self.actor_combo.grid(row=4, column=1, pady=3)
        self.actor_combo.current(0)

        # Grupo (combo)
        ttk.Label(left_frame, text="Grupo:").grid(row=5, column=0, sticky=tk.W, pady=3)
        self.grupo_var = tk.StringVar()
        grupos = ["Ciencias Sociales", "Ingenieria", "Ciencias Medicas",
                  "Tecnologia", "Agro", "Innovacion social", "Otro"]
        self.grupo_combo = ttk.Combobox(left_frame, textvariable=self.grupo_var,
                                        values=grupos, width=20, state="readonly")
        self.grupo_combo.grid(row=5, column=1, pady=3)
        self.grupo_combo.current(0)

        # Botones de operacion
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Insertar al frente", command=self.add_front).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Insertar al final", command=self.add_back).pack(side=tk.LEFT, padx=2)

        btn_frame2 = ttk.Frame(left_frame)
        btn_frame2.grid(row=7, column=0, columnspan=2, pady=5)
        ttk.Button(btn_frame2, text="Buscar por codigo", command=self.find_node).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame2, text="Eliminar por codigo", command=self.remove_node_by_code).pack(side=tk.LEFT, padx=2)

        btn_frame3 = ttk.Frame(left_frame)
        btn_frame3.grid(row=8, column=0, columnspan=2, pady=5)
        ttk.Button(btn_frame3, text="Limpiar lista", command=self.clear_list).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame3, text="Demo paso a paso", command=self.start_demo_thread).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame3, text="Ver alertas", command=self.show_alerts).pack(side=tk.LEFT, padx=2)

        # ---------- Panel central: lienzo con scroll y zoom ----------
        canvas_frame = ttk.LabelFrame(root, text="Visualizacion de la lista enlazada", padding=5)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.canvas = tk.Canvas(canvas_frame, bg="#f0f8ff", highlightthickness=1,
                                highlightbackground="#aaa", width=500, height=500)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.canvas_width = 2000
        self.canvas_height = 2000
        self.canvas.config(scrollregion=(0, 0, self.canvas_width, self.canvas_height))

        # Zoom y arrastre
        self.zoom_level = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Control-MouseWheel>", self.on_zoom)
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.drag_start_x = 0
        self.drag_start_y = 0

        # ---------- Panel derecho: pestañas (Tabla, Log, Graficos) ----------
        right_frame = ttk.LabelFrame(root, text="Datos y analisis", padding=5)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.notebook = ttk.Notebook(right_frame, width=500, height=600)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña 1: Tabla de iniciativas
        tab_table = ttk.Frame(self.notebook)
        self.notebook.add(tab_table, text="Lista de iniciativas")

        # Treeview con las columnas
        columns = ("ID", "Nombre", "Meta", "Municipio", "Actor", "Grupo")
        self.tree = ttk.Treeview(tab_table, columns=columns, show="headings", height=20)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor=tk.W)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tree_scroll = ttk.Scrollbar(tab_table, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        # Al hacer clic en un elemento de la tabla, autocompletar el formulario
        self.tree.bind("<ButtonRelease-1>", self.on_table_select)

        # Pestaña 2: Registro de eventos
        tab_log = ttk.Frame(self.notebook)
        self.notebook.add(tab_log, text="Registro de eventos")

        self.log_text = tk.Text(tab_log, height=25, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll = ttk.Scrollbar(tab_log, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=log_scroll.set)

        # Pestaña 3: Graficos (opcional, requiere matplotlib)
        tab_charts = ttk.Frame(self.notebook)
        self.notebook.add(tab_charts, text="Graficos")

        # Combo para elegir tipo de grafico
        chart_ctrl_frame = ttk.Frame(tab_charts)
        chart_ctrl_frame.pack(fill=tk.X, pady=5)
        ttk.Label(chart_ctrl_frame, text="Tipo de grafico:").pack(side=tk.LEFT, padx=5)
        self.chart_var = tk.StringVar()
        self.chart_combo = ttk.Combobox(chart_ctrl_frame, textvariable=self.chart_var,
                                        values=("Conteo por grupo", "Suma de meta por municipio",
                                                "Distribucion por actor"), state="readonly", width=25)
        self.chart_combo.pack(side=tk.LEFT, padx=5)
        self.chart_combo.current(0)
        ttk.Button(chart_ctrl_frame, text="Actualizar grafico", command=self.draw_chart).pack(side=tk.LEFT, padx=5)

        # Contenedor para el grafico
        self.chart_container = ttk.Frame(tab_charts)
        self.chart_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._mpl = None

        # ---------- Barra de herramientas inferior (export/import) ----------
        toolbar = ttk.Frame(root)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=4)
        ttk.Button(toolbar, text="Exportar JSON", command=self.export_json).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Exportar CSV", command=self.export_csv).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Guardar SQLite", command=self.save_sqlite).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Cargar JSON", command=self.load_json).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Cargar CSV", command=self.load_csv).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Cargar SQLite", command=self.load_sqlite).pack(side=tk.LEFT, padx=2)

        # Variable para resaltar
        self.highlighted_code = None

        # Dibujar estado inicial
        self.draw_list()
        self.update_table()

    # ------------------------------------------------------------
    # Autocompletado
    # ------------------------------------------------------------
    def on_code_change(self, event):
        """Al escribir un codigo, si existe en DATOS_REFERENCIA, autocompleta."""
        code = self.code_var.get().strip()
        if code in DATOS_REFERENCIA:
            data = DATOS_REFERENCIA[code]
            self.name_var.set(data["nombre"])
            self.meta_var.set(str(data["meta"]))
            self.municipio_var.set(data["municipio"])
            self.actor_var.set(data["actor"])
            self.grupo_var.set(data["grupo"])
        else:
            # Si no coincide, no borramos lo que el usuario ya haya escrito
            pass

    def on_table_select(self, event):
        """Al seleccionar un elemento de la tabla, autocompletar el formulario."""
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]
        if values:
            codigo = values[0]
            self.code_var.set(codigo)
            # Activar autocompletado manualmente
            if codigo in DATOS_REFERENCIA:
                data = DATOS_REFERENCIA[codigo]
                self.name_var.set(data["nombre"])
                self.meta_var.set(str(data["meta"]))
                self.municipio_var.set(data["municipio"])
                self.actor_var.set(data["actor"])
                self.grupo_var.set(data["grupo"])

    # ------------------------------------------------------------
    # Log
    # ------------------------------------------------------------
    def log(self, msg: str) -> None:
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {msg}\n")
        self.log_text.see(tk.END)

    # ------------------------------------------------------------
    # Obtener datos del formulario
    # ------------------------------------------------------------
    def get_data(self) -> dict:
        code = self.code_var.get().strip()
        name = self.name_var.get().strip() or "(sin nombre)"
        meta_str = self.meta_var.get().strip()
        try:
            meta = int(meta_str) if meta_str else 0
        except ValueError:
            meta = 0
        municipio = self.municipio_var.get().strip()
        actor = self.actor_var.get().strip()
        grupo = self.grupo_var.get().strip()
        return {
            "id": code or f"N{int(time.time())}",
            "nombre": name,
            "meta": meta,
            "municipio": municipio,
            "actor": actor,
            "grupo": grupo
        }

    # ------------------------------------------------------------
    # Operaciones
    # ------------------------------------------------------------
    def add_front(self):
        data = self.get_data()
        if not data["id"]:
            messagebox.showwarning("Entrada", "Ingrese un codigo")
            return
        self.lst.push_front(data)
        self.log(f"Insertado al frente: {data['id']}")
        self.draw_list()
        self.update_table()

    def add_back(self):
        data = self.get_data()
        if not data["id"]:
            messagebox.showwarning("Entrada", "Ingrese un codigo")
            return
        self.lst.push_back(data)
        self.log(f"Insertado al final: {data['id']}")
        self.draw_list()
        self.update_table()

    def find_node(self):
        code = self.code_var.get().strip()
        if not code:
            messagebox.showwarning("Entrada", "Ingrese un codigo")
            return
        node = self.lst.find(lambda d: d and d.get('id') == code)
        if node:
            self.highlighted_code = code
            self.log(f"Encontrado: {code}")
        else:
            self.highlighted_code = None
            self.log(f"No encontrado: {code}")
        self.draw_list()

    def remove_node_by_code(self):
        code = self.code_var.get().strip()
        if not code:
            messagebox.showwarning("Entrada", "Ingrese un codigo")
            return
        node = self.lst.find(lambda d: d and d.get('id') == code)
        if node:
            removed = self.lst.remove_node(node)
            self.log(f"Eliminado: {removed.get('id')}")
            self.highlighted_code = None
            self.draw_list()
            self.update_table()
        else:
            self.log(f"No encontrado: {code}")

    def clear_list(self):
        self.lst.clear()
        self.log("Lista limpiada")
        self.highlighted_code = None
        self.draw_list()
        self.update_table()

    # ------------------------------------------------------------
    # Dibujo del lienzo (con zoom y scroll)
    # ------------------------------------------------------------
    def draw_list(self):
        self.canvas.delete("all")
        items = self.lst.to_list_forward()
        if not items:
            self.canvas.create_text(self.canvas_width//2, self.canvas_height//2,
                                    text="(lista vacia)", fill="gray", font=("Arial", 16))
            return

        scale = self.zoom_level
        ox = self.offset_x
        oy = self.offset_y

        colores_grupo = {
            "Ciencias Sociales": "#FFD1DC",
            "Ingenieria": "#B0D9FF",
            "Ciencias Medicas": "#C1E1C1",
            "Tecnologia": "#FCE6A9",
            "Agro": "#D4C4A8",
            "Innovacion social": "#E6CCFF",
            "Otro": "#D3D3D3"
        }

        x = PADDING_X * scale + ox
        y = PADDING_Y * scale + oy
        width = NODE_WIDTH * scale
        height = NODE_HEIGHT * scale
        positions = []

        for i, data in enumerate(items):
            x1 = x + i * (width + 20*scale)
            y1 = y
            x2 = x1 + width
            y2 = y1 + height

            grupo = data.get('grupo', 'Otro')
            fill = colores_grupo.get(grupo, "#def")
            if self.highlighted_code is not None and data.get('id') == self.highlighted_code:
                fill = "#FFD700"

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#333", width=2)
            font_size = max(6, int(9 * scale))
            texto = f"{data.get('id')}\n{data.get('nombre')}\nMeta: {data.get('meta')}"
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=texto,
                                    font=("Arial", font_size), justify=tk.CENTER)
            positions.append((x1, y1, x2, y2))

        for i in range(len(positions)-1):
            x1 = positions[i][2]
            y1 = (positions[i][1] + positions[i][3]) // 2
            x2 = positions[i+1][0]
            y2 = (positions[i+1][1] + positions[i+1][3]) // 2
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2, fill="#555")

        if len(positions) > 1:
            last = positions[-1]
            first = positions[0]
            lx = last[2]
            ly = (last[1] + last[3]) // 2
            fx = first[0]
            fy = (first[1] + first[3]) // 2
            midx = (lx + fx) / 2
            self.canvas.create_line(lx, ly, midx, ly - 70*scale, fx, fy,
                                    smooth=True, arrow=tk.LAST, width=2, fill="#777", dash=(4,2))

        self.canvas.config(scrollregion=(0, 0, self.canvas_width, self.canvas_height))

    # ------------------------------------------------------------
    # Zoom y arrastre
    # ------------------------------------------------------------
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_zoom(self, event):
        if event.delta > 0:
            self.zoom_level *= ZOOM_FACTOR
        else:
            self.zoom_level /= ZOOM_FACTOR
        self.zoom_level = max(0.2, min(5.0, self.zoom_level))
        self.draw_list()

    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.canvas.xview_scroll(-dx, "units")
        self.canvas.yview_scroll(-dy, "units")
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    # ------------------------------------------------------------
    # Tabla
    # ------------------------------------------------------------
    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.lst.to_list_forward():
            self.tree.insert("", tk.END, values=(
                item.get('id', ''),
                item.get('nombre', ''),
                item.get('meta', 0),
                item.get('municipio', ''),
                item.get('actor', ''),
                item.get('grupo', '')
            ))

    # ------------------------------------------------------------
    # Alertas
    # ------------------------------------------------------------
    def show_alerts(self):
        items = self.lst.to_list_forward()
        if not items:
            messagebox.showinfo("Alertas", "No hay iniciativas")
            return
        umbral = 1000
        alertas = []
        for item in items:
            meta = item.get('meta', 0)
            if isinstance(meta, str):
                try:
                    meta = int(meta)
                except:
                    meta = 0
            if meta > umbral:
                alertas.append(f"{item.get('id')} - {item.get('nombre')}: meta {meta}")
        if alertas:
            messagebox.showwarning("Alertas de meta", "\n".join(alertas))
        else:
            messagebox.showinfo("Alertas", "Sin alertas")

    # ------------------------------------------------------------
    # Demo paso a paso
    # ------------------------------------------------------------
    def start_demo_thread(self):
        t = threading.Thread(target=self.demo_sequence, daemon=True)
        t.start()

    def demo_sequence(self):
        self.log("Iniciando demo...")
        self.lst.clear()
        self.root.after(0, self.draw_list)
        self.root.after(0, self.update_table)
        time.sleep(0.6)

        ejemplos = [
            {"id": "SCT02", "nombre": "Investigacion capacidades CTel", "meta": 1,
             "municipio": "Bogota", "actor": "Gobernacion", "grupo": "Ciencias Sociales"},
            {"id": "SCT03", "nombre": "Red centros innovacion", "meta": 1,
             "municipio": "Soacha", "actor": "Universidad", "grupo": "Ingenieria"},
            {"id": "STI02", "nombre": "Capacitar en IA y blockchain", "meta": 30000,
             "municipio": "Zipaquira", "actor": "Empresa privada", "grupo": "Tecnologia"},
            {"id": "SCT08", "nombre": "Proyectos agropecuarios CTel", "meta": 2000,
             "municipio": "Facatativa", "actor": "Asociacion campesina", "grupo": "Agro"},
        ]
        for ini in ejemplos:
            self.lst.push_back(ini)
            self.log(f"Insertado: {ini['id']}")
            self.root.after(0, self.draw_list)
            self.root.after(0, self.update_table)
            time.sleep(0.8)

        prioridad = {"id": "PRI01", "nombre": "Laboratorio jovenes innovadores",
                     "meta": 250, "municipio": "Girardot", "actor": "Alcaldia",
                     "grupo": "Innovacion social"}
        self.lst.push_front(prioridad)
        self.log(f"Insertado al frente: {prioridad['id']}")
        self.root.after(0, self.draw_list)
        self.root.after(0, self.update_table)
        time.sleep(1.0)

        code = 'STI02'
        node = self.lst.find(lambda d: d and d.get('id') == code)
        if node:
            self.highlighted_code = code
            self.log(f"Busqueda: encontrado {code}")
        else:
            self.log(f"Busqueda: no encontrado {code}")
        self.root.after(0, self.draw_list)
        time.sleep(1.2)

        if node:
            removed = self.lst.remove_node(node)
            self.log(f"Eliminado: {removed.get('id')}")
            self.highlighted_code = None
            self.root.after(0, self.draw_list)
            self.root.after(0, self.update_table)
        time.sleep(1.0)

        if not self.lst.is_empty():
            first = self.lst.remove_first()
            time.sleep(0.4)
            last = None
            if not self.lst.is_empty():
                last = self.lst.remove_last()
            self.log(f"Eliminado primero: {first.get('id')}")
            if last:
                self.log(f"Eliminado ultimo: {last.get('id')}")
            self.root.after(0, self.draw_list)
            self.root.after(0, self.update_table)

        self.log("Demo finalizada")

    # ------------------------------------------------------------
    # Graficos (matplotlib)
    # ------------------------------------------------------------
    def _ensure_matplotlib(self):
        if self._mpl is not None:
            return
        try:
            mpl = importlib.import_module('matplotlib')
            mpl.use('Agg')
            pyplot = importlib.import_module('matplotlib.pyplot')
            Figure = importlib.import_module('matplotlib.figure').Figure
            tkagg = importlib.import_module('matplotlib.backends.backend_tkagg')
            self._mpl = {'mpl': mpl, 'pyplot': pyplot, 'Figure': Figure, 'tkagg': tkagg}
        except Exception:
            self._mpl = None
            raise

    def draw_chart(self):
        try:
            self._ensure_matplotlib()
        except Exception:
            messagebox.showerror("Error", "matplotlib no instalado")
            return

        kind = self.chart_var.get()
        pyplot = self._mpl['pyplot']
        Figure = self._mpl['Figure']
        tkagg = self._mpl['tkagg']

        items = self.lst.to_list_forward()
        for child in self.chart_container.winfo_children():
            child.destroy()

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        if kind == "Conteo por grupo":
            counts = {}
            for it in items:
                g = it.get('grupo') or 'Sin grupo'
                counts[g] = counts.get(g, 0) + 1
            ax.bar(counts.keys(), counts.values(), color='#4CAF50')
            ax.set_title('Conteo por grupo')
            ax.set_ylabel('Cantidad')
            ax.tick_params(axis='x', rotation=30)
        elif kind == "Suma de meta por municipio":
            sums = {}
            for it in items:
                m = it.get('municipio') or 'Sin municipio'
                try:
                    val = int(it.get('meta') or 0)
                except:
                    val = 0
                sums[m] = sums.get(m, 0) + val
            ax.bar(sums.keys(), sums.values(), color='#2196F3')
            ax.set_title('Suma de meta por municipio')
            ax.set_ylabel('Meta (sum)')
            ax.tick_params(axis='x', rotation=30)
        else:  # Distribucion por actor
            counts = {}
            for it in items:
                a = it.get('actor') or 'Sin actor'
                counts[a] = counts.get(a, 0) + 1
            ax.pie(counts.values(), labels=counts.keys(), autopct='%1.1f%%')
            ax.set_title('Distribucion por actor')

        fig.tight_layout()
        canvas = tkagg.FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------
    # Export/Import
    # ------------------------------------------------------------
    def export_json(self):
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON', '*.json')])
        if path:
            self.lst.save_to_json(path)
            self.log(f"Exportado JSON: {path}")

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV', '*.csv')])
        if path:
            self.lst.save_to_csv(path, fieldnames=['id','nombre','meta','municipio','actor','grupo'])
            self.log(f"Exportado CSV: {path}")

    def save_sqlite(self):
        path = filedialog.asksaveasfilename(defaultextension='.db', filetypes=[('SQLite', '*.db')])
        if path:
            self.lst.save_to_sqlite(path)
            self.log(f"Guardado SQLite: {path}")

    def load_json(self):
        path = filedialog.askopenfilename(filetypes=[('JSON', '*.json')])
        if path:
            self.lst.load_from_json(path)
            self.log(f"Cargado JSON: {path}")
            self.draw_list()
            self.update_table()

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[('CSV', '*.csv')])
        if path:
            self.lst.load_from_csv(path)
            self.log(f"Cargado CSV: {path}")
            self.draw_list()
            self.update_table()

    def load_sqlite(self):
        path = filedialog.askopenfilename(filetypes=[('SQLite', '*.db')])
        if path:
            self.lst.load_from_sqlite(path)
            self.log(f"Cargado SQLite: {path}")
            self.draw_list()
            self.update_table()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()