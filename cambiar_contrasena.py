import flet as ft
import services.conexion as con
from services.TempFileManager import TempFileManager
from passlib.hash import sha256_crypt

# Función que crea y devuelve un cuadro de diálogo
def crear_dialogo(page: ft.Page, user):
    # Crear los campos de texto con las propiedades necesarias
    actual_pass = ft.TextField(password=True, can_reveal_password=True, label="Contraseña actual")
    new_pass = ft.TextField(password=True, can_reveal_password=True, label="Nueva contraseña")
    repeat_pass = ft.TextField(password=True, can_reveal_password=True, label="Repetir nueva contraseña")
    error_text=ft.Text(" ", color="red")
    # Función para manejar la captura de valores
    def capturar_valores(e):
        # Captura los valores y muestra un mensaje
        p1, p2, p3 = actual_pass.value, new_pass.value, repeat_pass.value
        if not p1 or not p2 or not p3:
            error_text.value = "Todos los campos son obligatorios"
            page.update()
            return
    
        if(sha256_crypt.verify(p1, user["password"])):
            if(p2==p3):
                user["password"]=p2
                id=user["id"]
                #del user["id"]
                user["password"]=sha256_crypt.encrypt(user["password"])
                con.put_request("users",id,user)
                page.snack_bar = ft.SnackBar(ft.Text(f"Contraseña modificada correctamente"))
                page.snack_bar.open = True
                dialog.open = False
            else:
                error_text.value="Las contraseñas no coinciden"
        else:
            error_text.value="No se reconoce la contraseña"

        
        page.update()
    
    # Función para cerrar el diálogo al cancelar
    def cerrar_dialogo(e):
        dialog.open = False
        page.update()

    # Cuadro de diálogo
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cambio de contraseña"),
        content=ft.Column([
            actual_pass,
            new_pass,
            repeat_pass,
            error_text,
        ], tight=True),
        actions=[
            ft.TextButton("Aceptar", on_click=capturar_valores),
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
        ],
    )
    return dialog
