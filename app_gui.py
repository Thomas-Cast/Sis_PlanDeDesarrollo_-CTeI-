"""
app_gui.py
Interfaz gráfica con tres paneles:
- Izquierda: formulario de entrada (con combos para municipio, actor, grupo)
- Centro: lienzo interactivo (zoom con Ctrl+rueda, desplazamiento con arrastre)
- Derecha: pestañas para tabla de datos y registro de eventos

Ahora utiliza las clases Iniciativa, Nodo y ListaEnlazada (Programación Orientada a Objetos).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

from Iniciativa import Iniciativa
from ListaEnlazada import ListaEnlazada

# ------------------------------------------------------------
# Configuración del dibujo
# ------------------------------------------------------------
ANCHO_NODO = 200
ALTO_NODO = 80
PADDING_X = 40
PADDING_Y = 60
ZOOM_FACTOR = 1.1

# Colores por grupo para distinguir visualmente los nodos
COLORES_GRUPO = {
    "Ciencias Sociales": "#FFD1DC",
    "Ingenieria": "#B0D9FF",
    "Ciencias Medicas": "#C1E1C1",
    "Tecnologia": "#FCE6A9",
    "Agro": "#D4C4A8",
    "Innovacion social": "#E6CCFF",
    "Otro": "#D3D3D3"
}

class App:
    def __init__(self, root):
        self.root = root
        root.title("Gestor de Iniciativas CTeI - Cundinamarca")
        root.geometry("1300x750")

        # Instancia de la lista enlazada (ahora con objetos Iniciativa)
        self.lista = ListaEnlazada()

        # ---------- Panel izquierdo: Formulario ----------
        left_frame = ttk.LabelFrame(root, text="Datos de la iniciativa", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        # Código
        ttk.Label(left_frame, text="Codigo:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.codigo_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.codigo_var, width=15).grid(row=0, column=1, pady=3)

        # Nombre
        ttk.Label(left_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.nombre_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.nombre_var, width=25).grid(row=1, column=1, pady=3)

        # Meta
        ttk.Label(left_frame, text="Meta (numero):").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.meta_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.meta_var, width=10).grid(row=2, column=1, pady=3, sticky=tk.W)

        # Municipio (Combo)
        ttk.Label(left_frame, text="Municipio:").grid(row=3, column=0, sticky=tk.W, pady=3)
        self.municipio_var = tk.StringVar()
        municipios = ["Bogota", "Soacha", "Zipaquira", "Facatativa", "Girardot",
                      "Chia", "Cajica", "Fusagasuga", "Otro"]
        self.municipio_combo = ttk.Combobox(left_frame, textvariable=self.municipio_var,
                                            values=municipios, width=20, state="readonly")
        self.municipio_combo.grid(row=3, column=1, pady=3)
        self.municipio_combo.current(0)

        # Actor (Combo)
        ttk.Label(left_frame, text="Actor:").grid(row=4, column=0, sticky=tk.W, pady=3)
        self.actor_var = tk.StringVar()
        actores = ["Gobernacion", "Universidad", "Empresa privada", "Asociacion campesina",
                   "Alcaldia", "ONG", "Otro"]
        self.actor_combo = ttk.Combobox(left_frame, textvariable=self.actor_var,
                                        values=actores, width=20, state="readonly")
        self.actor_combo.grid(row=4, column=1, pady=3)
        self.actor_combo.current(0)

        # Grupo (Combo)
        ttk.Label(left_frame, text="Grupo:").grid(row=5, column=0, sticky=tk.W, pady=3)
        self.grupo_var = tk.StringVar()
        grupos = ["Ciencias Sociales", "Ingenieria", "Ciencias Medicas",
                  "Tecnologia", "Agro", "Innovacion social", "Otro"]
        self.grupo_combo = ttk.Combobox(left_frame, textvariable=self.grupo_var,
                                        values=grupos, width=20, state="readonly")
        self.grupo_combo.grid(row=5, column=1, pady=3)
        self.grupo_combo.current(0)

        # Botones de operación
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Insertar al frente", command=self.insertar_frente).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Insertar al final", command=self.insertar_final).pack(side=tk.LEFT, padx=2)

        btn_frame2 = ttk.Frame(left_frame)
        btn_frame2.grid(row=7, column=0, columnspan=2, pady=5)
        ttk.Button(btn_frame2, text="Buscar por codigo", command=self.buscar).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame2, text="Eliminar por codigo", command=self.eliminar).pack(side=tk.LEFT, padx=2)

        btn_frame3 = ttk.Frame(left_frame)
        btn_frame3.grid(row=8, column=0, columnspan=2, pady=5)
        ttk.Button(btn_frame3, text="Limpiar lista", command=self.limpiar).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame3, text="Demo paso a paso", command=self.iniciar_demo).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame3, text="Ver alertas", command=self.mostrar_alertas).pack(side=tk.LEFT, padx=2)

        # ---------- Panel central: Lienzo con scroll y zoom ----------
        canvas_frame = ttk.LabelFrame(root, text="Visualizacion de la lista enlazada", padding=5)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.canvas = tk.Canvas(canvas_frame, bg="#f0f8ff", highlightthickness=1, highlightbackground="#aaa")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbars
        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Tamaño del área de dibujo (grande para permitir muchos nodos)
        self.canvas_ancho = 2000
        self.canvas_alto = 2000
        self.canvas.config(scrollregion=(0, 0, self.canvas_ancho, self.canvas_alto))

        # Variables para zoom y desplazamiento
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0

        # Eventos del mouse (zoom y pan)
        self.canvas.bind("<MouseWheel>", self.on_scroll)          # Desplazamiento vertical
        self.canvas.bind("<Control-MouseWheel>", self.on_zoom)    # Zoom con Ctrl
        self.canvas.bind("<ButtonPress-1>", self.iniciar_arrastre)
        self.canvas.bind("<B1-Motion>", self.arrastrar)

        self.drag_start_x = 0
        self.drag_start_y = 0

        # ---------- Panel derecho: Tabla y Registro (pestañas) ----------
        right_frame = ttk.LabelFrame(root, text="Datos y eventos", padding=5)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=8, pady=8)

        self.notebook = ttk.Notebook(right_frame, width=450, height=600)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña 1: Tabla de iniciativas
        tab_tabla = ttk.Frame(self.notebook)
        self.notebook.add(tab_tabla, text="Lista de iniciativas")
        self.tabla = ttk.Treeview(tab_tabla, columns=("Codigo", "Nombre", "Meta", "Municipio", "Actor", "Grupo"),
                                  show="headings", height=20)
        for col in ("Codigo", "Nombre", "Meta", "Municipio", "Actor", "Grupo"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=70, anchor=tk.W)
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_tabla = ttk.Scrollbar(tab_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        scroll_tabla.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla.configure(yscrollcommand=scroll_tabla.set)

        # Pestaña 2: Registro de eventos (Log)
        tab_log = ttk.Frame(self.notebook)
        self.notebook.add(tab_log, text="Registro de eventos")
        self.log_text = tk.Text(tab_log, height=25, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_log = ttk.Scrollbar(tab_log, orient=tk.VERTICAL, command=self.log_text.yview)
        scroll_log.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scroll_log.set)

        # Variable para resaltar un nodo
        self.codigo_resaltado = None

        # Dibujar estado inicial
        self.dibujar_lista()
        self.actualizar_tabla()

    # ------------------------------------------------------------
    # Funciones auxiliares: Log y obtención de datos
    # ------------------------------------------------------------
    def log(self, mensaje):
        """Agrega un mensaje al registro con timestamp."""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {mensaje}\n")
        self.log_text.see(tk.END)

    def obtener_iniciativa_desde_formulario(self):
        """Crea y retorna un objeto Iniciativa con los datos ingresados."""
        codigo = self.codigo_var.get().strip()
        nombre = self.nombre_var.get().strip() or "(sin nombre)"
        meta_str = self.meta_var.get().strip()
        try:
            meta = int(meta_str) if meta_str else 0
        except ValueError:
            meta = 0
        municipio = self.municipio_var.get().strip()
        actor = self.actor_var.get().strip()
        grupo = self.grupo_var.get().strip()
        return Iniciativa(codigo, nombre, meta, municipio, actor, grupo)

    # ------------------------------------------------------------
    # Operaciones de la interfaz
    # ------------------------------------------------------------
    def insertar_frente(self):
        ini = self.obtener_iniciativa_desde_formulario()
        if not ini.codigo:
            messagebox.showwarning("Entrada", "El codigo es obligatorio.")
            return
        self.lista.insertar_al_frente(ini)
        self.log(f"Insertado al frente: {ini.codigo}")
        self.dibujar_lista()
        self.actualizar_tabla()

    def insertar_final(self):
        ini = self.obtener_iniciativa_desde_formulario()
        if not ini.codigo:
            messagebox.showwarning("Entrada", "El codigo es obligatorio.")
            return
        self.lista.insertar_al_final(ini)
        self.log(f"Insertado al final: {ini.codigo}")
        self.dibujar_lista()
        self.actualizar_tabla()

    def buscar(self):
        codigo = self.codigo_var.get().strip()
        if not codigo:
            messagebox.showwarning("Entrada", "Ingrese un codigo a buscar")
            return
        nodo = self.lista.buscar_por_codigo(codigo)
        if nodo:
            self.codigo_resaltado = codigo
            self.log(f"Encontrado: {codigo}")
        else:
            self.codigo_resaltado = None
            self.log(f"No encontrado: {codigo}")
        self.dibujar_lista()

    def eliminar(self):
        codigo = self.codigo_var.get().strip()
        if not codigo:
            messagebox.showwarning("Entrada", "Ingrese un codigo a eliminar")
            return
        nodo = self.lista.buscar_por_codigo(codigo)
        if nodo:
            eliminado = self.lista.eliminar_nodo(nodo)
            self.log(f"Eliminado: {eliminado.codigo}")
            self.codigo_resaltado = None
            self.dibujar_lista()
            self.actualizar_tabla()
        else:
            self.log(f"No se encontro el codigo {codigo}")

    def limpiar(self):
        self.lista.limpiar()
        self.log("Lista limpiada")
        self.codigo_resaltado = None
        self.dibujar_lista()
        self.actualizar_tabla()

    # ------------------------------------------------------------
    # Dibujo del lienzo (con zoom y desplazamiento)
    # ------------------------------------------------------------
    def dibujar_lista(self):
        """Dibuja los nodos en el canvas aplicando zoom y offset."""
        self.canvas.delete("all")
        iniciativas = self.lista.recorrer_adelante()

        if not iniciativas:
            self.canvas.create_text(self.canvas_ancho//2, self.canvas_alto//2,
                                    text="(lista vacia)", fill="gray", font=("Arial", 16))
            return

        escala = self.zoom
        ox = self.offset_x
        oy = self.offset_y

        x = PADDING_X * escala + ox
        y = PADDING_Y * escala + oy
        ancho = ANCHO_NODO * escala
        alto = ALTO_NODO * escala

        posiciones = []  # Guarda coordenadas para dibujar flechas

        for i, ini in enumerate(iniciativas):
            x1 = x + i * (ancho + 20*escala)
            y1 = y
            x2 = x1 + ancho
            y2 = y1 + alto

            # Color según grupo o resaltado
            grupo = ini.grupo
            color_base = COLORES_GRUPO.get(grupo, "#def")
            if self.codigo_resaltado is not None and ini.codigo == self.codigo_resaltado:
                relleno = "#FFD700"  # Dorado para resaltar
            else:
                relleno = color_base

            # Dibujar rectángulo
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=relleno, outline="#333", width=2)
            # Dibujar texto dentro
            tam_fuente = int(9 * escala)
            if tam_fuente < 6:
                tam_fuente = 6
            texto = f"{ini.codigo}\n{ini.nombre}\nMeta: {ini.meta}"
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=texto,
                                    font=("Arial", tam_fuente), justify=tk.CENTER)
            posiciones.append((x1, y1, x2, y2))

        # Dibujar flechas entre nodos (siguiente)
        for i in range(len(posiciones)-1):
            x1 = posiciones[i][2]
            y1 = (posiciones[i][1] + posiciones[i][3]) // 2
            x2 = posiciones[i+1][0]
            y2 = (posiciones[i+1][1] + posiciones[i+1][3]) // 2
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2, fill="#555")

        # Dibujar flecha circular (último -> primero) para mostrar circularidad
        if len(posiciones) > 1:
            ult = posiciones[-1]
            prim = posiciones[0]
            lx = ult[2]
            ly = (ult[1] + ult[3]) // 2
            fx = prim[0]
            fy = (prim[1] + prim[3]) // 2
            midx = (lx + fx) / 2
            self.canvas.create_line(lx, ly, midx, ly - 70*escala, fx, fy,
                                    smooth=True, arrow=tk.LAST, width=2, fill="#777", dash=(4,2))

        self.canvas.config(scrollregion=(0, 0, self.canvas_ancho, self.canvas_alto))

    # ------------------------------------------------------------
    # Eventos de mouse (Zoom y Pan)
    # ------------------------------------------------------------
    def on_scroll(self, event):
        """Desplazamiento vertical con la rueda."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_zoom(self, event):
        """Zoom con Ctrl + rueda del mouse."""
        if event.delta > 0:
            self.zoom *= ZOOM_FACTOR
        else:
            self.zoom /= ZOOM_FACTOR
        # Limitar zoom
        if self.zoom < 0.2:
            self.zoom = 0.2
        if self.zoom > 5.0:
            self.zoom = 5.0
        self.dibujar_lista()

    def iniciar_arrastre(self, event):
        """Guarda la posición inicial para el arrastre."""
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def arrastrar(self, event):
        """Desplaza el canvas al arrastrar con el mouse."""
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.canvas.xview_scroll(-dx, "units")
        self.canvas.yview_scroll(-dy, "units")
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    # ------------------------------------------------------------
    # Actualizar tabla
    # ------------------------------------------------------------
    def actualizar_tabla(self):
        """Limpia y recarga la tabla con los datos actuales."""
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for ini in self.lista.recorrer_adelante():
            self.tabla.insert("", tk.END, values=(
                ini.codigo, ini.nombre, ini.meta, ini.municipio, ini.actor, ini.grupo
            ))

    # ------------------------------------------------------------
    # Alertas
    # ------------------------------------------------------------
    def mostrar_alertas(self):
        """Verifica si hay metas que superen el umbral (1000)."""
        iniciativas = self.lista.recorrer_adelante()
        if not iniciativas:
            messagebox.showinfo("Alertas", "No hay iniciativas registradas.")
            return
        umbral = 1000
        alertas = []
        for ini in iniciativas:
            if ini.meta > umbral:
                alertas.append(f"Iniciativa {ini.codigo} - {ini.nombre}: meta {ini.meta} > {umbral}")
        if alertas:
            messagebox.showwarning("Alertas de meta", "\n".join(alertas))
        else:
            messagebox.showinfo("Alertas", "No se detectaron alertas.")

    # ------------------------------------------------------------
    # DEMOSTRACIÓN PASO A PASO (MEJORADA Y VARIADA)
    # ------------------------------------------------------------
    def iniciar_demo(self):
        """Lanza la demostración en un hilo separado para no bloquear la GUI."""
        t = threading.Thread(target=self.demo_paso_a_paso, daemon=True)
        t.start()

    def demo_paso_a_paso(self):
        """
        Secuencia de demostración que muestra todas las operaciones
        de forma variada, usando los códigos reales del plan de desarrollo.
        """
        self.log("=== INICIO DE DEMOSTRACION PASO A PASO ===")
        self.lista.limpiar()
        self.root.after(0, self.dibujar_lista)
        self.root.after(0, self.actualizar_tabla)
        time.sleep(0.5)

        # 1. Insertar 6 iniciativas al final (usando códigos reales de las tablas)
        datos_ejemplo = [
            Iniciativa("SCT02", "Investigacion capacidades CTel", 1, "Bogota", "Gobernacion", "Ciencias Sociales"),
            Iniciativa("SCT03", "Red centros innovacion", 1, "Soacha", "Universidad", "Ingenieria"),
            Iniciativa("STI02", "Capacitar en IA y blockchain", 30000, "Zipaquira", "Empresa privada", "Tecnologia"),
            Iniciativa("SCT08", "Proyectos agropecuarios CTel", 2000, "Facatativa", "Asociacion campesina", "Agro"),
            Iniciativa("SCT06", "Beneficiar empresas con CTeI", 200, "Bogota", "Gobernacion", "Innovacion social"),
            Iniciativa("SCT13", "Impulsar semilleros investigacion", 15, "Girardot", "Alcaldia", "Ciencias Sociales")
        ]

        self.log("Paso 1: Insertar 6 iniciativas al final (push_back)")
        for ini in datos_ejemplo:
            self.lista.insertar_al_final(ini)
            self.log(f"  Insertado: {ini.codigo} - {ini.nombre}")
            self.root.after(0, self.dibujar_lista)
            self.root.after(0, self.actualizar_tabla)
            time.sleep(0.6)

        # 2. Insertar una prioridad al frente
        prioridad = Iniciativa("PRI01", "Laboratorio jovenes innovadores", 250,
                               "Chia", "Alcaldia", "Innovacion social")
        self.log("Paso 2: Insertar una iniciativa prioritaria al frente (push_front)")
        self.lista.insertar_al_frente(prioridad)
        self.log(f"  Insertado al frente: {prioridad.codigo}")
        self.root.after(0, self.dibujar_lista)
        self.root.after(0, self.actualizar_tabla)
        time.sleep(1.0)

        # 3. Recorridos (adelante y atrás)
        self.log("Paso 3: Mostrar recorridos (adelante y atras)")
        adelante = [ini.codigo for ini in self.lista.recorrer_adelante()]
        atras = [ini.codigo for ini in self.lista.recorrer_atras()]
        self.log(f"  Adelante: {adelante}")
        self.log(f"  Atras: {atras}")
        time.sleep(1.0)

        # 4. Buscar un elemento existente
        codigo_buscar = 'STI02'
        self.log(f"Paso 4: Buscar el codigo '{codigo_buscar}'")
        nodo = self.lista.buscar_por_codigo(codigo_buscar)
        if nodo:
            self.codigo_resaltado = codigo_buscar
            self.log(f"  Encontrado: {codigo_buscar}")
            self.root.after(0, self.dibujar_lista)
            time.sleep(1.2)
        else:
            self.log(f"  No encontrado: {codigo_buscar}")

        # 5. Eliminar ese elemento
        self.log(f"Paso 5: Eliminar el codigo '{codigo_buscar}'")
        if nodo:
            eliminado = self.lista.eliminar_nodo(nodo)
            self.log(f"  Eliminado: {eliminado.codigo}")
            self.codigo_resaltado = None
            self.root.after(0, self.dibujar_lista)
            self.root.after(0, self.actualizar_tabla)
            time.sleep(1.0)

        # 6. Insertar uno nuevo al azar (simulando una nueva iniciativa)
        nuevo = Iniciativa("STI07", "Centro de IA en Cundinamarca", 3,
                           "Cajica", "Universidad", "Tecnologia")
        self.log("Paso 6: Insertar una nueva iniciativa al final (STI07)")
        self.lista.insertar_al_final(nuevo)
        self.log(f"  Insertado: {nuevo.codigo}")
        self.root.after(0, self.dibujar_lista)
        self.root.after(0, self.actualizar_tabla)
        time.sleep(0.8)

        # 7. Eliminar el primero y el ultimo (operaciones de extremo)
        self.log("Paso 7: Eliminar el primer y ultimo nodo")
        if not self.lista.esta_vacia():
            primero = self.lista.eliminar_primero()
            self.log(f"  Eliminado primero: {primero.codigo}")
            self.root.after(0, self.dibujar_lista)
            self.root.after(0, self.actualizar_tabla)
            time.sleep(0.8)
        if not self.lista.esta_vacia():
            ultimo = self.lista.eliminar_ultimo()
            self.log(f"  Eliminado ultimo: {ultimo.codigo}")
            self.root.after(0, self.dibujar_lista)
            self.root.after(0, self.actualizar_tabla)
            time.sleep(0.8)

        # 8. Mostrar estado final
        self.log("Paso 8: Estado final de la lista")
        final = [ini.codigo for ini in self.lista.recorrer_adelante()]
        self.log(f"  Lista final: {final} (tamaño: {len(self.lista)})")
        self.log("=== DEMOSTRACION FINALIZADA ===")


# ------------------------------------------------------------
# Punto de entrada
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()