#  Biblioteca Mágica Alrededor del Mundo  
**Proyecto del curso Laboratorio de Estructura de Datos — USAC CUNOC**

---

##  Descripción General

**Biblioteca Mágica Alrededor del Mundo** es un sistema desarrollado en **Python** con **interfaz gráfica** que gestiona una red de bibliotecas interconectadas, cada una con su propio catálogo de libros.  
El sistema utiliza **estructuras de datos avanzadas** implementadas desde cero y renderizadas visualmente mediante **Graphviz**.  

Permite registrar, buscar, ordenar y transferir libros entre bibliotecas, optimizando tiempos y costos de traslado mediante algoritmos de grafos.

---

##  Estructura del Proyecto

BibliotecaMagica/
│
├── interfaz/
│ ├── VentanaPrincipal.py
│ ├── PanelBibliotecas.py
│ └── PanelLibros.py
│
├── controladores/
│ ├── ControladorBiblioteca.py
│ └── ControladorLibro.py
│
├── estructuras/
│ ├── ListaEnlazada.py
│ ├── Pila.py
│ ├── Cola.py
│ ├── ArbolAVL.py
│ ├── ArbolB.py
│ ├── ArbolBMas.py
│ ├── TablaHash.py
│ └── Grafo.py
│
├── reportes/
│ ├── ReporteManager.py
│ └── ReporteTiempos.py
│
├── datos/
│ ├── libros.csv
│ ├── bibliotecas.csv
│ └── conexiones.csv
│
└── main.py



##  Tecnologías Utilizadas

| Tecnología | Uso |
|-------------|-----|
| **Python 3.12** | Lenguaje de programación principal |
| **Tkinter / ttkbootstrap** | Interfaz gráfica (GUI) |
| **Graphviz** | Renderizado de estructuras de datos |
| **Pandas (opcional)** | Carga de archivos CSV |
| **Algoritmos:** Dijkstra, Floyd-Warshall, QuickSort, ShellSort | Procesamiento de datos y rutas |

---

## Instalación y Ejecución

###  Requisitos previos

Asegúrate de tener instalado:
- Python 3.10 o superior  
- Graphviz (agregado al PATH del sistema)

Verifica Graphviz con:
```bash
dot -V
 Instalar dependencias

pip install graphviz
pip install ttkbootstrap
pip install pandas
 Ejecutar el sistema



python main.py
La aplicación abrirá la ventana principal con las opciones de carga, visualización y simulación.

 Archivos de Entrada (CSV)
 libros.csv

Título,Autor,ISBN,Año,Género,Estado
El Principito,Antoine de Saint-Exupéry,9783161484100,1943,Fantasía,Disponible
 bibliotecas.csv

Nombre,Ubicación,TiempoIngreso,TiempoTraspaso,IntervaloDespacho
Biblioteca Central,Guatemala,5,2,10
 conexiones.csv

Origen,Destino,Peso
Biblioteca Central,Biblioteca Norte,8
 Estructuras de Datos Implementadas
Estructura	Uso Principal
Lista Enlazada	Gestión de colecciones de libros
Pila (Stack)	Control de devoluciones y deshacer
Cola (Queue)	Simulación de despacho entre bibliotecas
Árbol AVL	Búsqueda y ordenamiento por título
Árbol B / B+	Clasificación por año y género
Tabla Hash	Indexación rápida por ISBN
Grafo Ponderado	Red de bibliotecas y rutas de transferencia

 Visualización con Graphviz
El sistema genera representaciones gráficas automáticas en formato .png y .dot dentro de la carpeta /reportes.

Ejemplo de generación desde Python:



from graphviz import Digraph

dot = Digraph()
dot.node('A', 'Biblioteca Central')
dot.node('B', 'Biblioteca Norte')
dot.edge('A', 'B', label='8s')
dot.render('grafo_bibliotecas', format='png', view=True)
Las visualizaciones disponibles incluyen:

Árbol AVL (por título)

Árbol B / B+ (por año / género)

Tabla Hash (por ISBN)

Grafo de Bibliotecas (rutas y pesos)

Colas y Pilas (procesos FIFO/LIFO)

 Simulación de Transferencias
El usuario puede seleccionar una biblioteca de origen y destino, un libro y el criterio de transferencia:

Por tiempo mínimo: algoritmo de Dijkstra.

Por costo energético: algoritmo de Floyd-Warshall.

Durante la simulación se muestran:

Estado de cada libro (“en tránsito”, “entregado”).

Rutas intermedias.

Tiempos de despacho.

Visualización gráfica en tiempo real.

 Reportes Generados
Los reportes se almacenan automáticamente en la carpeta /reportes.

Tipo de Reporte	Formato	Ejemplo
Estructuras	.png / .dot	reporte_arbolAVL_1.png
Rutas	.png / .txt	reporte_grafo_2.png
Rendimiento	.txt	reporte_tiempos_3.txt

 Análisis de Complejidad
Estructura	Inserción	Eliminación	Búsqueda
Lista Enlazada	O(1)	O(n)	O(n)
Pila / Cola	O(1)	O(1)	O(1)
Árbol AVL	O(log n)	O(log n)	O(log n)
Árbol B / B+	O(log n)	O(log n)	O(log n)
Tabla Hash	O(1)*	O(1)*	O(1)*
Grafo (Dijkstra)	O(V²)	-	O(V²)

*Promedio con buena dispersión.



markdown

![Ejemplo Grafo](reportes/grafo_bibliotecas.png)
![Árbol AVL](reportes/arbolAVL.png)
![Tabla Hash](reportes/tablaHash.png)
 Funcionalidades Destacadas
 Búsquedas rápidas (AVL, Hash, B+).

 Transferencias automáticas entre bibliotecas.

 Comparación de tiempos de búsqueda y ordenamiento.

 Visualización gráfica automática con Graphviz.

 Simulación de colas de envío y recepción.

 Deshacer operaciones (Pila).

 Autor y Créditos
Desarrollado por: Brandon Gustavo Güinac Román

Carné: 201931217

Universidad: Universidad de San Carlos de Guatemala — CUNOC

Curso: Laboratorio de Estructura de Datos

Fecha: 02 de noviembre de 2025

 Licencia
Este proyecto fue desarrollado con fines académicos y educativos.
Se permite su uso, modificación y estudio con propósitos formativos, siempre citando la fuente original.

