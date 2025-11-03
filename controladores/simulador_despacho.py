# -----------------------------------------------------------
#  Simulador de Despacho de Libros
# Usa el grafo de bibliotecas para simular rutas y tiempos
# -----------------------------------------------------------

import heapq

class SimuladorDespacho:
    def __init__(self, sistema):
        self.sistema = sistema  # contiene grafo y colecciones de libros

    # -----------------------------------------------------------
    #  Algoritmo Dijkstra (mínimo costo o tiempo)
    # -----------------------------------------------------------
    def dijkstra(self, inicio, fin, modo="tiempo"):
        grafo = self.sistema.grafo.nodos
        if inicio not in grafo or fin not in grafo:
            print(f"[ERROR] Biblioteca {inicio} o {fin} no encontrada.")
            return float("inf"), []

        distancias = {n: float("inf") for n in grafo}
        distancias[inicio] = 0
        previos = {n: None for n in grafo}
        cola = [(0, inicio)]

        while cola:
            costo_actual, nodo_actual = heapq.heappop(cola)

            if nodo_actual == fin:
                break

            for vecino, peso in grafo[nodo_actual].conexiones.items():
                nuevo_costo = costo_actual + peso
                if nuevo_costo < distancias[vecino]:
                    distancias[vecino] = nuevo_costo
                    previos[vecino] = nodo_actual
                    heapq.heappush(cola, (nuevo_costo, vecino))

        # reconstruir la ruta
        ruta = []
        actual = fin
        while actual is not None:
            ruta.insert(0, actual)
            actual = previos[actual]

        return distancias[fin], ruta

    # -----------------------------------------------------------
    #  Simular envío de libros en tránsito
    # -----------------------------------------------------------
    def simular_envios(self):
        resultados = []
        actual = self.sistema.coleccion.primero
        contador = 0

        while actual:
            libro = actual.libro
            if libro.estado.lower() in ["en tránsito", "prestado"]:
                costo, ruta = self.dijkstra(
                    libro.biblioteca_origen, libro.biblioteca_destino,
                    "costo" if libro.prioridad == "costo" else "tiempo"
                )

                if ruta and costo < float("inf"):
                    resultados.append(f" {libro.titulo} ({libro.estado})")
                    resultados.append(f"   Origen: {libro.biblioteca_origen} → Destino: {libro.biblioteca_destino}")
                    resultados.append(f"   Ruta: {' → '.join(ruta)}")
                    resultados.append(f"   Costo total ({libro.prioridad}): {costo:.2f}\n")
                    contador += 1
                else:
                    resultados.append(f" No hay ruta disponible para {libro.titulo}")

            actual = actual.siguiente

        resultados.append(f" Se simularon {contador} despachos.")
        return resultados
