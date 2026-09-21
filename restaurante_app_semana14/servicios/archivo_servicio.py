import json
from pathlib import Path


class ArchivoServicio:
    """Centraliza la lectura y escritura de archivos JSON."""

    def __init__(self, ruta: str) -> None:
        self.ruta = Path(ruta)

    def leer(self) -> list[dict]:
        if not self.ruta.exists():
            return []

        try:
            with self.ruta.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                return datos if isinstance(datos, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def guardar(self, datos: list[dict]) -> None:
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with self.ruta.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
