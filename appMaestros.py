import flet as ft
import services.conexion as con

def main(page: ft.Page):
    profesores = con.get_request("maestros")

    error_dialog = ft.AlertDialog(
        title=ft.Text("Error de validación"),
        content=ft.Text("Por favor, completa todos los campos"),
        actions=[
            ft.TextButton("OK", on_click=lambda e: page.close(error_dialog)),  # Eliminar dismiss()
        ],
    )

    def actualizar_tabla():
        tabla.controls.clear()
        tabla.controls.append(
            ft.Row(
                [
                    ft.Text("ID", weight=ft.FontWeight.BOLD),
                    ft.Text("Nombre", weight=ft.FontWeight.BOLD),
                    ft.Text("Apellido", weight=ft.FontWeight.BOLD),
                    ft.Text("Teléfono", weight=ft.FontWeight.BOLD),
                    ft.Text("Dirección", weight=ft.FontWeight.BOLD),
                    ft.Text("Acciones", weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                    )
        for profesor in profesores:
            tabla.controls.append(
                ft.Row(
                    [
                        ft.Text(profesor["id"]),
                        ft.Text(profesor["nombre"]),
                        ft.Text(profesor["apellido"]),
                        ft.Text(profesor["telefono"]),
                        ft.Text(profesor["direccion"]),
                        ft.ElevatedButton("Eliminar", on_click=lambda e, pid=profesor["id"]: eliminar_profesor(pid)),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                        )
            page.update()


    def eliminar_profesor(profesor_id):
        nonlocal profesores
        # Cargar los datos de las materias
        materias = con.get_request("materias")
    
    # Buscar los horarios relacionados con el profesor a eliminar
        horarios_a_eliminar = con.search_by_field("horarios", "id_profesor", profesor_id)
        if horarios_a_eliminar != None:
            for horario in horarios_a_eliminar:
                # Encontrar la materia asignada en el horario
                materia_id = horario["id_materia"]
                for materia in materias:
                    if materia["id"] == materia_id:
                    # Cambiar el estado de la materia a "Asignada: False"
                        materia["Asignada"] = False
                        con.put_request("materias",materia_id,materia)
                        
                con.delete_request("horarios", horario["id"])
    
        con.delete_request("maestros",profesor_id)
        profesores = con.get_request("maestros")
        # Actualizar la tabla de la UI
        page.snack_bar=ft.SnackBar(ft.Text("Profesor Eliminado Correctamente!"))
        page.snack_bar.open=True
        actualizar_tabla()


    def agregar_profesor(e):
        nonlocal profesores
        nuevo_profesor = {
            "id":"",
            "nombre": nombre_input.value,
            "apellido": apellido_input.value,
            "telefono": telefono_input.value,
            "direccion": direccion_input.value,
        }
        if not nombre_input.value or not apellido_input.value or not telefono_input.value or not direccion_input.value:
            page.dialog = error_dialog
            error_dialog.open = True
            page.update()
            return
        con.post_request("maestros",nuevo_profesor)
        profesores = con.get_request("maestros")
        nombre_input.value = apellido_input.value = telefono_input.value = direccion_input.value = ""
        page.snack_bar=ft.SnackBar(ft.Text("Profesor Agregado Correctamente"))
        page.snack_bar.open=True
        actualizar_tabla()

    # Formulario
    nombre_input = ft.TextField(label="Nombre", width=200)
    apellido_input = ft.TextField(label="Apellido", width=200)
    telefono_input = ft.TextField(label="Teléfono", width=200)
    direccion_input = ft.TextField(label="Dirección", width=200)

    formulario = ft.Column(
    [
        ft.Row(
            [
                nombre_input,
                apellido_input,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        ft.Row(
            [
                telefono_input,
                direccion_input,
                ft.ElevatedButton("Agregar", on_click=agregar_profesor),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
    ],
    spacing=10,
)


    tabla = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    containerTabla=ft.Container(
        content=ft.Column(
            controls=[tabla],  # Aquí pones la tabla
            scroll=ft.ScrollMode.AUTO,  # Habilita el desplazamiento
            alignment=ft.MainAxisAlignment.CENTER,  # Alinear los controles dentro del Column
        ),
        width=700,  # Ancho del contenedor
        height=300,  # Altura del contenedor
        alignment=ft.alignment.center,
        padding=20,
    )

    actualizar_tabla()

    return ft.Column(
        [
            ft.Text("Gestión de Profesores", size=24, weight=ft.FontWeight.BOLD),
            formulario,
            containerTabla,
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Alinea verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinea horizontalmente
        
    )
