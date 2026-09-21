import tkinter as tk
from tkinter import ttk, messagebox

from servicios.restaurante_servicio import RestauranteServicio
from ui.main_view import MainView


class LoginView(tk.Tk):
    """Ventana de acceso al sistema."""

    def __init__(self) -> None:
        super().__init__()

        self.servicio = RestauranteServicio()

        self.title("Restaurante App - Inicio de sesión")
        self.geometry("430x330")
        self.resizable(False, False)
        self.configure(padx=20, pady=20)

        self._crear_estilos()
        self._crear_interfaz()

    def _crear_estilos(self) -> None:
        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure("Titulo.TLabel", font=("Segoe UI", 20, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 10))
        estilo.configure("Accion.TButton", font=("Segoe UI", 10, "bold"), padding=8)

    def _crear_interfaz(self) -> None:
        contenedor = ttk.Frame(self, padding=15)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor,
            text="🍽 RESTAURANTE APP",
            style="Titulo.TLabel"
        ).pack(pady=(5, 5))

        ttk.Label(
            contenedor,
            text="Sistema de gestión de productos",
            style="Subtitulo.TLabel"
        ).pack(pady=(0, 20))

        formulario = ttk.LabelFrame(
            contenedor,
            text="Acceso al sistema",
            padding=18
        )
        formulario.pack(fill="x")

        ttk.Label(formulario, text="Usuario:").grid(
            row=0, column=0, sticky="w", pady=7
        )
        self.txt_usuario = ttk.Entry(formulario, width=30)
        self.txt_usuario.grid(row=0, column=1, pady=7, padx=(10, 0))

        ttk.Label(formulario, text="Contraseña:").grid(
            row=1, column=0, sticky="w", pady=7
        )
        self.txt_password = ttk.Entry(formulario, width=30, show="*")
        self.txt_password.grid(row=1, column=1, pady=7, padx=(10, 0))

        ttk.Button(
            formulario,
            text="Ingresar",
            command=self.iniciar_sesion,
            style="Accion.TButton"
        ).grid(row=2, column=0, columnspan=2, pady=(18, 5))

        ttk.Label(
            contenedor,
            text="Usuario de prueba: admin  |  Contraseña: 1234"
        ).pack(pady=15)

    def iniciar_sesion(self) -> None:
        usuario = self.txt_usuario.get().strip()
        password = self.txt_password.get()

        if self.servicio.validar_login(usuario, password):
            self.withdraw()
            ventana = MainView(self, self.servicio)
            ventana.grab_set()
        else:
            messagebox.showerror(
                "Acceso denegado",
                "Usuario o contraseña incorrectos."
            )
