import flet as ft
import services.conexion as con


def main(page: ft.Page):
    loading_indicator = ft.Container(
        content=ft.ProgressRing(),
        alignment=ft.alignment.center,  # Centrado en el contenedor
        visible=False,  # Inicialmente oculto
        expand=True,  # Asegura que ocupe toda la pantalla
    )

    def show_loading():
        loading_indicator.visible = True
        page.update()

    def hide_loading():
        loading_indicator.visible = False
        page.update()

    global horarios
    show_loading()
    horarios = con.get_request("horarios")
    hide_loading()


    def actualizar_tabla():
        show_loading()
        tabla.controls.clear()

    # Agregar los títulos de las columnas
        tabla.controls.append(
            ft.Row(
                [
                    ft.Text("Materia", weight=ft.FontWeight.BOLD, width=100),
                    ft.Text("Maestro", weight=ft.FontWeight.BOLD, width=200),
                    ft.Text("Hora Inicio", weight=ft.FontWeight.BOLD, width=150),
                    ft.Text("Hora Final", weight=ft.FontWeight.BOLD, width=150),
                    ft.Text("Acciones", weight=ft.FontWeight.BOLD, width=150),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                    )
                    )
        for horario in horarios:
            tabla.controls.append(
                ft.Row(
                    [
                        ft.Text(horario["nombre_materia"], width=100),
                        ft.Text(f"{horario["nombre_profesor"]} {horario["apellido_profesor"]}", width=200),
                        ft.Text(horario["hora_inicio"], width=150),
                        ft.Text(horario["hora_final"], width=150),
                        ft.ElevatedButton("Eliminar", on_click=lambda e, mid=horario["id"]: eliminar_horario(mid)),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                        )
                        )
            hide_loading()
            page.update()


    def eliminar_horario(horario_id):
        show_loading()
        global horarios
        horario_seleccionado=con.get_by_id("horarios",horario_id)
        materia_a_modificar_id=horario_seleccionado["id_materia"]
        materia_a_modificar=con.get_by_id("materias",materia_a_modificar_id)
        materia_a_modificar["Asignada"]=False
        con.put_request("materias",materia_a_modificar_id,materia_a_modificar)
        con.delete_request("horarios",horario_id)
        horarios=con.get_request("horarios")
        hide_loading()
        page.snack_bar = ft.SnackBar(ft.Text("Horario eliminado correctamente"))
        page.snack_bar.open = True
        # Actualizar la tabla
        actualizar_tabla()

        
    tabla = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    containerTabla=ft.Container(
        content=ft.Column(
            controls=[tabla],  # Aquí pones la tabla
            scroll=ft.ScrollMode.AUTO,  # Habilita el desplazamiento
            alignment=ft.MainAxisAlignment.CENTER,  # Alinear los controles dentro del Column
        ),
        width=850,  # Ancho del contenedor
        height=400,  # Altura del contenedor
        padding=20
    )

    actualizar_tabla()
    return ft.Stack(
        controls=[
            ft.Column(
                controls=[
                    ft.Text("Horarios asignados", size=24, weight=ft.FontWeight.BOLD),
                    containerTabla,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            loading_indicator,
        ],
        expand=True,  # Asegura que el Stack ocupe toda la pantalla
    )


