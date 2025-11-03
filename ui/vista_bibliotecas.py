import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class VistaBibliotecas(ttk.Frame):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema
        self._crear_interfaz()

    def _crear_interfaz(self):
        ttk.Label(
            self,
            text="ADMINISTRACIÓN DE BIBLIOTECAS",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=15)

        ttk.Label(
            self,
            text="Gestiona las bibliotecas disponibles en la red.",
            font=("Segoe UI", 11)
        ).pack(pady=5)

        # Tabla
        columnas = ("Nombre", "Ubicación", "T. Ingreso", "T. Traspaso", "Intervalo")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=12)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150, anchor="center")

        self.tabla.pack(padx=20, pady=10, fill=BOTH, expand=True)

        ttk.Button(
            self,
            text="🔄 Actualizar Tabla",
            bootstyle="info-outline",
            command=self.actualizar_tabla
        ).pack(pady=10)

    def actualizar_tabla(self):
        # Limpiar
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        # Agregar bibliotecas del grafo
        for nombre, nodo in self.sistema.grafo.nodos.items():
            biblio = nodo.biblioteca
            self.tabla.insert(
                "",
                "end",
                values=(biblio.nombre, biblio.ubicacion, biblio.tiempo_ingreso, biblio.tiempo_traspaso, biblio.intervalo)
            )

        print(f"[DEBUG] Tabla de bibliotecas actualizada ({len(self.sistema.grafo.nodos)} registros).")
