# -----------------------------------------------------------
# 🌐 Grafo de Bibliotecas (versión final sincronizada)
# -----------------------------------------------------------
from graphviz import Digraph
from PIL import Image, ImageTk
import tempfile
import os
import tkinter as tk
import unicodedata


class NodoGrafo:
    def __init__(self, biblioteca):
        self.biblioteca = biblioteca
        self.conexiones = {}  # destino_id -> peso

    def agregar_conexion(self, destino, peso):
        self.conexiones[destino] = peso


class Grafo:
    def __init__(self):
        self.nodos = {}

    # -----------------------------------------------------------
    # Normalizador único (para TODO el grafo)
    # -----------------------------------------------------------
    def _normalizar(self, texto):
        if not texto:
            return ""
        texto = str(texto).strip().lower()
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )

    # -----------------------------------------------------------
    # Agregar nodo (Biblioteca)
    # -----------------------------------------------------------
    def agregar_nodo(self, biblioteca):
        clave = self._normalizar(biblioteca.id)
        if clave not in self.nodos:
            self.nodos[clave] = NodoGrafo(biblioteca)
            print(f"[DEBUG] Nodo agregado: {biblioteca.nombre} ({biblioteca.id})")

    # -----------------------------------------------------------
    # Agregar conexión entre bibliotecas
    # -----------------------------------------------------------
    def agregar_arista(self, origen, destino, peso):
        o = self._normalizar(origen)
        d = self._normalizar(destino)

        if o in self.nodos and d in self.nodos:
            self.nodos[o].agregar_conexion(d, peso)
            self.nodos[d].agregar_conexion(o, peso)
            print(f"[DEBUG] Conexión agregada correctamente: {origen} ↔ {destino} ({peso})")
        else:
            print(f"[ERROR] Biblioteca {origen} o {destino} no encontrada.")
            print(f"[DEBUG] Claves disponibles: {list(self.nodos.keys())}")

    # -----------------------------------------------------------
    # Mostrar conexiones (para depuración)
    # -----------------------------------------------------------
    def mostrar_conexiones(self):
        for clave, nodo in self.nodos.items():
            nombre = nodo.biblioteca.nombre
            conexiones = ", ".join([f"{dest} ({peso})" for dest, peso in nodo.conexiones.items()])
            print(f"{nombre} [{clave}] ➜ {conexiones if conexiones else 'Sin conexiones'}")

        # -----------------------------------------------------------
    # Visualización con Graphviz (corregida)
    # -----------------------------------------------------------
    def mostrar_grafo(self):
        """Versión simple y limpia del grafo."""
        dot = Digraph(comment="Red de Bibliotecas", format='png')
        dot.attr(rankdir='LR', bgcolor="white", splines="true")

        for clave, nodo in self.nodos.items():
            dot.node(
                clave,
                f"{nodo.biblioteca.nombre}\n({nodo.biblioteca.id})",
                shape="box",
                style="filled",
                fillcolor="#A6C8FF",
                fontcolor="black"
            )

        for origen, nodo in self.nodos.items():
            for destino, peso in nodo.conexiones.items():
                dot.edge(origen, destino, label=f"{peso:.0f}")

        with tempfile.TemporaryDirectory() as tmpdir:
            ruta_img = os.path.join(tmpdir, "grafo")
            dot.render(filename=ruta_img, cleanup=True)
            imagen = Image.open(ruta_img + ".png")

            ventana = tk.Toplevel()
            ventana.title("Red de Bibliotecas")
            ventana.configure(bg="white")

            img_tk = ImageTk.PhotoImage(imagen)
            label = tk.Label(ventana, image=img_tk, bg="white")
            label.image = img_tk
            label.pack(expand=True, fill="both")

            ventana.mainloop()
