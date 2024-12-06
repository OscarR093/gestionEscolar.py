import flet as ft
import appMaestros
import appMaterias
import asignatura
import services.conexion as con
import horarios

def main(page: ft.Page):
    page.title = "Sistema de Gestión"
    page.window.width = 900
    page.window.height = 600
    page.window.resizable = False

    global is_authenticated

    def validate_credentials(username, password):
        """Lógica de validación de credenciales"""
        return username == "admin" and password == "1234"

    def login_screen(page: ft.Page):
        """Pantalla de inicio de sesión"""
        username_field = ft.TextField(label="Usuario", autofocus=True, width=300)
        password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
        error_text = ft.Text("", color="red", visible=False)

        def handle_login(e):
            nonlocal username_field, password_field, error_text
            username = username_field.value
            password = password_field.value
            if validate_credentials(username, password):
                global is_authenticated
                is_authenticated = True
                page.views.clear()
                page.go("/")  # Ir al menú principal
            else:
                error_text.value = "Credenciales incorrectas. Inténtelo de nuevo."
                error_text.visible = True
                page.update()

        return ft.Stack(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("Iniciar Sesión", size=30, weight=ft.FontWeight.BOLD),
                        username_field,
                        password_field,
                        error_text,
                        ft.ElevatedButton("Ingresar", on_click=handle_login, width=100, bgcolor="pink", color="black"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                loading_indicator,
            ],
            expand=True,
        )

    # Indicador de carga global
    loading_indicator = ft.Container(
    content=ft.Column(
        controls=[
            ft.ProgressRing(),
            ft.Text("Conectando", visible=True, color="White"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    ),
    alignment=ft.alignment.center,
    visible=False,
    expand=True,)


    # Contenedor principal
    main_view = ft.Stack(
        expand=True,
        controls=[loading_indicator],
    )

    def show_loading():
        loading_indicator.visible = True
        page.update()

    def hide_loading():
        loading_indicator.visible = False
        page.update()

    def route_change(route):
        show_loading()
        page.views.clear()

        # Aquí se cargan los datos de la base de datos
        materias_no_asignadas = con.search_by_field("materias", "Asignada", False)
        if materias_no_asignadas is not None:
            TextoMaterias = ft.Text(f"Hay {len(materias_no_asignadas)} materias sin asignar")
        else:
            TextoMaterias = ft.Text(f"Todas las materias se han asignado")
        
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    controls=[
                        ft.Text("Menú Principal", size=30, weight=ft.FontWeight.BOLD),
                        TextoMaterias,
                        ft.ElevatedButton("Ir a Gestión de Maestros", on_click=lambda e: page.go("/maestros")),
                        ft.ElevatedButton("Ir a Gestión de Materias", on_click=lambda e: page.go("/materias")),
                        ft.ElevatedButton("Ir a Asignaturas", on_click=lambda e: page.go("/asignatura")),
                        ft.ElevatedButton("Ver horarios asignados", on_click=lambda e: page.go("/horarios")),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        elif page.route == "/maestros":
            page.views.append(
                ft.View(
                    "/maestros",
                    controls=[
                        appMaestros.main(page),
                        ft.ElevatedButton("Volver al menú principal", on_click=lambda e: page.go("/")),
                    ]
                )
            )
        elif page.route == "/materias":
            page.views.append(
                ft.View(
                    "/materias",
                    controls=[
                        appMaterias.main(page),
                        ft.ElevatedButton("Volver al menú principal", on_click=lambda e: page.go("/")),
                    ]
                )
            )
        elif page.route == "/asignatura":
            page.views.append(
                ft.View(
                    "/asignatura",
                    controls=[
                        asignatura.main(page),
                        ft.ElevatedButton("Volver al menú principal", on_click=lambda e: page.go("/")),
                    ]
                )
            )
        elif page.route == "/horarios":
            page.views.append(
                ft.View(
                    "/horarios",
                    controls=[
                        horarios.main(page),
                        ft.ElevatedButton("Volver al menú principal", on_click=lambda e: page.go("/")),
                    ]
                )
            )
        elif page.route == "/login":
            page.views.append(
                ft.View(
                    "/login",
                    controls=[
                        login_screen(page),
                    ], vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        else:
            page.views.append(
                ft.View(
                    "/404",
                    controls=[
                        ft.Text("Página no encontrada", size=24, color="red"),
                        ft.ElevatedButton("Volver al menú principal", on_click=lambda e: page.go("/")),
                    ],
                )
            )
        
        hide_loading()
        page.update()

    page.on_route_change = route_change

    # Añade la vista principal al stack
    page.add(main_view)
    page.go("/login")

ft.app(target=main)