import tkinter as tk
from tkinter import ttk, messagebox
from controladores.comparador_tiempos import ComparadorTiempos

class VistaComparaciones(ttk.Frame):
    def __init__(self, parent, sistema):
        super().__init__(parent)
        self.sistema = sistema
        self._crear_componentes()

    # ===============================================================
    # CREACIÓN DE COMPONENTES
    # ===============================================================
    def _crear_componentes(self):
        # Título
        lbl_titulo = ttk.Label(
            self,
            text="COMPARACIÓN DE MÉTODOS Y ESTRUCTURAS",
            font=("Segoe UI", 14, "bold"),
            foreground="white",
            background="#243447"
        )
        lbl_titulo.pack(pady=10)

        lbl_desc = ttk.Label(
            self,
            text="Analiza el rendimiento de búsqueda en cada estructura.",
            font=("Segoe UI", 10),
            foreground="white",
            background="#243447"
        )
        lbl_desc.pack()

        # Botón principal
        btn_generar = ttk.Button(
            self,
            text="Generar Comparación",
            command=self.generar_comparacion
        )
        btn_generar.pack(pady=10)

        # Tabla de resultados
        columnas = ("estructura", "tiempo", "rendimiento")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=10)

        self.tabla.heading("estructura", text="Estructura")
        self.tabla.heading("tiempo", text="Tiempo (ms)")
        self.tabla.heading("rendimiento", text="Rendimiento")

        self.tabla.column("estructura", width=180, anchor="center")
        self.tabla.column("tiempo", width=100, anchor="center")
        self.tabla.column("rendimiento", width=150, anchor="center")

        self.tabla.pack(padx=15, pady=10, fill="both", expand=True)

    # ===============================================================
    # GENERAR COMPARACIÓN
    # ===============================================================
    def generar_comparacion(self):
        try:
            comparador = ComparadorTiempos(self.sistema)
            resultados = comparador.comparar()

            # Limpiar tabla anterior
            for fila in self.tabla.get_children():
                self.tabla.delete(fila)

            if not resultados:
                messagebox.showwarning("Aviso", "No hay resultados para mostrar.")
                return

            # Insertar resultados en la tabla
            for r in resultados:
                self.tabla.insert(
                    "", "end",
                    values=(
                        r["estructura"],
                        f"{r['tiempo']:.3f}",
                        r["rendimiento"]
                    )
                )

            messagebox.showinfo("Éxito", "Comparación generada correctamente.")

        except Exception as e:
            print(f"[ERROR] Fallo al generar comparación: {e}")
            messagebox.showerror("Error", f"Ocurrió un error al generar la comparación:\n{e}")
