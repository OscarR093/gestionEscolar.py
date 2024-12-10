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

    global usuarios
    show_loading()
    usuarios = con.search_by_field("users","active",False)
    hide_loading()


    def actualizar_tabla():
        show_loading()
        tabla.controls.clear()

    # Agregar los títulos de las columnas
        tabla.controls.append(
            ft.Row(
                [
                    ft.Text("Nombre", weight=ft.FontWeight.BOLD, width=100),
                    ft.Text("Usuario", weight=ft.FontWeight.BOLD, width=100),
                    ft.Text("E-Mail", weight=ft.FontWeight.BOLD, width=200),
                    ft.Text("Aceptar", weight=ft.FontWeight.BOLD, width=110),
                    ft.Text("Rechazar", weight=ft.FontWeight.BOLD, width=110),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                    )
                    )
        for usuario in usuarios:
            tabla.controls.append(
                ft.Row(
                    [
                        ft.Text(usuario["name"], width=100),
                        ft.Text(usuario["username"],width=100),
                        ft.Text(usuario["email"], width=200),
                        ft.ElevatedButton("Aceptar", width=110, on_click=lambda e, mid=usuario["id"]: activar_usuario(mid)),
                        ft.ElevatedButton("Rechazar", bgcolor="pink", color="black", width=110, on_click=lambda e, mid=usuario["id"]: eliminar_usuario(mid)),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                        )
                        )
            hide_loading()
            page.update()


    def eliminar_usuario(usuario_id):
        show_loading()
        global usuarios
        con.delete_request("users",usuario_id)
        usuarios=con.search_by_field("users","active",False)
        hide_loading()
        page.snack_bar = ft.SnackBar(ft.Text("Se elimino usuario rechazado"))
        page.snack_bar.open = True
        # Actualizar la tabla
        actualizar_tabla()

    def activar_usuario(usuario_id):
        global usuarios
        show_loading()
        usuario_a_activar=con.get_by_id("users",usuario_id)
        usuario_a_activar={
                    "id": "",
                    "name": usuario_a_activar["name"],
                    "username": usuario_a_activar["username"],
                    "email":usuario_a_activar["email"],
                    "password":usuario_a_activar["password"],
                    "super": False,
                    "active": True
                    }
        con.put_request("users",usuario_id,usuario_a_activar)
        usuarios=con.search_by_field("users","active",False)
        hide_loading()
        page.snack_bar = ft.SnackBar(ft.Text("Usuario Activado correctamente"))
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
                    ft.Text("Usuarios pendientes de activacion", size=24, weight=ft.FontWeight.BOLD),
                    containerTabla,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            loading_indicator,
        ],
        expand=True,  # Asegura que el Stack ocupe toda la pantalla
    )
        

