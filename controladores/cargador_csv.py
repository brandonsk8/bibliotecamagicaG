import csv
from modelos.libro import Libro
from modelos.biblioteca import Biblioteca
import unicodedata

class CargadorCSV:
    def __init__(self, sistema):
        self.sistema = sistema

    # -----------------------------------------------------------
    #  CARGAR LIBROS DESDE CSV (mejorado)
    # -----------------------------------------------------------
    def cargar_libros(self, ruta):
        try:
            count, errores = 0, 0
            with open(ruta, encoding="utf-8-sig", errors="ignore", newline="") as f:
                reader = csv.DictReader(f)
                columnas = [c.strip().lower() for c in reader.fieldnames]
                print(f"[DEBUG] Encabezados detectados: {columnas}")

                for row in reader:
                    try:
                        libro = Libro(
                            titulo=row.get("Título", row.get("Titulo", "")).strip(),
                            autor=row.get("Autor", "").strip(),
                            isbn=row.get("ISBN", "").strip(),
                            anio=row.get("Año", row.get("Anio", "0")).strip(),
                            genero=row.get("Género", row.get("Genero", "")).strip(),
                            estado=row.get("Estado", "Disponible").strip(),
                            biblioteca_origen=row.get("ID_BibliotecaOrigen", "").strip(),
                            biblioteca_destino=row.get("ID_BibliotecaDestino", "").strip(),
                            prioridad=row.get("Prioridad", "").strip()
                        )

                        # Insertar en todas las estructuras
                        self.sistema.coleccion.insertar(libro)
                        self.sistema.avl.insertar(libro)
                        self.sistema.hash.insertar(libro.isbn, libro)
                        self.sistema.bmas.insertar(libro)

                        count += 1
                    except Exception as e:
                        errores += 1
                        print(f" Error en línea {count+errores}: {e}")

            print(f" {count} libros cargados correctamente.  {errores} líneas ignoradas.")
            return count, errores

        except Exceptin as e:
            print(f" Error general al leer el archivo: {e}")
            return 0, 1
        
    # -----------------------------------------------------------
    #  CARGAR BIBLIOTECAS DESDE CSV (versión FINAL compatible con comillas)
    # -----------------------------------------------------------
    def cargar_bibliotecas(self, ruta):
        """Carga las bibliotecas desde un archivo CSV con comillas en los encabezados."""
        try:
            with open(ruta, newline='', encoding='utf-8-sig') as archivo:
                lector = csv.DictReader(archivo)

                # ✅ Limpiar comillas y espacios de los encabezados
                columnas = [c.strip().replace('"', '').lower() for c in lector.fieldnames]
                lector.fieldnames = columnas
                print(f"[DEBUG] Encabezados detectados en bibliotecas: {columnas}")

                contador = 0
                for fila in lector:
                    # 🔧 Limpiar comillas y espacios de todos los valores
                    fila = {k.strip().replace('"', ''): (v.strip().replace('"', '') if v else "") for k, v in fila.items()}

                    nombre = fila.get("nombre", "")
                    ubicacion = fila.get("ubicacion", fila.get("ubicación", ""))
                    t_ingreso = float(fila.get("t_ingreso", "0") or 0)
                    t_traspaso = float(fila.get("t_traspaso", "0") or 0)
                    intervalo = float(fila.get("dispatchinterval", "0") or 0)
                    id_biblioteca = fila.get("id_biblioteca", fila.get("id", nombre))

                    if not nombre:
                        print(f"⚠️ Fila sin nombre, omitida: {fila}")
                        continue

                    biblioteca = Biblioteca(
                        nombre=nombre,
                        ubicacion=ubicacion,
                        t_ingreso=t_ingreso,
                        t_traspaso=t_traspaso,
                        intervalo=intervalo,
                        id_biblioteca=id_biblioteca
                    )
                    self.sistema.agregar_biblioteca(biblioteca)
                    contador += 1
                    print(f"[DEBUG] Biblioteca agregada: {nombre} ({id_biblioteca})")

                print(f"[DEBUG] {contador} bibliotecas cargadas correctamente.")
                return contador

        except Exception as e:
            print(f"[ERROR] Fallo al cargar bibliotecas: {e}")
            return 0



    # ===========================================================
    #  CARGAR CONEXIONES ENTRE BIBLIOTECAS (versión segura)
    # ===========================================================
    def cargar_conexiones(self, ruta):
        """Carga las conexiones entre bibliotecas desde un CSV y las agrega al grafo."""
        if not self.sistema.grafo:
            raise ValueError("No existe un grafo inicializado en el sistema.")

        try:
            contador = 0
            with open(ruta, newline='', encoding='utf-8-sig', errors='ignore') as archivo:
                lector = csv.DictReader(archivo)

                if not lector.fieldnames:
                    raise ValueError("El archivo CSV no tiene encabezados válidos.")

                #  Limpiar comillas y espacios
                columnas = [c.strip().replace('"', '').lower() for c in lector.fieldnames]
                lector.fieldnames = columnas
                print(f"[DEBUG] Encabezados detectados en conexiones: {columnas}")

                # Detectar columnas
                col_origen = next((c for c in columnas if "origen" in c or "source" in c), None)
                col_destino = next((c for c in columnas if "destino" in c or "target" in c), None)
                col_peso = next((c for c in columnas if "costo" in c or "peso" in c or "tiempo" in c), None)

                if not col_origen or not col_destino or not col_peso:
                    raise ValueError(f"No se encontraron columnas válidas de origen, destino o peso en el CSV. ({columnas})")

                # Recorrer filas
                for fila in lector:
                    # Limpiar comillas y espacios de valores
                    fila = {k.strip().replace('"', ''): (v.strip().replace('"', '') if v else "") for k, v in fila.items()}

                    origen = fila.get(col_origen, "").strip()
                    destino = fila.get(col_destino, "").strip()
                    peso_val = fila.get(col_peso, "0").strip()

                    if not origen or not destino:
                        print(f"[WARN] Fila ignorada por datos incompletos: {fila}")
                        continue

                    # Normalizar valores (mayúsculas y sin espacios)
                    origen = origen.upper()
                    destino = destino.upper()

                    try:
                        peso = float(peso_val)
                    except ValueError:
                        peso = 1.0

                    self.sistema.grafo.agregar_arista(origen, destino, peso)
                    contador += 1
                    print(f"[DEBUG] Conexión agregada: {origen} ↔ {destino} (peso={peso})")

            print(f"[DEBUG] {contador} conexiones cargadas correctamente.")
            return contador

        except Exception as e:
            print(f"[ERROR] Fallo al cargar conexiones: {e}")
            return 0

