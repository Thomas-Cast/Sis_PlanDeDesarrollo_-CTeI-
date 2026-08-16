# Prototipo funcional de solución con listas enlazadas demostrado

**Autores:** [Tu nombre] y [Nombre del compañero]  
**Curso:** [Nombre de la asignatura] – IV Semestre  
**Fecha:** 15 de agosto de 2026

---

## 1. Resumen

Se presenta un prototipo funcional que utiliza una **lista doblemente enlazada circular con nodo centinela** para gestionar iniciativas de la apuesta CTeI (Ciencia, Tecnología e Innovación) del departamento de Cundinamarca. El sistema cuenta con una interfaz gráfica intuitiva que permite ingresar, buscar, eliminar y visualizar proyectos, así como generar alertas y estadísticas. La interfaz está organizada en tres paneles: formulario de entrada, lienzo interactivo con zoom y desplazamiento, y pestañas para tabla de datos y registro de eventos. El prototipo demuestra el uso práctico de listas enlazadas en un contexto real y se alinea con las metas departamentales.

---

## 2. Descripción del problema

Cundinamarca ha priorizado la CTeI para impulsar la productividad y el desarrollo sostenible. Sin embargo, enfrenta desafíos como la caída del índice de absorción del conocimiento (del 73.58% en 2016 al 45.99% en 2021) y fluctuaciones en la producción investigativa (de 1.41 a 1.12 productos por investigador en 2023). Para hacer seguimiento a las iniciativas de innovación y optimizar los recursos, se requiere una herramienta que permita gestionar proyectos de forma ágil y visual.

---

## 3. Justificación de la estructura de datos

Se eligió una **lista doblemente enlazada circular con centinela** porque:

- Permite inserciones y eliminaciones en O(1) al frente o al final.
- Soporte de recorrido bidireccional (hacia adelante y atrás).
- El centinela simplifica el manejo de casos límite (lista vacía).
- Es fácil de extender con persistencia o búsquedas por clave.

Esta estructura es ideal para un volumen dinámico de proyectos y proporciona una base sólida para el aprendizaje de estructuras de datos.

---

## 4. Componentes del prototipo

- **`linked_list.py`**: Implementación de la lista enlazada con operaciones CRUD y persistencia (JSON, SQLite).
- **`app_gui.py`**: Interfaz gráfica con tres paneles:
  - **Izquierda**: formulario con campos de texto y combos para municipio, actor y grupo.
  - **Centro**: lienzo que dibuja los nodos como rectángulos, con **zoom** (Ctrl+rueda) y **desplazamiento** (arrastrar con el mouse).
  - **Derecha**: pestañas para ver la **tabla de datos** y el **registro de eventos**.
- **`menu_consola.py`**: versión por consola (opcional).

---

## 5. Instrucciones de ejecución y evidencias

**Requisitos:** Python 3.8+ con Tkinter (incluido en la mayoría de las distribuciones).

1. Guardar los archivos `linked_list.py` y `app_gui.py` en la misma carpeta.
2. Ejecutar: `python app_gui.py`
3. La ventana principal se abrirá con los tres paneles.

**Evidencias a capturar (pantallazos):**

1. **Pantalla inicial** con la lista vacía.
2. **Inserción de varias iniciativas** (al menos 4) usando "Insertar al frente" y "Insertar al final". Capturar el lienzo con los nodos y la tabla actualizada.
3. **Búsqueda por código**: resaltar un nodo (color dorado) y mostrar el mensaje en el log.
4. **Eliminación por código**: mostrar el nodo eliminado y el estado posterior.
5. **Demostración paso a paso**: presionar el botón y capturar varias etapas (inserciones, búsqueda, eliminaciones). El log mostrará todos los pasos.
6. **Alertas**: después de insertar una iniciativa con meta > 1000, presionar "Ver alertas" y capturar la ventana emergente.
7. **Uso del zoom y desplazamiento**: capturar el lienzo con diferentes niveles de zoom.

Todas las capturas deben incluirse en el anexo del documento.

---

## 6. Casos de uso soportados

- **Alerta temprana**: detecta automáticamente metas que superan un umbral.
- **Segmentación territorial**: los combos de municipio, actor y grupo facilitan la clasificación.
- **Visualización educativa**: el lienzo con nodos y flechas permite entender el comportamiento de la lista enlazada.

---

## 7. Conclusiones

El prototipo cumple con los objetivos de gestionar iniciativas CTeI mediante una lista enlazada, ofreciendo una interfaz amigable y funcionalidades clave. La incorporación de zoom y desplazamiento mejora la experiencia de visualización, y la tabla de datos permite consultar toda la información de forma estructurada. Este trabajo demuestra la aplicación práctica de estructuras de datos en un contexto real y sienta las bases para un sistema más completo.

---

## 8. Referencias (APA)

Consejo Privado de Competitividad. (2023). *Índice Departamental de Competitividad 2023*. Bogotá: CPC.

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.

Gobernación de Cundinamarca. (2024). *Plan de Desarrollo Departamental 2024-2027*. Secretaría de Planeación.

Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2014). *Data Structures and Algorithms in Python*. Wiley.

---

**Anexos:** (Insertar aquí las capturas de pantalla numeradas y con pies de figura)

**Repositorio:** [Enlace a GitHub o Drive]