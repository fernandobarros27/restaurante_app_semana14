# Restaurante App - Semana 14

## Descripción

Esta versión corresponde a la evolución del proyecto `restaurante_app` para la Semana 14 de la asignatura.

El objetivo principal es aplicar componentes y contenedores de Tkinter/ttk para mejorar la interfaz gráfica, manteniendo la arquitectura modular trabajada anteriormente y la persistencia mediante archivos JSON.

## Estructura

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
├── main.py
└── README.md
```

## Componentes y contenedores utilizados

La interfaz utiliza Tkinter y ttk. Se incorporaron `Frame`, `LabelFrame`, `Label`, `Entry`, `Button`, `Treeview`, `Scrollbar` y mensajes de `messagebox`.

Para organizar los componentes se utilizan los gestores de geometría `pack()` y `grid()`.

## Mejoras realizadas en Semana 14

- Se incorporó una ventana gráfica de inicio de sesión.
- Se mantuvo la separación entre interfaz, modelos, servicios y datos.
- Se creó una ventana principal con zonas diferenciadas para navegación, formulario y tabla.
- Se incorporó una consulta gráfica de usuarios.
- Se implementó la gestión de productos desde la interfaz.
- Se mejoró la presentación de los registros mediante `ttk.Treeview`.
- Se agregaron botones con `command=` para ejecutar las operaciones.
- Se actualizaron las tablas después de registrar, actualizar o eliminar productos.
- La interfaz no realiza lectura o escritura directa de los archivos JSON.

## Operaciones sobre productos

La sección Productos permite:

1. Registrar un producto.
2. Cargar/consultar un producto mediante su código.
3. Actualizar nombre, categoría, precio y stock.
4. Eliminar un producto.
5. Consultar los productos registrados mediante la tabla.

Las validaciones y operaciones del dominio se encuentran en `RestauranteServicio`.

## Persistencia

Los productos se almacenan en:

```text
datos/productos.json
```

Los usuarios se almacenan en:

```text
datos/usuarios.json
```

La lectura y escritura se realiza mediante `ArchivoServicio`.

## Inicio de sesión

Para realizar las pruebas se puede utilizar:

```text
Usuario: admin
Contraseña: 1234
```

## Ejecución

Se requiere Python 3.

Desde la carpeta del proyecto ejecutar:

```bash
python main.py
```

La aplicación abre primero el inicio de sesión y, después de validar las credenciales, muestra el panel principal.

## Comprobación realizada

Se verificaron las operaciones principales de la aplicación:

- Inicio de sesión.
- Consulta de usuarios.
- Registro de productos.
- Consulta de productos.
- Actualización de productos.
- Eliminación de productos.
- Persistencia de cambios en `productos.json`.
- Separación de responsabilidades entre interfaz, servicios, modelos y datos.
