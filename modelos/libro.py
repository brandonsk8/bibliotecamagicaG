class Libro:
    def __init__(self, titulo, autor, isbn, anio, genero, estado="Disponible",
                 biblioteca_origen=None, biblioteca_destino=None, prioridad=None):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.anio = anio
        self.genero = genero
        self.estado = estado
        self.biblioteca_origen = biblioteca_origen
        self.biblioteca_destino = biblioteca_destino
        self.prioridad = prioridad

    def __str__(self):
        return f"{self.titulo} ({self.isbn})"

    def __repr__(self):
        return f"<Libro {self.titulo} - {self.autor} - {self.estado}>"