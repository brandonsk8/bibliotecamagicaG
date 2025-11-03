from estructuras.arbol_avl import ArbolAVL
from estructuras.tabla_hash import TablaHash
from estructuras.grafo import Grafo
from estructuras.lista_doble import ListaDobleLibros
from estructuras.arbol_bplus import ArbolBMas

class SistemaBiblioteca:
    def __init__(self):
        self.avl = ArbolAVL()
        self.hash = TablaHash(100)
        self.grafo = Grafo()
        self.coleccion = ListaDobleLibros()
        self.bmas = ArbolBMas(3)

    # -------------------------------------------------------
    # Inserción sincronizada
    # -------------------------------------------------------
    def agregar_libro(self, libro):
            """Agrega el libro en todas las estructuras."""
            self.avl.insertar(libro)
            self.hash.insertar(libro.isbn, libro)
            self.coleccion.insertar(libro)
            self.bmas.insertar(libro)  

            print(f"[DEBUG] Libro agregado: {libro.titulo}")

    def eliminar_libro(self, isbn):
        """Elimina el libro de todas las estructuras (AVL, Hash y Lista)."""
        libro = self.hash.buscar(isbn)

        if not libro:
            print(f"[DEBUG] Libro con ISBN {isbn} no encontrado en hash.")
            return False

        #  Eliminar del AVL
        if hasattr(self.avl, "eliminar"):
            self.avl.eliminar(libro.titulo)
            print(f"[DEBUG] Eliminado del AVL: {libro.titulo}")

        #  Eliminar del Hash
        if hasattr(self.hash, "eliminar"):
            self.hash.eliminar(isbn)
            print(f"[DEBUG] Eliminado del Hash: {isbn}")

        # 3️ Eliminar de la lista doble
        eliminado_lista = self.coleccion.eliminar(isbn)
        print(f"[DEBUG] Eliminado de lista doble: {eliminado_lista}")

        return eliminado_lista


    # -------------------------------------------------------
    # Búsqueda avanzada
    # -------------------------------------------------------
    def buscar_libro(self, criterio):
        """Busca libros por ISBN o coincidencia parcial en título."""
        resultados = []

        # Buscar por ISBN exacto
        libro_hash = self.hash.buscar(criterio)
        if libro_hash:
            resultados.append(libro_hash)

        # Buscar por coincidencia de título (AVL)
        criterio_lower = criterio.lower()

        def recorrer_avl(nodo):
            if nodo:
                recorrer_avl(nodo.izq)
                if criterio_lower in nodo.libro.titulo.lower():
                    resultados.append(nodo.libro)
                recorrer_avl(nodo.der)

        recorrer_avl(self.avl.raiz)

        # Buscar también en la lista doble
        actual = self.coleccion.primero
        while actual:
            if criterio_lower in actual.libro.titulo.lower() and actual.libro not in resultados:
                resultados.append(actual.libro)
            actual = actual.siguiente

        return resultados

    # ============================================================
    #  AGREGAR BIBLIOTECA (SINCRONIZADO CON GRAFO)
    # ============================================================
    def agregar_biblioteca(self, biblioteca):
        """
        Agrega una nueva biblioteca al grafo principal del sistema.
        """
        if biblioteca.nombre not in self.grafo.nodos:
            self.grafo.agregar_nodo(biblioteca)
            print(f"[DEBUG] Biblioteca agregada al grafo: {biblioteca.nombre}")
        else:
            print(f"[DEBUG] Biblioteca duplicada ignorada: {biblioteca.nombre}")

    