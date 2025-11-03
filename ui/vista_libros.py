import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from modelos.libro import Libro

class VistaLibros(ttk.Frame):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema
        self._crear_interfaz()

    # -----------------------------------------------------------
    # INTERFAZ PRINCIPAL
    # -----------------------------------------------------------
    def _crear_interfaz(self):
        ttk.Label(
            self,
            text="📚 GESTIÓN DE LIBROS",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=15)

        ttk.Label(
            self,
            text="Agrega, busca, elimina y visualiza libros sincronizados con las estructuras AVL, Hash, Lista Doble y B+.",
            font=("Segoe UI", 11)
        ).pack(pady=5)

        # Campo y tipo de búsqueda
        frame_busqueda = ttk.Frame(self)
        frame_busqueda.pack(pady=10)

        self.combo_tipo = ttk.Combobox(
            frame_busqueda,
            state="readonly",
            values=["Título", "ISBN", "Autor", "Género", "Año"],
            width=12
        )
        self.combo_tipo.set("Título")
        self.combo_tipo.pack(side=LEFT, padx=5)

        self.entry_busqueda = ttk.Entry(frame_busqueda, width=40)
        self.entry_busqueda.pack(side=LEFT, padx=5)

        ttk.Button(
            frame_busqueda,
            text="🔍 Buscar",
            bootstyle="info-outline",
            command=self.buscar_libro
        ).pack(side=LEFT, padx=5)
        ttk.Button(
            frame_busqueda,
            text="🔄 Mostrar todos",
            bootstyle="secondary-outline",
            command=self.actualizar_tabla
        ).pack(side=LEFT, padx=5)

        # Tabla principal
        self.tabla = ttk.Treeview(
            self,
            columns=("titulo", "autor", "isbn", "anio", "genero", "estado",
                    "origen", "destino", "prioridad"),
            show="headings",
            height=15,
            bootstyle="dark"
        )

        encabezados = ["Título", "Autor", "ISBN", "Año", "Género", "Estado",
                    "Biblioteca Origen", "Biblioteca Destino", "Prioridad"]

        for col, texto in zip(self.tabla["columns"], encabezados):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=140, anchor=CENTER)

        for col, texto in zip(self.tabla["columns"], encabezados):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=150, anchor=CENTER)
        self.tabla.pack(fill=BOTH, expand=True, padx=15, pady=10)

        # Botones inferiores
        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=10)
        ttk.Button(
            frame_botones,
            text="➕ Agregar libro",
            bootstyle="success-outline",
            command=self.abrir_ventana_agregar
        ).pack(side=LEFT, padx=5)
        ttk.Button(
            frame_botones,
            text="❌ Eliminar libro",
            bootstyle="danger-outline",
            command=self.eliminar_libro
        ).pack(side=LEFT, padx=5)
        ttk.Button(
            frame_botones,
            text="🔄 Actualizar tabla",
            bootstyle="info-outline",
            command=self.actualizar_tabla
        ).pack(side=LEFT, padx=5)
        ttk.Button(
            frame_botones,
            text="📖 Detalles",
            bootstyle="secondary-outline",
            command=self.ver_detalles
        ).pack(side=LEFT, padx=5)

    # -----------------------------------------------------------
    # ACTUALIZAR TABLA
    # -----------------------------------------------------------
    def actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        actual = self.sistema.coleccion.primero
        contador = 0
        while actual:
            l = actual.libro
            self.tabla.insert(
    "",
    "end",
    values=(
        l.titulo, l.autor, l.isbn, l.anio, l.genero, l.estado,
        l.biblioteca_origen, l.biblioteca_destino, l.prioridad
    )
)

            contador += 1
            actual = actual.siguiente

        print(f"[DEBUG] Tabla actualizada con {contador} libros.")

    # -----------------------------------------------------------
    # ABRIR FORMULARIO PARA AGREGAR LIBRO
    # -----------------------------------------------------------
    def abrir_ventana_agregar(self):
        self.ventana_agregar = ttk.Toplevel(self)
        self.ventana_agregar.title("Agregar Libro")
        self.ventana_agregar.geometry("600x620")
        self.ventana_agregar.resizable(False, False)

        campos = [
            ("Título", "entry_titulo"),
            ("Autor", "entry_autor"),
            ("ISBN", "entry_isbn"),
            ("Año", "entry_anio"),
            ("Género", "entry_genero"),
            ("Estado", "entry_estado"),
            ("Biblioteca Origen", "entry_origen"),
            ("Biblioteca Destino", "entry_destino"),
            ("Prioridad", "entry_prioridad"),
        ]

        for texto, atributo in campos:
            ttk.Label(self.ventana_agregar, text=texto, font=("Segoe UI", 10, "bold")).pack(pady=5)
            entry = ttk.Entry(self.ventana_agregar, width=35)
            entry.pack()
            setattr(self, atributo, entry)

        self.entry_estado.insert(0, "Disponible")

        ttk.Button(
            self.ventana_agregar,
            text="Guardar",
            bootstyle="success",
            command=self.guardar_libro
        ).pack(pady=15)

        self.ventana_agregar.bind("<Return>", lambda e: self.guardar_libro())

    # -----------------------------------------------------------
    # GUARDAR LIBRO
    # -----------------------------------------------------------
    def guardar_libro(self):
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        isbn = self.entry_isbn.get().strip()
        anio = self.entry_anio.get().strip()
        genero = self.entry_genero.get().strip()
        estado = self.entry_estado.get().strip()
        origen = self.entry_origen.get().strip()
        destino = self.entry_destino.get().strip()
        prioridad = self.entry_prioridad.get().strip()

        if not titulo or not autor or not isbn:
            messagebox.showerror("Error", "Los campos Título, Autor e ISBN son obligatorios.")
            return

        try:
            anio = int(anio)
        except ValueError:
            messagebox.showerror("Error", "El campo Año debe ser un número entero.")
            return

        #  Crear c el objeto Libro con todos los campos
        nuevo_libro = Libro(titulo, autor, isbn, anio, genero, estado, origen, destino, prioridad)

        if self.sistema.coleccion.existe_conflicto_isbn(nuevo_libro):
            messagebox.showerror("Error", f"Ya existe otro libro con el ISBN {isbn}.")
            return

        self.sistema.agregar_libro(nuevo_libro)
        self.actualizar_tabla()
        messagebox.showinfo("Éxito", f"📘 Libro '{titulo}' agregado correctamente.")
        self.ventana_agregar.destroy()


    # -----------------------------------------------------------
    # BUSCAR LIBRO AVANZADO
    # -----------------------------------------------------------
    def buscar_libro(self):
        tipo = self.combo_tipo.get()
        criterio = self.entry_busqueda.get().strip()

        if not criterio:
            messagebox.showinfo("Buscar", "Ingrese un valor para buscar.")
            return

        resultados = []

        if tipo == "Título":
            libro = self.sistema.avl.buscar(criterio)
            if libro:
                resultados.append(libro)

        elif tipo == "ISBN":
            libro = self.sistema.hash.buscar(criterio)
            if libro:
                resultados.append(libro)

        elif tipo == "Autor":
            actual = self.sistema.coleccion.primero
            while actual:
                if criterio.lower() in actual.libro.autor.lower():
                    resultados.append(actual.libro)
                actual = actual.siguiente

        elif tipo == "Género":
            resultados = self.sistema.bmas.buscar(criterio)

        elif tipo == "Año":
            actual = self.sistema.coleccion.primero
            while actual:
                if str(actual.libro.anio).lower() == criterio.lower():
                    resultados.append(actual.libro)
                actual = actual.siguiente

        if resultados:
            self._mostrar_resultados(resultados)
        else:
            messagebox.showinfo("Sin resultados", f"No se encontró ningún libro con {tipo.lower()} '{criterio}'.")

    # -----------------------------------------------------------
    # MOSTRAR RESULTADOS
    # -----------------------------------------------------------
    def _mostrar_resultados(self, lista):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for libro in lista:
            item = self.tabla.insert(
                "",
                END,
                values=(libro.titulo, libro.autor, libro.isbn, libro.anio, libro.genero, libro.estado)
            )
            self.tabla.item(item, tags=("resaltado",))

        self.tabla.tag_configure("resaltado", background="#133E7C", foreground="white")
        messagebox.showinfo("Resultados de búsqueda", f"Se encontraron {len(lista)} coincidencias.")

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
                self.tabla.delete(seleccion)
                messagebox.showinfo("Eliminado", f"Libro '{titulo}' eliminado correctamente.")
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el libro '{titulo}'.")

            self.actualizar_tabla()

    # -----------------------------------------------------------
    # VER DETALLES
    # -----------------------------------------------------------
    def ver_detalles(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Detalles", "Seleccione un libro primero.")
            return

        item = self.tabla.item(seleccion)
        valores = item["values"]

        # Evitar errores si no hay todos los campos
        titulo, autor, isbn, anio, genero, estado, *resto = valores
        origen = resto[0] if len(resto) > 0 else "N/A"
        destino = resto[1] if len(resto) > 1 else "N/A"
        prioridad = resto[2] if len(resto) > 2 else "N/A"

        detalle = f"""

📖 Título: {titulo}
👤 Autor: {autor}
🔢 ISBN: {isbn}
📅 Año: {anio}
🏷️ Género: {genero}
📦 Estado: {estado}

🏛️ Biblioteca Origen: {origen}
🏙️ Biblioteca Destino: {destino}
⭐ Prioridad: {prioridad}
"""

        messagebox.showinfo("Detalles del libro", detalle)
