# -----------------------------------------------------------
#  ÁRBOL B+ PARA AGRUPAR LIBROS POR GÉNERO
# -----------------------------------------------------------

class NodoBMas:
    def __init__(self, orden=3):
        self.orden = orden
        self.claves = []
        self.hijos = []
        self.libros = []  # Solo en hojas
        self.hoja = True

    def esta_lleno(self):
        return len(self.claves) >= self.orden


class ArbolBMas:
    def __init__(self, orden=3):
        self.raiz = NodoBMas(orden)
        self.orden = orden

    # -----------------------------------------------------------
    # Insertar un libro en el árbol (por género)
    # -----------------------------------------------------------
    def insertar(self, libro):
        nodo = self.raiz

        # Si el nodo raíz está lleno, dividir
        if nodo.esta_lleno():
            nueva_raiz = NodoBMas(self.orden)
            nueva_raiz.hoja = False
            nueva_raiz.hijos.append(self.raiz)
            self._dividir_hijo(nueva_raiz, 0)
            self.raiz = nueva_raiz

        self._insertar_no_lleno(self.raiz, libro)

    def _insertar_no_lleno(self, nodo, libro):
        clave = libro.genero

        if nodo.hoja:
            if clave not in nodo.claves:
                nodo.claves.append(clave)
                nodo.libros.append([libro])
                nodo.claves.sort()
                nodo.libros = [l for _, l in sorted(zip(nodo.claves, nodo.libros))]
            else:
                idx = nodo.claves.index(clave)
                nodo.libros[idx].append(libro)
        else:
            i = len(nodo.claves) - 1
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1
            if nodo.hijos[i].esta_lleno():
                self._dividir_hijo(nodo, i)
                if clave > nodo.claves[i]:
                    i += 1
            self._insertar_no_lleno(nodo.hijos[i], libro)

    def _dividir_hijo(self, padre, i):
        nodo = padre.hijos[i]
        nuevo = NodoBMas(self.orden)
        nuevo.hoja = nodo.hoja
        mid = self.orden // 2

        # Claves y libros de la derecha
        nuevo.claves = nodo.claves[mid + 1:]
        nodo.claves = nodo.claves[:mid]

        if nodo.hoja:
            nuevo.libros = nodo.libros[mid + 1:]
            nodo.libros = nodo.libros[:mid + 1]
            nuevo.hijos = []
        else:
            nuevo.hijos = nodo.hijos[mid + 1:]
            nodo.hijos = nodo.hijos[:mid + 1]

        padre.claves.insert(i, nodo.claves[-1])
        padre.hijos.insert(i + 1, nuevo)
        padre.hoja = False

    # -----------------------------------------------------------
    # Buscar libros por género
    # -----------------------------------------------------------
    def buscar(self, genero):
        nodo = self.raiz
        while not nodo.hoja:
            i = 0
            while i < len(nodo.claves) and genero > nodo.claves[i]:
                i += 1
            nodo = nodo.hijos[i]
        for i, clave in enumerate(nodo.claves):
            if clave == genero:
                return nodo.libros[i]
        return []

    # -----------------------------------------------------------
    # Recorrido completo (para mostrar todo el árbol)
    # -----------------------------------------------------------
    def recorrer(self):
        resultado = []
        self._recorrer_nodo(self.raiz, resultado)
        return resultado

    def _recorrer_nodo(self, nodo, resultado):
        if nodo.hoja:
            for genero, libros in zip(nodo.claves, nodo.libros):
                resultado.append((genero, [l.titulo for l in libros]))
        else:
            for i in range(len(nodo.claves)):
                self._recorrer_nodo(nodo.hijos[i], resultado)
            self._recorrer_nodo(nodo.hijos[-1], resultado)
