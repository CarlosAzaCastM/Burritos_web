import pywhatkit
import flet as ft

# Envía un mensaje a un número a una hora específica (24h)
def main(page: ft.Page):
    page.title = "Enviar"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    enviar = ft.ElevatedButton("Enviar",on_click=lambda e : pywhatkit.sendwhatmsg_instantly("+524495693298", "Mensaje enviado ahora"))
    
    page.update()

    

    page.add(enviar)

ft.app(main)




