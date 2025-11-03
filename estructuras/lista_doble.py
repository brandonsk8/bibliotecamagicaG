# -----------------------------------------------------------
# LISTA DOBLEMENTE ENLAZADA DE LIBROS
# -----------------------------------------------------------
# Implementación de una lista doble para almacenar libros.
#   - Inserción secuencial de libros (colección)
#   - Búsqueda y eliminación por ISBN
#   - Validación de conflictos por ISBN
# -----------------------------------------------------------

from modelos.libro import Libro

class NodoLibro:
    """Nodo que representa un libro dentro de la lista doble."""
    def __init__(self, libro: Libro):
        self.libro = libro
        self.siguiente = None
        self.anterior = None


class ListaDobleLibros:
    """Lista doblemente enlazada para gestionar la colección de libros."""
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamaño = 0

    # -----------------------------------------------------------
    # Insertar libro al final
    # -----------------------------------------------------------
    def insertar(self, libro: Libro):
        nuevo = NodoLibro(libro)
        if not self.primero:
            self.primero = self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo
        self.tamaño += 1

    # -----------------------------------------------------------
    #  Buscar libro por ISBN
    # -----------------------------------------------------------
    def buscar_por_isbn(self, isbn: str):
        actual = self.primero
        while actual:
            if actual.libro.isbn == isbn:
                return actual.libro
            actual = actual.siguiente
        return None

    # -----------------------------------------------------------
    # ELIMINAR LIBRO
    # -----------------------------------------------------------
    def eliminar_libro(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar", "Seleccione un libro de la tabla.")
            return

        item = self.tabla.item(seleccion)
        isbn = item["values"][2]
        titulo = item["values"][0]

        if messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar '{titulo}' (ISBN: {isbn})?"):
            eliminado = self.sistema.eliminar_libro(isbn)

            if eliminado:
                # Eliminar directamente de la tabla visual
                self.tabla.delete(seleccion)
                messagebox.showinfo("Eliminado", f"Libro '{titulo}' eliminado correctamente.")
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el libro '{titulo}'.")

            # Actualizar tabla (para reflejar cambios en lista doble)
            self.actualizar_tabla()




       # -----------------------------------------------------------
    #  Validar conflictos de ISBN
    # -----------------------------------------------------------
    def existe_conflicto_isbn(self, libro):
        """
        Verifica si el ISBN ya existe en la colección:
        - Si pertenece al mismo libro (mismo título y autor), se permite.
        - Si pertenece a un libro distinto, se considera conflicto.
        """
        actual = self.primero
        while actual:
            if actual.libro.isbn == libro.isbn:
                mismo_titulo = actual.libro.titulo.lower() == libro.titulo.lower()
                mismo_autor = actual.libro.autor.lower() == libro.autor.lower()
                if not (mismo_titulo and mismo_autor):
                    return True  # Conflicto detectado
            actual = actual.siguiente
        return False  #  No hay conflicto

    # -----------------------------------------------------------
    #  Listar libros como lista de objetos Libro
    # -----------------------------------------------------------
    def listar(self):
        resultado = []
        actual = self.primero
        while actual:
            resultado.append(actual.libro)
            actual = actual.siguiente
        return resultado

    # -----------------------------------------------------------
    # Mostrar la lista en consola (debug)
    # -----------------------------------------------------------
    def imprimir(self):
        print("\n Colección actual:")
        actual = self.primero
        while actual:
            print(f" - {actual.libro.titulo} | ISBN: {actual.libro.isbn}")
            actual = actual.siguiente
        print(f"Total de libros: {self.tamaño}\n")

    
        # -----------------------------------------------------------
    #  ELIMINAR LIBRO POR ISBN
    # -----------------------------------------------------------
    def eliminar(self, isbn: str):
        """Elimina un libro de la lista doblemente enlazada por ISBN."""
        actual = self.primero
        while actual:
            if str(actual.libro.isbn).strip() == str(isbn).strip():
                # Caso único
                if actual == self.primero == self.ultimo:
                    self.primero = self.ultimo = None
                # Caso primero
                elif actual == self.primero:
                    self.primero = actual.siguiente
                    if self.primero:
                        self.primero.anterior = None
                # Caso último
                elif actual == self.ultimo:
                    self.ultimo = actual.anterior
                    if self.ultimo:
                        self.ultimo.siguiente = None
                # Caso intermedio
                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior

                print(f"[DEBUG] Eliminado de lista doble: {isbn}")
                return True
            actual = actual.siguiente

        print(f"[DEBUG] Libro con ISBN {isbn} no encontrado en lista doble.")
        return False

