import flet as ft
import services.conexion as con

def main(page: ft.Page):
    page.clean()
    page.title = "Registro de Usuarios"
    page.theme_mode = "dark"  # Cambiar a "dark" para modo oscuro
    page.padding = 20
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

    # Función para manejar el registro
    def registrar_usuario(e):
        # Validar campos
        if not name_input.value or not username_input.value or not email_input.value or not password_input.value or not confirm_password_input.value:
            error_message.value = "Todos los campos son obligatorios."
            error_message.visible = True
            page.update()
            return

        if " " in username_input.value:
            error_message.value = "El nombre de usuario no puede contener espacios."
            error_message.visible = True
            page.update()
            return

        if "@" not in email_input.value or "." not in email_input.value:
            error_message.value = "El correo electrónico no es válido."
            error_message.visible = True
            page.update()
            return

        if password_input.value != confirm_password_input.value:
            error_message.value = "Las contraseñas no coinciden."
            error_message.visible = True
            page.update()
            return

        show_loading()
        # Preparar datos para enviar
        nuevo_usuario = {
            "id": "",
            "name": name_input.value,
            "username": username_input.value,
            "email": email_input.value,
            "password": password_input.value,
            "super": False,
            "active": False,
        }

        try:
            # Conexión al módulo existente
            con.post_request("users", nuevo_usuario)
            success_message.value = "Usuario registrado exitosamente."
            success_message.visible = True
            error_message.visible = False
            # Limpiar campos
            name_input.value = ""
            username_input.value = ""
            email_input.value = ""
            password_input.value = ""
            confirm_password_input.value = ""
        except Exception as ex:
            error_message.value = f"Error al registrar usuario: {str(ex)}"
            error_message.visible = True
            success_message.visible = False
        hide_loading()
        page.update()

    # Entradas del formulario
    name_input = ft.TextField(label="Nombre completo", width=400)
    username_input = ft.TextField(label="Usuario", width=400)
    email_input = ft.TextField(label="Correo Electrónico", width=400)
    password_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=400)
    confirm_password_input = ft.TextField(label="Confirmar Contraseña", password=True, can_reveal_password=True, width=400)

    # Mensajes de error y éxito
    error_message = ft.Text(value="", color="red", visible=False)
    success_message = ft.Text(value="", color="green", visible=False)

    # Botón de registro
    register_button = ft.ElevatedButton(text="Registrar", on_click=registrar_usuario, width=200)

    # Agregar elementos a la página
    return ft.Stack(
        controls=[
            ft.Column(
                controls=[
                    ft.Text("Formulario de Registro de Usuarios", size=24, weight="bold"),
                    name_input,
                    username_input,
                    email_input,
                    password_input,
                    confirm_password_input,
                    register_button,
                    error_message,
                    success_message,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            loading_indicator,
        ],
        expand=True,  # Asegura que el Stack ocupe toda la pantalla
    )
