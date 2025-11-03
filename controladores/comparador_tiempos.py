import time
import random

class ComparadorTiempos:
    def __init__(self, sistema):
        self.sistema = sistema

    # ===============================================================
    # MÉTODO PRINCIPAL DE COMPARACIÓN
    # ===============================================================
    def comparar(self):
        resultados = []
        libros = []

        # -----------------------------------------------------------
        # 🔍 Buscar libros en todas las estructuras conocidas
        # -----------------------------------------------------------
        try:
            # Desde hash
            if hasattr(self.sistema, "hash") and self.sistema.hash:
                for lista in self.sistema.hash.tabla:
                    for libro in lista:
                        libros.append(libro)
                print(f"[DEBUG] Libros obtenidos desde Tabla Hash ({len(libros)} encontrados).")

            # Desde lista doble
            if hasattr(self.sistema, "coleccion") and self.sistema.coleccion:
                nodo = self.sistema.coleccion.primero
                while nodo:
                    libros.append(nodo.libro if hasattr(nodo, "libro") else nodo.valor)
                    nodo = nodo.siguiente
                print(f"[DEBUG] Libros obtenidos desde Lista Doble ({len(libros)} encontrados).")
        except Exception as e:
            print(f"[ERROR] Fallo al recuperar libros: {e}")

        # -----------------------------------------------------------
        #  Validar libros detectados
        # -----------------------------------------------------------
        if not libros:
            print("[WARN] No hay libros cargados para realizar comparaciones.")
            return []

        print(f"[DEBUG] {len(libros)} libros detectados para comparación.")

        # -----------------------------------------------------------
        #  Seleccionar muestra aleatoria
        # -----------------------------------------------------------
        muestra = random.sample(libros, min(10, len(libros)))
        isbns = []

        for item in muestra:
            if hasattr(item, "isbn"):
                isbns.append(item.isbn)
            elif isinstance(item, tuple):
                for sub in item:
                    if hasattr(sub, "isbn"):
                        isbns.append(sub.isbn)
                        break

        # -----------------------------------------------------------
        #  Ejecutar comparaciones en estructuras disponibles
        # -----------------------------------------------------------
        if hasattr(self.sistema, "coleccion") and self.sistema.coleccion:
            resultados.append(self._medir_tiempo("Lista Doble", lambda: self._buscar_lista(isbns)))

        if hasattr(self.sistema, "avl") and self.sistema.avl:
            resultados.append(self._medir_tiempo("Árbol AVL", lambda: self._buscar_avl(isbns)))

        if hasattr(self.sistema, "hash") and self.sistema.hash:
            resultados.append(self._medir_tiempo("Tabla Hash", lambda: self._buscar_hash(isbns)))

        if hasattr(self.sistema, "bmas") and self.sistema.bmas:
            resultados.append(self._medir_tiempo("Árbol B+", lambda: self._buscar_bmas(isbns)))

        # -----------------------------------------------------------
        # Resultado final
        # -----------------------------------------------------------
        if not resultados:
            print("[WARN] No se detectaron estructuras para comparar.")
        else:
            print(" Comparación generada correctamente.")

        return resultados

    # ===============================================================
    # MÉTODOS DE BÚSQUEDA
    # ===============================================================
    def _buscar_lista(self, isbns):
        for isbn in isbns:
            try:
                _ = self.sistema.coleccion.buscar(lambda l: hasattr(l, "isbn") and l.isbn == isbn)
            except Exception:
                pass

    def _buscar_avl(self, isbns):
        for isbn in isbns:
            try:
                _ = self.sistema.avl.buscar(isbn)
            except Exception:
                pass

    def _buscar_hash(self, isbns):
        for isbn in isbns:
            try:
                _ = self.sistema.hash.buscar(isbn)
            except Exception:
                pass

    def _buscar_bmas(self, isbns):
        for isbn in isbns:
            try:
                _ = self.sistema.bmas.buscar(isbn)
            except Exception:
                pass

    # ===============================================================
    # MÉTODOS DE MEDICIÓN Y CLASIFICACIÓN
    # ===============================================================
    def _medir_tiempo(self, nombre, funcion):
        inicio = time.perf_counter()
        funcion()
        fin = time.perf_counter()
        duracion = (fin - inicio) * 1000
        rendimiento = self._clasificar_rendimiento(duracion)
        print(f"[DEBUG] {nombre}: {duracion:.3f} ms ({rendimiento})")
        return {"estructura": nombre, "tiempo": duracion, "rendimiento": rendimiento}

    def _clasificar_rendimiento(self, ms):
        if ms < 1:
            return "Excelente "
        elif ms < 10:
            return "Muy bueno "
        elif ms < 50:
            return "Aceptable "
        else:
            return "Lento "
