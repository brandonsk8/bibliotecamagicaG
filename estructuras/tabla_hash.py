# -----------------------------------------------------------
#  Tabla Hash (versión completa con búsqueda y eliminación)
# -----------------------------------------------------------

class TablaHash:
    def __init__(self, tamaño=50):
        self.tamaño = tamaño
        self.tabla = [[] for _ in range(tamaño)]

    # -----------------------------------------------------------
    #  Función hash segura (convierte siempre a string)
    # -----------------------------------------------------------
    def _hash(self, clave) -> int:
        clave_str = str(clave).strip()
        return hash(clave_str) % self.tamaño

    # -----------------------------------------------------------
    #  Inserción
    # -----------------------------------------------------------
    def insertar(self, clave, valor):
        clave_str = str(clave).strip()
        indice = self._hash(clave_str)
        for i, (k, v) in enumerate(self.tabla[indice]):
            if k == clave_str:
                self.tabla[indice][i] = (clave_str, valor)
                return
        self.tabla[indice].append((clave_str, valor))
        print(f"[DEBUG] Insertado en hash: {clave_str}")

    # -----------------------------------------------------------
    #  Búsqueda
    # -----------------------------------------------------------
    def buscar(self, clave):
        clave_str = str(clave).strip()
        indice = self._hash(clave_str)
        for k, v in self.tabla[indice]:
            if k == clave_str:
                return v
        return None

    # -----------------------------------------------------------
    #  Eliminación
    # -----------------------------------------------------------
    def eliminar(self, clave):
        clave_str = str(clave).strip()
        indice = self._hash(clave_str)
        for i, (k, v) in enumerate(self.tabla[indice]):
            if k == clave_str:
                del self.tabla[indice][i]
                print(f"[DEBUG] Eliminado del hash: {clave_str}")
                return True
        print(f"[DEBUG] Libro con ISBN {clave_str} no encontrado en hash.")
        return False

    def __len__(self):
        return sum(len(lista) for lista in self.tabla)
