import flet as ft
import documents

# Inicializar la variable global
timeFormatError = False

def validate_time(e):
    global timeFormatError
    input_value = e.control.value
    if len(input_value) == 5 and input_value[2] == ":":
        try:
            hours, minutes = map(int, input_value.split(":"))
            if 0 <= hours < 24 and 0 <= minutes < 60:
                e.control.error_text = None
                timeFormatError = False
            else:
                e.control.error_text = "Formato inválido (00:00 - 23:59)"
                timeFormatError = True
        except ValueError:
            e.control.error_text = "Formato inválido (00:00 - 23:59)"
            timeFormatError = True
    else:
        e.control.error_text = "Debe ser HH:MM"
        timeFormatError = True
    e.page.update()

def main(page: ft.Page):
    materias = documents.cargar_datos("materias.json")

    error_dialog = ft.AlertDialog(
        title=ft.Text("Error de validación"),
        content=ft.Text("Por favor, completa todos los campos o revisa el formato de hora"),
        actions=[
            ft.TextButton("OK", on_click=lambda e: page.close(error_dialog)),
        ],
    )

    def actualizar_tabla():
        tabla.controls.clear()
        tabla.controls.append(
            ft.Row(
                [
                    ft.Text("ID", weight=ft.FontWeight.BOLD, width=100),
                    ft.Text("Nombre", weight=ft.FontWeight.BOLD, width=200),
                    ft.Text("Hora Inicio", weight=ft.FontWeight.BOLD, width=150),
                    ft.Text("Hora Final", weight=ft.FontWeight.BOLD, width=150),
                    ft.Text("Acciones", weight=ft.FontWeight.BOLD, width=150),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            )
        )
        for materia in materias:
            tabla.controls.append(
                ft.Row(
                    [
                        ft.Text(materia["id"], width=100),
                        ft.Text(materia["nombre"], width=200),
                        ft.Text(materia["HoraInicio"], width=150),
                        ft.Text(materia["HoraFinal"], width=150),
                        ft.ElevatedButton(
                            "Eliminar", on_click=lambda e, mid=materia["id"]: eliminar_materia(mid)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                )
            )
        page.update()

    def eliminar_materia(materia_id):
        nonlocal materias
        materias = [m for m in materias if m["id"] != materia_id]
        documents.guardar_datos("materias.json", materias)
        actualizar_tabla()

    def agregar_materia(e):
        nonlocal materias
        global timeFormatError
        if (
            not nombre_input.value
            or not hora_inicio_input.value
            or not hora_final_input.value
            or timeFormatError
        ):
            page.dialog = error_dialog
            error_dialog.open = True
            page.update()
            return

        nueva_materia = {
            "id": documents.generar_id_unico(materias),
            "nombre": nombre_input.value,
            "HoraInicio": hora_inicio_input.value,
            "HoraFinal": hora_final_input.value,
            "asignada": False,
        }

        materias.append(nueva_materia)
        documents.guardar_datos("materias.json", materias)
        nombre_input.value = hora_inicio_input.value = hora_final_input.value = ""
        page.snack_bar = ft.SnackBar(ft.Text("Materia Capturada Correctamente!"))
        page.snack_bar.open = True
        actualizar_tabla()

    nombre_input = ft.TextField(label="Nombre", width=200)
    hora_inicio_input = ft.TextField(
        label="Hora Inicio (HH:MM)", width=150, on_change=validate_time
    )
    hora_final_input = ft.TextField(
        label="Hora Final (HH:MM)", width=150, on_change=validate_time
    )

    formulario = ft.Row(
        [
            nombre_input,
            hora_inicio_input,
            hora_final_input,
            ft.ElevatedButton("Agregar", on_click=agregar_materia),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    tabla = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    containerTabla = ft.Container(
        content=ft.Column(
            controls=[tabla],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=850,
        height=400,
        padding=20,
    )

    actualizar_tabla()

    return ft.Column(
        controls=[
            ft.Text("Gestión de Materias", size=24, weight=ft.FontWeight.BOLD),
            formulario,
            containerTabla,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )