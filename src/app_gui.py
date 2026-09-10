"""
app_gui.py
Interfaz grafica funcional para el gestor de iniciativas CTeI.
- Panel izquierdo: formulario de registro + acciones generales.
- Panel central: lienzo circular auto-centrado.
- Panel derecho: tabla de proyectos + detalle del protocolo del seleccionado
  con botones de control manual (avanzar, retroceder, finalizar, eliminar).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import math

from Iniciativa import Iniciativa
from ListaCircular import ListaCircular
from Paso import Paso


ANCHO_NODO = 200
ALTO_NODO = 130

COLORES_PRIORIDAD = {
    "Alta":  "#FFB6B6",
    "Media": "#FFE4B5",
    "Baja":  "#C1E1C1"
}


class App:
    def __init__(self, root):
        self.root = root
        root.title("Gestor CTeI - Protocolo con Lista Circular")
        root.geometry("1500x900")
        root.minsize(1200, 750)

        self.lista = ListaCircular()
        self.finalizados = []
        self.seleccionado = None      # Iniciativa seleccionada en la tabla
        self.zoom = 1.0

        # ============ PANEL IZQUIERDO ============
        left = ttk.Frame(root, width=330)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=6)
        left.pack_propagate(False)

        # --- Formulario ---
        form = ttk.LabelFrame(left, text="Registrar nueva iniciativa", padding=8)
        form.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(form, text="Codigo:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.codigo_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.codigo_var, width=18).grid(row=0, column=1, pady=2)

        ttk.Label(form, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.nombre_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.nombre_var, width=18).grid(row=1, column=1, pady=2)

        ttk.Label(form, text="Meta (numero):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.meta_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.meta_var, width=18).grid(row=2, column=1, pady=2)

        ttk.Label(form, text="Prioridad:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.prioridad_var = tk.StringVar(value="Media")
        ttk.Combobox(form, textvariable=self.prioridad_var, width=16, state="readonly",
                     values=["Alta", "Media", "Baja"]).grid(row=3, column=1, pady=2)

        ttk.Label(form, text="Municipio:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.municipio_var = tk.StringVar(value="Bogota")
        ttk.Combobox(form, textvariable=self.municipio_var, width=16, state="readonly",
                     values=["Bogota", "Soacha", "Zipaquira", "Facatativa", "Girardot",
                             "Chia", "Cajica", "Otro"]).grid(row=4, column=1, pady=2)

        ttk.Label(form, text="Actor:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.actor_var = tk.StringVar(value="Gobernacion")
        ttk.Combobox(form, textvariable=self.actor_var, width=16, state="readonly",
                     values=["Gobernacion", "Universidad", "Empresa privada",
                             "Asociacion campesina", "Alcaldia", "ONG", "Otro"]
                     ).grid(row=5, column=1, pady=2)

        ttk.Label(form, text="Grupo:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.grupo_var = tk.StringVar(value="Ciencias Sociales")
        ttk.Combobox(form, textvariable=self.grupo_var, width=16, state="readonly",
                     values=["Ciencias Sociales", "Ingenieria", "Ciencias Medicas",
                             "Tecnologia", "Agro", "Innovacion social", "Otro"]
                     ).grid(row=6, column=1, pady=2)

        ttk.Button(form, text="Registrar iniciativa",
                   command=self.registrar).grid(row=7, column=0, columnspan=2,
                                                pady=(8, 0), sticky=tk.EW)

        # --- Acciones del ciclo ---
        acc = ttk.LabelFrame(left, text="Acciones del ciclo", padding=8)
        acc.pack(fill=tk.X, pady=6)

        ttk.Button(acc, text=">> Ejecutar paso del turno <<",
                   command=self.ejecutar_turno).pack(fill=tk.X, pady=3)
        ttk.Button(acc, text="Reordenar por prioridad",
                   command=self.reordenar).pack(fill=tk.X, pady=3)
        ttk.Button(acc, text="Ver turno actual",
                   command=self.ver_turno).pack(fill=tk.X, pady=3)

        # --- Herramientas ---
        herr = ttk.LabelFrame(left, text="Herramientas", padding=8)
        herr.pack(fill=tk.X, pady=6)

        ttk.Button(herr, text="Demo paso a paso",
                   command=self.iniciar_demo).pack(fill=tk.X, pady=3)
        ttk.Button(herr, text="Ajustar vista",
                   command=self.ajustar_vista).pack(fill=tk.X, pady=3)
        ttk.Button(herr, text="Limpiar todo",
                   command=self.limpiar).pack(fill=tk.X, pady=3)

        # ============ PANEL CENTRAL ============
        cframe = ttk.LabelFrame(root, text="Ciclo de proyectos activos", padding=4)
        cframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.canvas = tk.Canvas(cframe, bg="#f5faff",
                                highlightthickness=1, highlightbackground="#bbb")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vs = ttk.Scrollbar(cframe, orient=tk.VERTICAL, command=self.canvas.yview)
        vs.pack(side=tk.RIGHT, fill=tk.Y)
        hs = ttk.Scrollbar(cframe, orient=tk.HORIZONTAL, command=self.canvas.xview)
        hs.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)

        self.canvas.bind("<Control-MouseWheel>", self.on_zoom)

        # ============ PANEL DERECHO ============
        right = ttk.Frame(root, width=570)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=6, pady=6)
        right.pack_propagate(False)

        self.notebook = ttk.Notebook(right)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # --- Pestaña "Proyectos" ---
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Proyectos y protocolo")

        # Tabla
        top = ttk.LabelFrame(tab1, text="Lista de iniciativas", padding=3)
        top.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        cols = ("Codigo", "Nombre", "Prior.", "Estado", "Paso actual", "Progreso")
        self.tabla = ttk.Treeview(top, columns=cols, show="headings", height=8)
        for c, w in zip(cols, (80, 150, 60, 90, 120, 70)):
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=w, anchor=tk.W)
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ts = ttk.Scrollbar(top, orient=tk.VERTICAL, command=self.tabla.yview)
        ts.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla.configure(yscrollcommand=ts.set)
        self.tabla.bind("<<TreeviewSelect>>", self.on_seleccionar)

        # Detalle
        det = ttk.LabelFrame(tab1, text="Protocolo del proyecto seleccionado", padding=4)
        det.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        self.lbl_detalle = ttk.Label(det, text="(Seleccione una iniciativa de la lista)",
                                     font=("Arial", 9, "italic"), foreground="#555")
        self.lbl_detalle.pack(anchor=tk.W, padx=3, pady=(2, 4))

        cols2 = ("Paso", "Estado", "Fecha", "Observacion")
        self.detalle = ttk.Treeview(det, columns=cols2, show="headings", height=5)
        for c, w in zip(cols2, (120, 90, 130, 180)):
            self.detalle.heading(c, text=c)
            self.detalle.column(c, width=w, anchor=tk.W)
        self.detalle.pack(fill=tk.BOTH, expand=True)

        # Observacion + botones de acción
        obs_frame = ttk.Frame(det)
        obs_frame.pack(fill=tk.X, padx=3, pady=(6, 2))
        ttk.Label(obs_frame, text="Observacion:").pack(side=tk.LEFT)
        self.obs_var = tk.StringVar()
        ttk.Entry(obs_frame, textvariable=self.obs_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

        btn_frame = ttk.Frame(det)
        btn_frame.pack(fill=tk.X, padx=3, pady=4)
        self.btn_avanzar = ttk.Button(btn_frame, text="Avanzar paso",
                                      command=self.avanzar_seleccionado, state=tk.DISABLED)
        self.btn_avanzar.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        self.btn_retroceder = ttk.Button(btn_frame, text="Retroceder paso",
                                         command=self.retroceder_seleccionado, state=tk.DISABLED)
        self.btn_retroceder.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        self.btn_finalizar = ttk.Button(btn_frame, text="Finalizar",
                                        command=self.finalizar_seleccionado, state=tk.DISABLED)
        self.btn_finalizar.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        self.btn_eliminar = ttk.Button(btn_frame, text="Eliminar",
                                       command=self.eliminar_seleccionado, state=tk.DISABLED)
        self.btn_eliminar.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        # --- Pestaña "Registro" ---
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="Registro")
        self.log_text = tk.Text(tab2, height=20, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ls = ttk.Scrollbar(tab2, orient=tk.VERTICAL, command=self.log_text.yview)
        ls.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=ls.set)

        # Dibujar el estado inicial
        self.root.after(150, self.dibujar)

    # ================= Utilidades =================

    def log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{ts}] {msg}\n")
        self.log_text.see(tk.END)

    def obtener_iniciativa(self):
        codigo = self.codigo_var.get().strip()
        nombre = self.nombre_var.get().strip() or "(sin nombre)"
        try:
            meta = int(self.meta_var.get().strip()) if self.meta_var.get().strip() else 0
        except ValueError:
            meta = 0
        return Iniciativa(codigo, nombre, meta,
                          self.municipio_var.get().strip(),
                          self.actor_var.get().strip(),
                          self.grupo_var.get().strip(),
                          self.prioridad_var.get().strip())

    # ================= Operaciones generales =================

    def registrar(self):
        ini = self.obtener_iniciativa()
        if not ini.codigo:
            messagebox.showwarning("Aviso", "El codigo es obligatorio")
            return
        if self.lista.buscar_por_codigo(ini.codigo):
            messagebox.showwarning("Aviso", f"Ya existe una iniciativa con codigo '{ini.codigo}'")
            return
        self.lista.insertar_ordenado(ini)
        self.log(f"REGISTRADA: {ini.codigo} - {ini.nombre} [{ini.prioridad}]")
        self.dibujar()
        self.actualizar_tabla()
        # Limpiar campos
        self.codigo_var.set("")
        self.nombre_var.set("")
        self.meta_var.set("")

    def reordenar(self):
        self.lista.reordenar_por_prioridad()
        self.log("Lista reordenada por prioridad (Alta > Media > Baja)")
        self.dibujar()
        self.actualizar_tabla()

    def ejecutar_turno(self):
        """Ejecuta el siguiente paso del proyecto en turno (round-robin)."""
        if self.lista.esta_vacia():
            messagebox.showinfo("Aviso", "No hay proyectos activos")
            return
        ini, msg, fin = self.lista.avanzar_turno_actual("Avance automatico del turno")
        self.log(msg)
        if fin:
            self.finalizados.append(ini)
            self.log(f"  -> {ini.codigo} pasa al historial de finalizados")
        self.dibujar()
        self.actualizar_tabla()

    def ver_turno(self):
        actual = self.lista.obtener_actual()
        if actual is None:
            messagebox.showinfo("Turno", "No hay proyectos en el ciclo")
            return
        paso = actual.paso_actual()
        messagebox.showinfo("Turno actual",
                            f"Codigo:    {actual.codigo}\n"
                            f"Nombre:    {actual.nombre}\n"
                            f"Prioridad: {actual.prioridad}\n"
                            f"Paso:      {paso.nombre if paso else '-'}\n"
                            f"Progreso:  {actual.progreso()}")

    def limpiar(self):
        if not messagebox.askyesno("Confirmar", "Se borraran todos los proyectos. Continuar?"):
            return
        self.lista.limpiar()
        self.finalizados = []
        self.seleccionado = None
        self.log("Sistema limpiado por completo")
        self.detalle.delete(*self.detalle.get_children())
        self.lbl_detalle.config(text="(Seleccione una iniciativa de la lista)")
        self.dibujar()
        self.actualizar_tabla()

    def ajustar_vista(self):
        """Re-centra el canvas."""
        self.dibujar()

    # ================= Control del seleccionado =================

    def on_seleccionar(self, event):
        sel = self.tabla.selection()
        if not sel:
            return
        iid = sel[0]
        codigo = iid.split("_", 1)[1]

        ini = None
        for x in self.lista.recorrer():
            if x.codigo == codigo:
                ini = x
                break
        if ini is None:
            for x in self.finalizados:
                if x.codigo == codigo:
                    ini = x
                    break

        self.seleccionado = ini
        if ini is None:
            self.lbl_detalle.config(text="(Seleccione una iniciativa de la lista)")
            self.detalle.delete(*self.detalle.get_children())
            self._set_estado_botones(False, False, False, False)
            return

        # Actualizar el detalle
        estado = "FINALIZADO" if ini.finalizado else "EN PROCESO"
        self.lbl_detalle.config(
            text=f"{ini.codigo} - {ini.nombre} | Prioridad: {ini.prioridad} | "
                 f"Estado: {estado} | Progreso: {ini.progreso()}"
        )
        self.detalle.delete(*self.detalle.get_children())
        for p in ini.pasos:
            self.detalle.insert("", tk.END, values=(
                p.nombre, p.estado, p.fecha or "-", p.observacion or "-"
            ))

        # Habilitar botones según estado
        activo = not ini.finalizado
        self._set_estado_botones(
            avanzar=activo,
            retroceder=(ini.indice_paso > 0 or ini.finalizado),
            finalizar=activo,
            eliminar=True
        )
        self.dibujar()

    def _set_estado_botones(self, avanzar, retroceder, finalizar, eliminar):
        self.btn_avanzar.config(state=tk.NORMAL if avanzar else tk.DISABLED)
        self.btn_retroceder.config(state=tk.NORMAL if retroceder else tk.DISABLED)
        self.btn_finalizar.config(state=tk.NORMAL if finalizar else tk.DISABLED)
        self.btn_eliminar.config(state=tk.NORMAL if eliminar else tk.DISABLED)

    def avanzar_seleccionado(self):
        if self.seleccionado is None:
            return
        obs = self.obs_var.get().strip() or "Avance manual"
        ini = self.seleccionado
        paso = ini.paso_actual()
        if paso is None:
            return
        nombre_paso = paso.nombre
        fin = ini.avanzar_paso(obs)
        self.log(f"AVANCE MANUAL: {ini.codigo} - '{nombre_paso}' completado" +
                 (f" -> PROYECTO FINALIZADO" if fin else f" -> siguiente: {ini.paso_actual().nombre}"))
        if fin and ini not in self.finalizados:
            self.finalizados.append(ini)
            self.lista.eliminar_por_codigo(ini.codigo)
        self.obs_var.set("")
        self.dibujar()
        self.actualizar_tabla()
        self._refrescar_detalle()

    def retroceder_seleccionado(self):
        if self.seleccionado is None:
            return
        ini = self.seleccionado
        ok = ini.retroceder_paso()
        if ok:
            self.log(f"RETROCESO: {ini.codigo} vuelve al paso '{ini.paso_actual().nombre}'")
            # Si estaba finalizado y ahora no, lo devolvemos a la lista activa
            if not ini.finalizado and ini in self.finalizados:
                self.finalizados.remove(ini)
                self.lista.insertar_ordenado(ini)
        self.obs_var.set("")
        self.dibujar()
        self.actualizar_tabla()
        self._refrescar_detalle()

    def finalizar_seleccionado(self):
        if self.seleccionado is None:
            return
        ini = self.seleccionado
        if not messagebox.askyesno("Confirmar",
                                   f"Finalizar '{ini.codigo}' saltando los pasos pendientes?"):
            return
        ini.forzar_finalizar("Finalizado manualmente")
        if ini not in self.finalizados:
            self.finalizados.append(ini)
            self.lista.eliminar_por_codigo(ini.codigo)
        self.log(f"FINALIZADO MANUAL: {ini.codigo}")
        self.dibujar()
        self.actualizar_tabla()
        self._refrescar_detalle()

    def eliminar_seleccionado(self):
        if self.seleccionado is None:
            return
        ini = self.seleccionado
        if not messagebox.askyesno("Confirmar", f"Eliminar '{ini.codigo}' del sistema?"):
            return
        self.lista.eliminar_por_codigo(ini.codigo)
        if ini in self.finalizados:
            self.finalizados.remove(ini)
        self.log(f"ELIMINADO: {ini.codigo} - {ini.nombre}")
        self.seleccionado = None
        self.detalle.delete(*self.detalle.get_children())
        self.lbl_detalle.config(text="(Seleccione una iniciativa de la lista)")
        self._set_estado_botones(False, False, False, False)
        self.dibujar()
        self.actualizar_tabla()

    def _refrescar_detalle(self):
        """Vuelve a cargar el detalle del seleccionado sin perder la selección."""
        if self.seleccionado is None:
            return
        codigo = self.seleccionado.codigo
        # Reconstruir el iid
        for row in self.tabla.get_children():
            if row.endswith("_" + codigo):
                self.tabla.selection_set(row)
                break
        # Simular la selección
        self.on_seleccionar(None)

    # ================= Tabla =================

    def actualizar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for ini in self.lista.recorrer():
            paso = ini.paso_actual()
            self.tabla.insert("", tk.END, iid=f"A_{ini.codigo}",
                              values=(ini.codigo, ini.nombre, ini.prioridad,
                                      "En proceso",
                                      paso.nombre if paso else "-",
                                      ini.progreso()))

        for ini in self.finalizados:
            self.tabla.insert("", tk.END, iid=f"F_{ini.codigo}",
                              values=(ini.codigo, ini.nombre, ini.prioridad,
                                      "Finalizado", "Entrega / Final", ini.progreso()))

    # ================= Dibujo =================

    def dibujar(self):
        self.canvas.delete("all")
        iniciativas = self.lista.recorrer()

        self.canvas.update_idletasks()
        vw = max(self.canvas.winfo_width(), 500)
        vh = max(self.canvas.winfo_height(), 450)

        if not iniciativas:
            self.canvas.create_text(vw / 2, vh / 2,
                                    text="Sin proyectos activos\n\nRegistre una iniciativa para comenzar",
                                    fill="#888", font=("Arial", 15), justify=tk.CENTER)
            self.canvas.config(scrollregion=(0, 0, vw, vh))
            return

        n = len(iniciativas)

        # Radio dinámico según cantidad de nodos
        base = 170
        if n > 6:
            base += (n - 6) * 22
        radio = base * self.zoom

        ancho_nodo = ANCHO_NODO * self.zoom
        alto_nodo = ALTO_NODO * self.zoom

        margen = 90
        ancho = 2 * (radio + ancho_nodo / 2) + 2 * margen
        alto = 2 * (radio + alto_nodo / 2) + 2 * margen

        ancho = max(ancho, vw)
        alto = max(alto, vh)

        cx = ancho / 2
        cy = alto / 2

        self.canvas.config(scrollregion=(0, 0, ancho, alto))

        actual = self.lista.obtener_actual()
        seleccionado = self.seleccionado

        posiciones = []
        for i, ini in enumerate(iniciativas):
            angulo = 2 * math.pi * i / n - math.pi / 2
            x = cx + radio * math.cos(angulo)
            y = cy + radio * math.sin(angulo)
            posiciones.append((x, y, ini))

        # Flechas primero
        for i in range(n):
            x1, y1, _ = posiciones[i]
            j = (i + 1) % n
            x2, y2, _ = posiciones[j]
            dx, dy = x2 - x1, y2 - y1
            dist = math.hypot(dx, dy)
            if dist > 0:
                ux, uy = dx / dist, dy / dist
                sx = x1 + ux * (ancho_nodo * 0.5)
                sy = y1 + uy * (alto_nodo * 0.5)
                ex = x2 - ux * (ancho_nodo * 0.5)
                ey = y2 - uy * (alto_nodo * 0.5)
                self.canvas.create_line(sx, sy, ex, ey,
                                        arrow=tk.LAST, width=2, fill="#666")

        # Nodos
        for (x, y, ini) in posiciones:
            x1, y1 = x - ancho_nodo / 2, y - alto_nodo / 2
            x2, y2 = x + ancho_nodo / 2, y + alto_nodo / 2

            color = COLORES_PRIORIDAD.get(ini.prioridad, "#EEE")
            es_actual = (ini is actual)
            es_sel = (ini is seleccionado)

            outline = "#333"
            grosor = 2
            if es_actual:
                outline = "#FF8C00"
                grosor = 5
            if es_sel:
                outline = "#1E90FF"
                grosor = 5

            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         fill=color, outline=outline, width=grosor)

            paso = ini.paso_actual()
            fsize = max(8, int(9 * self.zoom))
            texto = (f"{ini.codigo}\n"
                     f"{ini.nombre[:20]}\n"
                     f"[{ini.prioridad}]\n"
                     f"{paso.nombre if paso else 'FINAL'}")
            self.canvas.create_text(x, y, text=texto,
                                    font=("Arial", fsize), justify=tk.CENTER)

            if es_actual:
                self.canvas.create_text(x, y1 - 14, text="TURNO ACTUAL",
                                        fill="#FF4500",
                                        font=("Arial", max(8, int(10 * self.zoom)), "bold"))
            elif es_sel:
                self.canvas.create_text(x, y1 - 14, text="SELECCIONADO",
                                        fill="#1E90FF",
                                        font=("Arial", max(8, int(10 * self.zoom)), "bold"))

        # Centrar vista en el contenido
        if ancho > vw:
            self.canvas.xview_moveto((ancho - vw) / (2 * ancho))
        else:
            self.canvas.xview_moveto(0)
        if alto > vh:
            self.canvas.yview_moveto((alto - vh) / (2 * alto))
        else:
            self.canvas.yview_moveto(0)

    def on_zoom(self, event):
        if event.delta > 0:
            self.zoom *= 1.1
        else:
            self.zoom /= 1.1
        if self.zoom < 0.4:
            self.zoom = 0.4
        if self.zoom > 2.5:
            self.zoom = 2.5
        self.dibujar()

    # ================= Demo =================

    def iniciar_demo(self):
        t = threading.Thread(target=self.demo, daemon=True)
        t.start()

    def demo(self):
        self.log("=== DEMO: LLEGADA Y TRAMITE DE INICIATIVAS ===")
        self.lista.limpiar()
        self.finalizados = []
        self.seleccionado = None
        self.root.after(0, self.dibujar)
        self.root.after(0, self.actualizar_tabla)
        time.sleep(0.5)

        llegadas = [
            Iniciativa("SCT02", "Investigacion capacidades CTel", 1, "Bogota", "Gobernacion", "Ciencias Sociales", "Media"),
            Iniciativa("STI02", "Capacitar en IA y blockchain", 30000, "Zipaquira", "Empresa privada", "Tecnologia", "Alta"),
            Iniciativa("SCT08", "Proyectos agropecuarios CTel", 2000, "Facatativa", "Asociacion campesina", "Agro", "Baja"),
            Iniciativa("SCT03", "Red centros innovacion", 1, "Soacha", "Universidad", "Ingenieria", "Alta"),
            Iniciativa("SCT06", "Beneficiar empresas con CTeI", 200, "Bogota", "Gobernacion", "Innovacion social", "Media"),
        ]

        self.log("Paso 1: Llegan 5 iniciativas (se ordenan por prioridad)")
        for ini in llegadas:
            self.lista.insertar_ordenado(ini)
            self.log(f"  + {ini.codigo} [{ini.prioridad}] {ini.nombre}")
            self.root.after(0, self.dibujar)
            self.root.after(0, self.actualizar_tabla)
            time.sleep(0.5)

        self.log("Paso 2: Se ejecuta el protocolo automaticamente (round-robin)")
        for _ in range(15):
            if self.lista.esta_vacia():
                break
            ini, msg, fin = self.lista.avanzar_turno_actual("Demo automatica")
            self.log(f"  {msg}")
            if fin and ini not in self.finalizados:
                self.finalizados.append(ini)
            self.root.after(0, self.dibujar)
            self.root.after(0, self.actualizar_tabla)
            time.sleep(0.7)

        self.log("Paso 3: Estado final")
        activos = [i.codigo for i in self.lista.recorrer()]
        fin = [i.codigo for i in self.finalizados]
        self.log(f"  Activos: {activos}")
        self.log(f"  Finalizados: {fin}")
        self.log("=== FIN DEMO ===")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()