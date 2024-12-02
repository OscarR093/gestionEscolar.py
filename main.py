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
    
    
    def route_change(route):
        page.views.clear()
        materias_no_asignadas = con.search_by_field("materias","Asignada",False)
        if materias_no_asignadas != None:
            TextoMaterias=ft.Text(f"Hay {len(materias_no_asignadas)} materias sin asignar")
        else:
            TextoMaterias=ft.Text(f"Todas las materias se han asignado")
        
        if page.route == "/":
            # Menú principal
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
            # Gestión de Maestros
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
            # Gestión de Materias
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
            
        else:
            # Página no encontrada
            page.views.append(
                ft.View(
                    "/404",
                    controls=[
                        ft.Text("Página no encontrada", size=24, color="red"),
                        ft.ElevatedButton("Volver al menú principal", on_click=lambda e: page.go("/")),
                    ],
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
