class Usuario:
    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        usuario: str = "",
        password: str = ""
    ) -> None:
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.usuario = usuario
        self.password = password

    def __str__(self) -> str:
        return (
            f"Identificación: {self.identificacion}\n"
            f"Nombre: {self.nombre}\n"
            f"Correo: {self.correo}"
        )

    def to_dict(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "usuario": self.usuario,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, datos: dict):
        return cls(
            str(datos.get("identificacion", "")),
            str(datos.get("nombre", "")),
            str(datos.get("correo", "")),
            str(datos.get("usuario", "")),
            str(datos.get("password", ""))
        )
