import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from controladores.cargador_csv import CargadorCSV

from ui.vista_carga_datos import VistaCargaDatos
from ui.vista_libros import VistaLibros
from ui.vista_bibliotecas import VistaBibliotecas
from ui.vista_red import VistaRed
from ui.vista_despacho import VistaDespacho
from ui.vista_comparaciones import VistaComparaciones


class InterfazPrincipal:
    def __init__(self, sistema):
        self.sistema = sistema
        self.cargador = CargadorCSV(self.sistema)
        # -------------------------------------------------------
        #  Ventana principal con tema moderno
        # -------------------------------------------------------
        self.root = ttk.Window(
            title="📚 Biblioteca Mágica Alrededor del Mundo",
            themename="superhero",
            resizable=(True, True)
        )
        self.root.geometry("1200x720")

        # Pasamos sistema al cargador CSV
        self.cargador = CargadorCSV(sistema)
        self._crear_menubar()
        self._crear_pestanas()
        self._crear_barra_estado()

    # -----------------------------------------------------------
    #  Menú superior
    # -----------------------------------------------------------
    def _crear_menubar(self):
        menubar = ttk.Menu(self.root)

        menu_archivo = ttk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Cargar Libros CSV", command=self.cargar_libros)
        menu_archivo.add_command(label="Cargar Bibliotecas CSV", command=self.cargar_bibliotecas)
        menu_archivo.add_command(label="Cargar Conexiones CSV", command=self.cargar_conexiones)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)

        menu_ver = ttk.Menu(menubar, tearoff=0)
        menu_ver.add_command(label="Refrescar vista", command=self.actualizar_estado)
        menubar.add_cascade(label="Ver", menu=menu_ver)

        menu_ayuda = ttk.Menu(menubar, tearoff=0)
        menu_ayuda.add_command(label="Acerca de...", command=self.mostrar_info)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.root.config(menu=menubar)

    # -----------------------------------------------------------
    #  Pestañas principales (Notebook)
    # -----------------------------------------------------------
    def _crear_pestanas(self):
        estilo = ttk.Style()
        estilo.configure("TNotebook.Tab", padding=[20, 10], font=("Segoe UI", 11, "bold"))

        notebook = ttk.Notebook(self.root, bootstyle="dark")
        notebook.pack(fill=BOTH, expand=True, padx=15, pady=10)

    #  Libros
        self.tab_libros = VistaLibros(notebook, self.sistema)
        notebook.add(self.tab_libros, text="📚 Libros")

    #  Bibliotecas
        self.tab_bibliotecas = VistaBibliotecas(notebook, self.sistema)
        notebook.add(self.tab_bibliotecas, text="🏛️ Bibliotecas")

    #  Red de Bibliotecas
        self.tab_red = VistaRed(notebook, self.sistema)
        notebook.add(self.tab_red, text="🌐 Red de Bibliotecas")


    #  Despacho
        self.tab_despacho = VistaDespacho(notebook, self.sistema)
        notebook.add(self.tab_despacho, text="📦 Despacho")

    #  Comparaciones
        self.tab_comparaciones = VistaComparaciones(notebook, self.sistema)
        notebook.add(self.tab_comparaciones, text="📊 Comparaciones")

    #  Carga de Datos
        self.tab_carga = VistaCargaDatos(notebook, self.cargador, self.actualizar_estado)
        notebook.add(self.tab_carga, text="📂 Cargar Datos")

    # -----------------------------------------------------------
    #  Barra de estado inferior
    # -----------------------------------------------------------
    def _crear_barra_estado(self):
        self.estado = ttk.Label(
            self.root,
            text="Listo.",
            anchor=W,
            bootstyle="secondary-inverse"
        )
        self.estado.pack(side=BOTTOM, fill=X, ipady=4)

    def actualizar_estado(self, mensaje="Listo."):
        self.estado.config(text=f" {mensaje}")

    # -----------------------------------------------------------
    #  Funciones del menú Archivo
    # -----------------------------------------------------------
    def cargar_libros(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de libros",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if ruta:
            try:
                cantidad = self.cargador.cargar_libros(ruta)
                messagebox.showinfo("Carga completada", f" {cantidad} libros cargados correctamente.")
                self.actualizar_estado(f"{cantidad} libros cargados.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al cargar los libros:\n{e}")

    def cargar_bibliotecas(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de bibliotecas",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if ruta:
            try:
                cantidad = self.cargador.cargar_bibliotecas(ruta)
                messagebox.showinfo("Carga completada", f" {cantidad} bibliotecas cargadas correctamente.")
                self.actualizar_estado(f"{cantidad} bibliotecas cargadas.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al cargar bibliotecas:\n{e}")

    def cargar_conexiones(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de conexiones",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if ruta:
            try:
                cantidad = self.cargador.cargar_conexiones(ruta)
                messagebox.showinfo("Carga completada", f" {cantidad} conexiones cargadas correctamente.")
                self.actualizar_estado(f"{cantidad} conexiones cargadas.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al cargar conexiones:\n{e}")

    # ---
    #Ventana de información
    # -----------------------------------------------------------
    def mostrar_info(self):
        messagebox.showinfo(
            "Biblioteca Mágica - Proyecto EDD 2025",
            "Aplicación desarrollada con ttkbootstrap\n"
            "Autor: Brandon Gustavo Guinac Roman \n"
            "Universidad de San Carlos de Guatemala\n"
            "Curso: Estructuras de Datos"
        )

    # -----------------------------------------------------------
    # Iniciar aplicación
    # -----------------------------------------------------------
    def ejecutar(self):
        self.root.mainloop()
