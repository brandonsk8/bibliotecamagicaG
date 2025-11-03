import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class VistaRed(ttk.Frame):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema
        self._crear_interfaz()

    def _crear_interfaz(self):
        ttk.Label(
            self,
            text="🌐 RED DE BIBLIOTECAS",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=15)

        ttk.Label(
            self,
            text="Visualiza y analiza las conexiones entre bibliotecas.",
            font=("Segoe UI", 11)
        ).pack(pady=5)

        ttk.Button(
            self,
            text="📈 Mostrar Grafo",
            bootstyle="info-outline",
            command=lambda: self.sistema.grafo.mostrar_grafo()
        ).pack(pady=20)
