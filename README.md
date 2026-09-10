# Solución cíclica con listas circulares - CTeI Cundinamarca

Prototipo funcional desarrollado en Python que implementa una **lista circular simple**
para gestionar el ciclo de atención de iniciativas de Ciencia, Tecnología e Innovación (CTeI)
del departamento de Cundinamarca. Cada proyecto avanza por un protocolo de etapas
(Concepción, Formulación, Evaluación, Contratación, Ejecución, Cierre, Completado)
de forma rotativa y equitativa.

---

## Descripción del problema

El departamento de Cundinamarca gestiona múltiples iniciativas de innovación que requieren
evaluación, contratación, ejecución y cierre. Los recursos son limitados y no se pueden
atender todas al mismo tiempo, por lo que se necesita un sistema de turnos rotativos que
garantice la atención equitativa y el avance ordenado de cada proyecto.

La **lista circular** modela este proceso: en cada ronda, el sistema toma el proyecto que
está en la cabeza, le aplica la siguiente etapa del protocolo y luego avanza la cabeza
al siguiente nodo. El ciclo es continuo e indefinido.

---

## Estructura del proyecto
src/
├── Etapa.py # Enumeración de las etapas del protocolo
├── Iniciativa.py # Clase que representa un proyecto de innovación
├── Nodo.py # Nodo de la lista circular
├── ListaCircular.py # Implementación de la lista circular simple
├── app_gui.py # Interfaz gráfica (Tkinter)
└── main.py # Punto de entrada


---

## Requisitos

- Python 3.8 o superior
- Tkinter (incluido en la mayoría de distribuciones de Python)

No se requieren dependencias externas.

---

## Cómo ejecutar

1. Clonar el repositorio:

2. Entrar a la carpeta `src`:

3. Ejecutar el programa:

4. Se abrirá una ventana con tres paneles:
- Izquierda: formulario para ingresar datos de las iniciativas.
- Centro: lienzo que dibuja los nodos en formación circular, resaltando
  el turno actual.
- Derecha: pestañas con la tabla de datos y el registro de eventos.

---

## Funcionalidades principales

- Insertar al frente / al final: agrega nuevas iniciativas al ciclo.
- Buscar por código: resalta el nodo encontrado.
- Eliminar por código: retira una iniciativa del ciclo.
- Avanzar turno: aplica la siguiente etapa del protocolo al proyecto en turno
y mueve la cabeza al siguiente nodo.
- Ver turno actual: muestra los datos del proyecto que está siendo atendido.
- Demo paso a paso: ejecuta una demostración automatizada que muestra inserciones,
avances de etapa y eliminaciones de proyectos completados.

---

## Capturas de pantalla

Las evidencias de ejecución se encuentran en la carpeta `capturas/`:

1. Pantalla inicial
2. Inserción de iniciativas
3. Búsqueda por código
4. Avance de turno
5. Demostración paso a paso
6. Estado final del ciclo

---

## Conceptos aplicados

- **Lista circular simple**: estructura de datos dinámica sin fin, donde el último
nodo apunta al primero.
- **Programación Orientada a Objetos**: clases separadas para Etapa, Iniciativa,
Nodo, ListaCircular y App.
- **Protocolo de etapas**: ciclo de vida de un proyecto modelado con una enumeración.
- **Interfaz gráfica**: Tkinter con canvas, tablas y registros.

---

## Autores

- [Tu nombre completo] - [Código estudiantil]
- [Nombre del compañero] - [Código estudiantil]

**Curso**: Estructuras de Datos - IV Semestre
**Universidad**: [Nombre de la universidad]
**Fecha**: [Fecha de entrega]

---

## Referencias (APA 7ª ed.)

Consejo Privado de Competitividad. (2023). *Índice Departamental de Competitividad 2023*.
Bogotá: CPC.

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to
Algorithms* (3rd ed.). MIT Press.

Gobernación de Cundinamarca. (2024). *Plan de Desarrollo Departamental 2024-2027:
Cundinamarca Región que Progresa*. Secretaría de Planeación.

Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2014). *Data Structures and
Algorithms in Python*. Wiley.