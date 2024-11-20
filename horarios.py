import flet as ft
import documents


def main(page: ft.Page):
    global horarios
    horarios = documents.cargar_datos("horarios.json")


    def actualizar_tabla():
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
            page.update()


    def eliminar_horario(horario_id):
        global horarios
        materias = documents.cargar_datos("materias.json")

        # Encontrar el horario a eliminar
        horario_a_eliminar = None
        
        for horario in horarios:
            if horario["id"] == horario_id:
                horario_a_eliminar = horario
                break

        if horario_a_eliminar:
            # Encontrar la materia asignada en el horario
            materia_id = horario_a_eliminar["id_materia"]
            for materia in materias:
                if materia["id"] == materia_id:
                    # Cambiar el estado de la materia a "Asignada: False"
                    materia["Asignada"] = False
                    break

        # Eliminar el horario
        horarios = [h for h in horarios if h["id"] != horario_id]

        # Guardar los cambios en los archivos JSON
        documents.guardar_datos("horarios.json", horarios)
        documents.guardar_datos("materias.json", materias)

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

    return ft.Column(
    controls=[
        ft.Text("Horarios Asignados Actualmente", size=24, weight=ft.FontWeight.BOLD),
        containerTabla,
    ],
    alignment=ft.MainAxisAlignment.CENTER,  # Alinea verticalmente
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinea horizontalmente
)

