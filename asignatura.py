import flet as ft
import services.conexion as con


def main(page: ft.Page):
    # Cargar los datos de los maestros y materias
    global materias
    profesores = con.get_request("maestros")
    materias = con.get_request("materias")
    
    # Variables para almacenar las selecciones
    global profesor_seleccionado 
    global materia_seleccionada 

    materia_seleccionada=None
    profesor_seleccionado=None

    lista_maestros = ft.Column([], scroll=ft.ScrollMode.AUTO, width=400)
    lista_materias = ft.Column([], scroll=ft.ScrollMode.AUTO, width=400)


    # Función para actualizar las listas
    def actualizar_listas():
        global materias  # Asegúrate de actualizar la variable global
        materias = con.get_request("materias")  # Recupera los datos más recientes desde el servidor
    
        # Crear las filas de las listas de maestros
        lista_maestros.controls.clear()
        for profesor in profesores:
            lista_maestros.controls.append(
            ft.Row(
                [
                    ft.Text(profesor["nombre"]),
                    ft.Text(profesor["apellido"]),
                    ft.ElevatedButton("Seleccionar", on_click=lambda e, p=profesor: seleccionar_maestro(p)),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )

        # Crear las filas de las listas de materias
        lista_materias.controls.clear()
        for materia in materias:
            if not materia.get("Asignada", False):  # Mostrar solo materias no asignadas
                lista_materias.controls.append(
                ft.Row(
                    [
                        ft.Text(materia["nombre"]),
                        ft.ElevatedButton("Seleccionar", on_click=lambda e, m=materia: seleccionar_materia(m)),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )
        # Actualiza la página solo al final
        page.update()


    def asignar_materia_seleccionada(materia_id):
        global materias  # Asegúrate de trabajar con la variable global
        for materia in materias:
            if materia["id"] == materia_id:  
                materia["Asignada"] = True
                con.put_request("materias", materia_id, materia)
                break  # Salir del bucle una vez encontrada
        materias = con.get_request("materias")
        actualizar_listas()




    # Función para seleccionar un maestro
    def seleccionar_maestro(profesor):
        global profesor_seleccionado
        profesor_seleccionado = profesor
        texto_maestro.value = f"Maestro seleccionado: {profesor['nombre']} {profesor['apellido']}"
        page.update()

    # Función para seleccionar una materia
    def seleccionar_materia(materia):
        global materia_seleccionada
        materia_seleccionada = materia
        texto_materia.value = f"Materia seleccionada: {materia['nombre']}"
        page.update()

    # Función para asignar el maestro y la materia
    def asignar_horario(e):
        global profesor_seleccionado, materia_seleccionada
        if profesor_seleccionado is None or materia_seleccionada is None:
            page.snack_bar = ft.SnackBar(ft.Text("¡Debe seleccionar un maestro y una materia!"))
            page.snack_bar.open = True
            page.update()
            return
    
    # Crear el horario
        horario = {
            "id": "",
            "id_profesor": profesor_seleccionado["id"],
            "id_materia": materia_seleccionada["id"],
            "nombre_profesor": profesor_seleccionado["nombre"],
            "apellido_profesor": profesor_seleccionado["apellido"],
            "nombre_materia": materia_seleccionada["nombre"],
            "hora_inicio": materia_seleccionada["HoraInicio"],
            "hora_final": materia_seleccionada["HoraFinal"],
            }
        # Asignar la materia y actualizar las listas
        asignar_materia_seleccionada(materia_seleccionada["id"])
        texto_maestro.value = "Maestro seleccionado: Ninguno"
        texto_materia.value = "Materia seleccionada: Ninguna"
        materia_seleccionada = None
        profesor_seleccionado = None

        # Guardar el horario
        con.post_request("horarios", horario)

        page.snack_bar = ft.SnackBar(ft.Text("Materia Asignada Correctamente"))
        page.snack_bar.open = True
        page.update()


    # Controles de la interfaz
    texto_maestro = ft.Text("Maestro seleccionado: Ninguno", size=16, weight=ft.FontWeight.BOLD)
    texto_materia = ft.Text("Materia seleccionada: Ninguna", size=16, weight=ft.FontWeight.BOLD)
    
    boton_asignar = ft.ElevatedButton("Asignar", on_click=asignar_horario)

    # Listas de maestros y materias
    

    containerListas = ft.Container(
    content=ft.Row(
        controls=[
            ft.Column(
                controls=[lista_maestros],  # Aquí pones la lista de maestros
                scroll=ft.ScrollMode.AUTO,  # Habilita el desplazamiento
                alignment=ft.MainAxisAlignment.START,  # Alinea el contenido de la columna
                width=300,  # Ancho de la columna
            ),
            ft.Column(
                controls=[lista_materias],  # Aquí pones la lista de materias
                scroll=ft.ScrollMode.AUTO,  # Habilita el desplazamiento
                alignment=ft.MainAxisAlignment.START,  # Alinea el contenido de la columna
                width=300,  # Ancho de la columna
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Alinea las columnas al centro del contenedor
        spacing=20,  # Espaciado entre las columnas
    ),
    width=700,  # Ancho total del contenedor
    height=400,  # Altura del contenedor
    alignment=ft.alignment.center,  # Alinea el contenedor en el centro
)

    # Crear la página
    

    # Actualizar las listas
    actualizar_listas()

# Exportar para ser utilizado en el `main.py`
    return ft.Column(
        controls=[
                texto_maestro,
                texto_materia,
                containerListas,
                boton_asignar,
            ],
    alignment=ft.MainAxisAlignment.CENTER,  # Alinea verticalmente
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinea horizontalmente
)