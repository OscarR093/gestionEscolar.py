import flet as ft
import documents  # Módulo personalizado para manejar datos y utilidades

# Cargar datos iniciales
profesores = documents.cargar_datos("profesores.json")

# Utilidades de manejo de datos
def filtrar_profesores(profesores, filtro):
    """Filtra los profesores por ID o Nombre."""
    if not filtro:
        return profesores
    filtro = filtro.lower()
    return [
        profesor for profesor in profesores
        if str(profesor["id"]).startswith(filtro) or profesor["nombre"].lower().startswith(filtro)
    ]

def eliminar_profesor(profesores, profesor_id):
    """Elimina un profesor del listado por ID."""
    return [profesor for profesor in profesores if profesor["id"] != profesor_id]

def agregar_profesor(profesores, nombre, apellido, telefono, direccion):
    """Agrega un nuevo profesor al listado."""
    nuevo_profesor = {
        "id": documents.generar_id_unico(profesores),
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "direccion": direccion
    }
    profesores.append(nuevo_profesor)
    return profesores

# Componentes de UI
def crear_formulario(page, profesores):
    """Crea el formulario de ingreso de datos."""
    nombre_input = ft.TextField(label="Nombre", width=200)
    apellido_input = ft.TextField(label="Apellido", width=200)
    telefono_input = ft.TextField(label="Teléfono", width=200)
    direccion_input = ft.TextField(label="Dirección", width=200)

    def agregar_handler(e):
        nonlocal profesores
        profesores = agregar_profesor(
            profesores,
            nombre_input.value,
            apellido_input.value,
            telefono_input.value,
            direccion_input.value
        )
        documents.guardar_datos("profesores.json", profesores)
        actualizar_tabla(page, profesores)

    boton_agregar = ft.ElevatedButton("Agregar Profesor", on_click=agregar_handler)

    formulario_fila = ft.Row(
        [
            ft.Column([nombre_input, telefono_input], spacing=10),
            ft.Column([apellido_input, direccion_input], spacing=10),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
    
    return ft.Column(
        [formulario_fila, boton_agregar],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

def crear_filtro_busqueda(page, profesores):
    """Crea el filtro de búsqueda y botones de acción."""
    filtro_input = ft.TextField(label="Filtrar por ID o Nombre", width=300)

    def buscar_handler(e):
        actualizar_tabla(page, profesores, filtro_input.value)

    def restaurar_handler(e):
        filtro_input.value = ""
        actualizar_tabla(page, profesores)

    return ft.Row(
        [
            filtro_input,
            ft.ElevatedButton("Buscar", on_click=buscar_handler),
            ft.ElevatedButton("Restaurar", on_click=restaurar_handler)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

def crear_tabla(page, profesores, filtro):
    """Crea una tabla desplazable con los datos filtrados."""
    profesores_filtrados = filtrar_profesores(profesores, filtro)

    def eliminar_handler(e, profesor_id):
        nonlocal profesores
        profesores = eliminar_profesor(profesores, profesor_id)
        documents.guardar_datos("profesores.json", profesores)
        actualizar_tabla(page, profesores)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Apellido")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(profesor["id"]))),
                    ft.DataCell(ft.Text(profesor["nombre"])),
                    ft.DataCell(ft.Text(profesor["apellido"])),
                    ft.DataCell(ft.Text(profesor["telefono"])),
                    ft.DataCell(ft.Text(profesor["direccion"])),
                    ft.DataCell(ft.ElevatedButton("Eliminar", on_click=lambda e, pid=profesor["id"]: eliminar_handler(e, pid))),
                ]
            ) for profesor in profesores_filtrados
        ]
    )
    return ft.Column([tabla], scroll=ft.ScrollMode.AUTO, height=300)

# Función principal
def actualizar_tabla(page, profesores, filtro=""):
    """Actualiza toda la interfaz con los datos actuales."""
    page.controls.clear()
    page.add(crear_filtro_busqueda(page, profesores))
    page.add(crear_formulario(page, profesores))
    page.add(crear_tabla(page, profesores, filtro))
    page.update()

def main(page: ft.Page):
    """Configura la aplicación principal."""
    page.title = "Gestión de Profesores"
    page.window_width = 800
    page.window_height = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    actualizar_tabla(page, profesores)

ft.app(target=main)
