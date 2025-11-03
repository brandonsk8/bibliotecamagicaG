import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controladores.simulador_despacho import SimuladorDespacho  # ✅ Importar simulador


class VistaDespacho(ttk.Frame):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema  #  Guardamos referencia al sistema
        self._crear_interfaz()

    # -----------------------------------------------------------
    # INTERFAZ GRÁFICA
    # -----------------------------------------------------------
    def _crear_interfaz(self):
        ttk.Label(
            self,
            text="SISTEMA DE DESPACHO",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=25)

        ttk.Label(
            self,
            text="Simula el proceso de envío y recepción de libros entre bibliotecas.",
            font=("Segoe UI", 11)
        ).pack(pady=5)

        # Botones principales
        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=10)

        ttk.Button(
            frame_botones,
            text="▶️ Iniciar Simulación",
            bootstyle="success-outline",
            command=self.iniciar_simulacion
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            frame_botones,
            text="⏹️ Detener Simulación",
            bootstyle="danger-outline",
            command=self.detener_simulacion
        ).pack(side=LEFT, padx=5)

        # Área de resultados
        self.texto_resultado = ttk.Text(
            self,
            height=18,
            width=100,
            wrap="word",
            state="disabled",
            font=("Consolas", 10)
        )
        self.texto_resultado.pack(padx=20, pady=15)

        ttk.Label(
            self,
            text="(Los resultados se mostrarán aquí durante la simulación)",
            font=("Segoe UI", 10, "italic")
        ).pack(pady=10)

    # -----------------------------------------------------------
    # INICIAR SIMULACIÓN
    # -----------------------------------------------------------
    def iniciar_simulacion(self):
        self.texto_resultado.config(state="normal")
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("end", " Iniciando simulación de despachos...\n\n")
        self.texto_resultado.update()

        simulador = SimuladorDespacho(self.sistema)
        resultados = simulador.simular_envios()  #  Devuelve lista de strings

        for linea in resultados:
            self.texto_resultado.insert("end", linea + "\n")
            self.texto_resultado.update()

        self.texto_resultado.insert("end", "\n Simulación completada.")
        self.texto_resultado.config(state="disabled")

    # -----------------------------------------------------------
    # DETENER SIMULACIÓN
    # -----------------------------------------------------------
    def detener_simulacion(self):
        self.texto_resultado.config(state="normal")
        self.texto_resultado.insert("end", "\n⛔ Simulación detenida por el usuario.\n")
        self.texto_resultado.config(state="disabled")
