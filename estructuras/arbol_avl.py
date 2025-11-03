# -----------------------------------------------------------
#  Árbol AVL (versión base temporal)
#  Permite insertar y almacenar objetos Libro con clave título
# -----------------------------------------------------------

class NodoAVL:
    def __init__(self, libro):
        self.libro = libro
        self.izq = None
        self.der = None
        self.altura = 1


class ArbolAVL:
    def __init__(self):
        self.raiz = None

    # -----------------------------------------------------------
    # Inserción (modo simplificado sin balanceo)
    # -----------------------------------------------------------
    def insertar(self, libro):
        """Inserta un libro basado en el título (sin balanceo por ahora)."""
        self.raiz = self._insertar_rec(self.raiz, libro)

    def _insertar_rec(self, nodo, libro):
        if nodo is None:
            return NodoAVL(libro)
        if libro.titulo < nodo.libro.titulo:
            nodo.izq = self._insertar_rec(nodo.izq, libro)
        else:
            nodo.der = self._insertar_rec(nodo.der, libro)
        return nodo

    # -----------------------------------------------------------
    # Búsqueda simple
    # -----------------------------------------------------------
    def buscar(self, titulo):
        return self._buscar_rec(self.raiz, titulo)

    def _buscar_rec(self, nodo, titulo):
        if nodo is None:
            return None
        if nodo.libro.titulo == titulo:
            return nodo.libro
        elif titulo < nodo.libro.titulo:
            return self._buscar_rec(nodo.izq, titulo)
        else:
            return self._buscar_rec(nodo.der, titulo)
        
    # -----------------------------------------------------------
    # Eliminación (básica sin rebalanceo)
    # -----------------------------------------------------------
    def eliminar(self, titulo):
        """Elimina un libro del árbol por su título."""
        self.raiz = self._eliminar_rec(self.raiz, titulo)

    def _eliminar_rec(self, nodo, titulo):
        if nodo is None:
            return None

        if titulo < nodo.libro.titulo:
            nodo.izq = self._eliminar_rec(nodo.izq, titulo)
        elif titulo > nodo.libro.titulo:
            nodo.der = self._eliminar_rec(nodo.der, titulo)
        else:
            # Nodo encontrado
            if nodo.izq is None:
                return nodo.der
            elif nodo.der is None:
                return nodo.izq

            # Caso con dos hijos → obtener sucesor inorden
            sucesor = self._minimo(nodo.der)
            nodo.libro = sucesor.libro
            nodo.der = self._eliminar_rec(nodo.der, sucesor.libro.titulo)
        return nodo

    def _minimo(self, nodo):
        while nodo.izq:
            nodo = nodo.izq
        return nodo


    # -----------------------------------------------------------
    # Recorrido inorden (para pruebas)
    # -----------------------------------------------------------
    def recorrido_inorden(self):
        resultado = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, resultado):
        if nodo:
            self._inorden_rec(nodo.izq, resultado)
            resultado.append(nodo.libro.titulo)
            self._inorden_rec(nodo.der, resultado)

    def eliminar(self, titulo):
        """Elimina un libro por su título (sin balanceo)."""
        self.raiz = self._eliminar_rec(self.raiz, titulo)

    def _eliminar_rec(self, nodo, titulo):
        if not nodo:
            return None
        if titulo < nodo.libro.titulo:
            nodo.izq = self._eliminar_rec(nodo.izq, titulo)
        elif titulo > nodo.libro.titulo:
            nodo.der = self._eliminar_rec(nodo.der, titulo)
        else:
            # Nodo encontrado
            if not nodo.izq:
                return nodo.der
            if not nodo.der:
                return nodo.izq
            # Reemplazo por el menor de la derecha
            sucesor = self._minimo(nodo.der)
            nodo.libro = sucesor.libro
            nodo.der = self._eliminar_rec(nodo.der, sucesor.libro.titulo)
        return nodo

    def _minimo(self, nodo):
        while nodo.izq:
            nodo = nodo.izq
        return nodo

            