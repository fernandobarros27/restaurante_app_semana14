import tkinter as tk
from tkinter import ttk, messagebox

from modelos.producto import Producto
from servicios.restaurante_servicio import RestauranteServicio


class MainView(tk.Toplevel):
    """Ventana principal para consultar usuarios y gestionar productos."""

    def __init__(self, parent: tk.Tk, servicio: RestauranteServicio) -> None:
        super().__init__(parent)

        self.parent = parent
        self.servicio = servicio

        self.title("Restaurante App - Panel principal")
        self.geometry("1050x650")
        self.minsize(950, 580)

        self._crear_estilos()
        self._crear_interfaz()
        self.mostrar_productos()

        self.protocol("WM_DELETE_WINDOW", self.cerrar_sesion)

    def _crear_estilos(self) -> None:
        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure("Titulo.TLabel", font=("Segoe UI", 18, "bold"))
        estilo.configure("Seccion.TLabel", font=("Segoe UI", 11, "bold"))
        estilo.configure("Accion.TButton", padding=6)
        estilo.configure("Treeview", rowheight=28)

    def _crear_interfaz(self) -> None:
        # Contenedor principal
        principal = ttk.Frame(self, padding=15)
        principal.pack(fill="both", expand=True)

        encabezado = ttk.Frame(principal)
        encabezado.pack(fill="x", pady=(0, 12))

        ttk.Label(
            encabezado,
            text="Panel de gestión del restaurante",
            style="Titulo.TLabel"
        ).pack(side="left")

        ttk.Button(
            encabezado,
            text="Cerrar sesión",
            command=self.cerrar_sesion
        ).pack(side="right")

        # Navegación
        navegacion = ttk.LabelFrame(
            principal,
            text="Navegación",
            padding=8
        )
        navegacion.pack(fill="x", pady=(0, 12))

        ttk.Button(
            navegacion,
            text="👥 Usuarios",
            command=self.mostrar_usuarios
        ).pack(side="left", padx=5)

        ttk.Button(
            navegacion,
            text="🍔 Productos",
            command=self.mostrar_productos
        ).pack(side="left", padx=5)

        # Área de contenido
        self.contenido = ttk.Frame(principal)
        self.contenido.pack(fill="both", expand=True)

        self.mostrar_productos()

    def limpiar_contenido(self) -> None:
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_productos(self) -> None:
        self.limpiar_contenido()

        ttk.Label(
            self.contenido,
            text="Gestión de productos",
            style="Seccion.TLabel"
        ).pack(anchor="w", pady=(0, 8))

        cuerpo = ttk.Frame(self.contenido)
        cuerpo.pack(fill="both", expand=True)

        # Formulario
        formulario = ttk.LabelFrame(
            cuerpo,
            text="Datos del producto",
            padding=15
        )
        formulario.pack(fill="x", pady=(0, 10))

        ttk.Label(formulario, text="Código:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.txt_codigo = ttk.Entry(formulario, width=22)
        self.txt_codigo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Nombre:").grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )
        self.txt_nombre = ttk.Entry(formulario, width=28)
        self.txt_nombre.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Categoría:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.txt_categoria = ttk.Entry(formulario, width=22)
        self.txt_categoria.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Precio:").grid(
            row=1, column=2, sticky="w", padx=5, pady=5
        )
        self.txt_precio = ttk.Entry(formulario, width=28)
        self.txt_precio.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Stock:").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.txt_stock = ttk.Entry(formulario, width=22)
        self.txt_stock.grid(row=2, column=1, padx=5, pady=5)

        acciones = ttk.Frame(formulario)
        acciones.grid(row=2, column=2, columnspan=2, sticky="e", pady=5)

        ttk.Button(
            acciones,
            text="Registrar",
            command=self.registrar_producto
        ).pack(side="left", padx=3)

        ttk.Button(
            acciones,
            text="Cargar / Consultar",
            command=self.cargar_producto
        ).pack(side="left", padx=3)

        ttk.Button(
            acciones,
            text="Actualizar",
            command=self.actualizar_producto
        ).pack(side="left", padx=3)

        ttk.Button(
            acciones,
            text="Eliminar",
            command=self.eliminar_producto
        ).pack(side="left", padx=3)

        ttk.Button(
            acciones,
            text="Limpiar",
            command=self.limpiar_formulario
        ).pack(side="left", padx=3)

        # Tabla
        tabla_frame = ttk.LabelFrame(
            cuerpo,
            text="Productos registrados",
            padding=8
        )
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")

        self.tabla_productos = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings"
        )

        encabezados = {
            "codigo": "Código",
            "nombre": "Nombre",
            "categoria": "Categoría",
            "precio": "Precio",
            "stock": "Stock"
        }

        anchos = {
            "codigo": 100,
            "nombre": 230,
            "categoria": 160,
            "precio": 100,
            "stock": 80
        }

        for columna in columnas:
            self.tabla_productos.heading(
                columna,
                text=encabezados[columna]
            )
            self.tabla_productos.column(
                columna,
                width=anchos[columna],
                anchor="center"
            )

        scroll = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=scroll.set)

        self.tabla_productos.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def mostrar_usuarios(self) -> None:
        self.limpiar_contenido()

        ttk.Label(
            self.contenido,
            text="Consulta de usuarios",
            style="Seccion.TLabel"
        ).pack(anchor="w", pady=(0, 8))

        marco = ttk.LabelFrame(
            self.contenido,
            text="Usuarios registrados",
            padding=10
        )
        marco.pack(fill="both", expand=True)

        columnas = ("identificacion", "nombre", "correo", "usuario")
        tabla = ttk.Treeview(
            marco,
            columns=columnas,
            show="headings"
        )

        encabezados = {
            "identificacion": "Identificación",
            "nombre": "Nombre",
            "correo": "Correo",
            "usuario": "Usuario"
        }

        for columna in columnas:
            tabla.heading(columna, text=encabezados[columna])
            tabla.column(columna, width=180, anchor="center")

        for usuario in self.servicio.listar_usuarios():
            tabla.insert(
                "",
                "end",
                values=(
                    usuario.identificacion,
                    usuario.nombre,
                    usuario.correo,
                    usuario.usuario
                )
            )

        scroll = ttk.Scrollbar(
            marco,
            orient="vertical",
            command=tabla.yview
        )
        tabla.configure(yscrollcommand=scroll.set)

        tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def registrar_producto(self) -> None:
        try:
            producto = Producto(
                self.txt_codigo.get().strip(),
                self.txt_nombre.get().strip(),
                self.txt_categoria.get().strip(),
                float(self.txt_precio.get()),
                int(self.txt_stock.get())
            )
        except ValueError:
            messagebox.showwarning(
                "Datos incorrectos",
                "Precio y stock deben contener valores numéricos."
            )
            return

        correcto, mensaje = self.servicio.registrar_producto(producto)

        if correcto:
            messagebox.showinfo("Registro", mensaje)
            self.limpiar_formulario()
            self.mostrar_productos()
        else:
            messagebox.showwarning("No se pudo registrar", mensaje)

    def cargar_producto(self) -> None:
        codigo = self.txt_codigo.get().strip()

        if not codigo:
            messagebox.showwarning(
                "Consulta",
                "Ingrese el código del producto."
            )
            return

        producto = self.servicio.buscar_producto(codigo)

        if producto is None:
            messagebox.showinfo(
                "Consulta",
                "Producto no encontrado."
            )
            return

        self.txt_nombre.delete(0, tk.END)
        self.txt_nombre.insert(0, producto.nombre)

        self.txt_categoria.delete(0, tk.END)
        self.txt_categoria.insert(0, producto.categoria)

        self.txt_precio.delete(0, tk.END)
        self.txt_precio.insert(0, str(producto.precio))

        self.txt_stock.delete(0, tk.END)
        self.txt_stock.insert(0, str(producto.stock))

    def actualizar_producto(self) -> None:
        codigo = self.txt_codigo.get().strip()

        if not codigo:
            messagebox.showwarning(
                "Actualización",
                "Ingrese el código del producto."
            )
            return

        try:
            precio = float(self.txt_precio.get())
            stock = int(self.txt_stock.get())
        except ValueError:
            messagebox.showwarning(
                "Datos incorrectos",
                "Precio y stock deben contener valores numéricos."
            )
            return

        correcto, mensaje = self.servicio.actualizar_producto(
            codigo,
            self.txt_nombre.get().strip(),
            self.txt_categoria.get().strip(),
            precio,
            stock
        )

        if correcto:
            messagebox.showinfo("Actualización", mensaje)
            self.mostrar_productos()
        else:
            messagebox.showwarning("Actualización", mensaje)

    def eliminar_producto(self) -> None:
        codigo = self.txt_codigo.get().strip()

        if not codigo:
            messagebox.showwarning(
                "Eliminación",
                "Ingrese el código del producto."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar el producto {codigo}?"
        )

        if not confirmar:
            return

        correcto, mensaje = self.servicio.eliminar_producto(codigo)

        if correcto:
            messagebox.showinfo("Eliminación", mensaje)
            self.limpiar_formulario()
            self.mostrar_productos()
        else:
            messagebox.showwarning("Eliminación", mensaje)

    def limpiar_formulario(self) -> None:
        for entrada in (
            self.txt_codigo,
            self.txt_nombre,
            self.txt_categoria,
            self.txt_precio,
            self.txt_stock
        ):
            entrada.delete(0, tk.END)

        self.txt_codigo.focus()

    def mostrar_productos_en_tabla(self) -> None:
        self.mostrar_productos()

    def cerrar_sesion(self) -> None:
        self.destroy()
        self.parent.deiconify()
