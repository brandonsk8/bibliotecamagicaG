import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class VistaCargaDatos(ttk.Frame):
    def __init__(self, master, cargador, actualizar_estado_callback):
        super().__init__(master)
        self.cargador = cargador
        self.actualizar_estado = actualizar_estado_callback
        self._crear_interfaz()

    def _crear_interfaz(self):
        ttk.Label(self, text=" CARGA DE ARCHIVOS CSV", font=("Segoe UI", 16, "bold")).pack(pady=20)

        marco_botones = ttk.Frame(self)
        marco_botones.pack(pady=10)

        ttk.Button(marco_botones, text="Cargar Libros", width=25, command=self.cargar_libros).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(marco_botones, text="Cargar Bibliotecas", width=25, command=self.cargar_bibliotecas).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(marco_botones, text="Cargar Conexiones", width=25, command=self.cargar_conexiones).grid(row=0, column=2, padx=10, pady=5)

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=20)

        self.lbl_estado = ttk.Label(self, text="Ningún archivo cargado aún.", font=("Segoe UI", 11, "italic"))
        self.lbl_estado.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("tipo", "cantidad"), show="headings", height=5)
        self.tree.heading("tipo", text="Archivo cargado")
        self.tree.heading("cantidad", text="Elementos leídos")
        self.tree.column("tipo", width=250)
        self.tree.column("cantidad", width=150, anchor="center")
        self.tree.pack(pady=10)

    # -------------------------------------------------------------
    # Funciones de carga
    # -------------------------------------------------------------
    def cargar_libros(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo de libros", filetypes=[("Archivos CSV", "*.csv")])
        if not ruta:
            return
        try:
            cantidad = self.cargador.cargar_libros(ruta)
            self.tree.insert("", "end", values=("Libros", cantidad))
            self.lbl_estado.config(text=f" Se cargaron {cantidad} libros.")
            self.actualizar_estado(f"{cantidad} libros cargados.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar_bibliotecas(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo de bibliotecas", filetypes=[("Archivos CSV", "*.csv")])
        if not ruta:
            return
        try:
            cantidad = self.cargador.cargar_bibliotecas(ruta)
            self.tree.insert("", "end", values=("Bibliotecas", cantidad))
            self.lbl_estado.config(text=f" Se cargaron {cantidad} bibliotecas.")
            self.actualizar_estado(f"{cantidad} bibliotecas cargadas.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar_conexiones(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo de conexiones", filetypes=[("Archivos CSV", "*.csv")])
        if not ruta:
            return
        try:
            cantidad = self.cargador.cargar_conexiones(ruta)
            self.tree.insert("", "end", values=("Conexiones", cantidad))
            self.lbl_estado.config(text=f" Se cargaron {cantidad} conexiones.")
            self.actualizar_estado(f"{cantidad} conexiones cargadas.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
