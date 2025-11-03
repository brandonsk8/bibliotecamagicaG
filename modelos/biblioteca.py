class Biblioteca:
    def __init__(self, nombre, ubicacion, t_ingreso, t_traspaso, intervalo, id_biblioteca=None):
        self.id = id_biblioteca or nombre  # ID único (A-101, B-205, etc.)
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.t_ingreso = t_ingreso
        self.t_traspaso = t_traspaso
        self.intervalo = intervalo

        # Alias opcionales para compatibilidad
        self.tiempo_ingreso = t_ingreso
        self.tiempo_traspaso = t_traspaso


    def __str__(self):
        return f"{self.nombre} ({self.ubicacion})"

    
