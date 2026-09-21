from pathlib import Path
from typing import Optional

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


BASE_DIR = Path(__file__).resolve().parent.parent
PRODUCTOS_JSON = BASE_DIR / "datos" / "productos.json"
USUARIOS_JSON = BASE_DIR / "datos" / "usuarios.json"


class RestauranteServicio:
    """Contiene las reglas de negocio y la persistencia del restaurante."""

    def __init__(self) -> None:
        self.archivo_productos = ArchivoServicio(str(PRODUCTOS_JSON))
        self.archivo_usuarios = ArchivoServicio(str(USUARIOS_JSON))
        self.productos: list[Producto] = []
        self.usuarios: list[Usuario] = []
        self.cargar_datos()

    def cargar_datos(self) -> None:
        self.productos = [
            Producto.from_dict(item)
            for item in self.archivo_productos.leer()
        ]
        self.usuarios = [
            Usuario.from_dict(item)
            for item in self.archivo_usuarios.leer()
        ]

    # ---------------- PRODUCTOS ----------------

    def registrar_producto(self, producto: Producto) -> tuple[bool, str]:
        if not producto.codigo or not producto.nombre or not producto.categoria:
            return False, "Complete todos los campos del producto."

        if producto.precio < 0:
            return False, "El precio no puede ser negativo."

        if producto.stock < 0:
            return False, "El stock no puede ser negativo."

        if self.buscar_producto(producto.codigo) is not None:
            return False, "Ya existe un producto con ese código."

        self.productos.append(producto)
        self.guardar_productos()
        return True, "Producto registrado correctamente."

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        for producto in self.productos:
            if producto.codigo.lower() == codigo.strip().lower():
                return producto
        return None

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int
    ) -> tuple[bool, str]:
        producto = self.buscar_producto(codigo)

        if producto is None:
            return False, "Producto no encontrado."

        if not nombre or not categoria:
            return False, "Complete todos los campos del producto."

        if precio < 0 or stock < 0:
            return False, "Precio y stock no pueden ser negativos."

        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        producto.stock = stock
        self.guardar_productos()
        return True, "Producto actualizado correctamente."

    def eliminar_producto(self, codigo: str) -> tuple[bool, str]:
        producto = self.buscar_producto(codigo)

        if producto is None:
            return False, "Producto no encontrado."

        self.productos.remove(producto)
        self.guardar_productos()
        return True, "Producto eliminado correctamente."

    def listar_productos(self) -> list[Producto]:
        return self.productos.copy()

    def guardar_productos(self) -> None:
        self.archivo_productos.guardar(
            [producto.to_dict() for producto in self.productos]
        )

    # ---------------- USUARIOS ----------------

    def listar_usuarios(self) -> list[Usuario]:
        return self.usuarios.copy()

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        for usuario in self.usuarios:
            if usuario.identificacion == identificacion:
                return usuario
        return None

    def validar_login(self, usuario: str, password: str) -> bool:
        for registrado in self.usuarios:
            if (
                registrado.usuario == usuario
                and registrado.password == password
            ):
                return True
        return False

    def obtener_categorias(self) -> set[str]:
        return {producto.categoria for producto in self.productos}
