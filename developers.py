import flet as ft

class Developers(ft.Column):

    def __init__(self, on_go_home):
        super().__init__(expand=True)

        #Paleta de colores
        self.colorFondo = "#f6efe7"
        self.colorTitulo = "#8b5e3c"
        self.colorSubtitulo = "#d18c60"
        self.colorExtra = "#a1b58c"

        #link: https://drive.google.com/file/d/1NemNP1CUJJW12jcX57OBbb7dFk5JVVQG/view?usp=sharing

        self.__btnHome = ft.IconButton(icon=ft.Icons.HOME, icon_color=ft.Colors.BLACK, on_click=on_go_home)

        self.drive_image_id = "1NemNP1CUJJW12jcX57OBbb7dFk5JVVQG"  # Reemplaza con tu ID real
        self.drive_url = f"https://lh3.googleusercontent.com/d/{self.drive_image_id}=s200?authuser=0"

        self.__img_equipo = ft.Image(
        src=self.drive_url,
        width=400,  
        height=300,  
        fit=ft.ImageFit.CONTAIN, 
        repeat=ft.ImageRepeat.NO_REPEAT,
        border_radius=ft.border_radius.all(10),
        tooltip="Imagen desde Google Drive",
        error_content=ft.Text("Error al cargar la imagen")  # Mensaje si falla
        )

        self.controls=[
            self.__btnHome,
            ft.Text(value="DESAROLLADORES DEL PROYECTO", size=20, color=self.colorTitulo),
            self.__img_equipo,
            ft.Text(value="240508 - Adolfo Yair Salas Hernandez", size=12, color=self.colorSubtitulo),
            ft.Text(value="240325 - Carlos Azael Castañeda Muñoz", size=12, color=self.colorSubtitulo),
            ft.Text(value="230193 - Luis Fernando Romo Peralta", size=12, color=self.colorSubtitulo),
            ft.Text(value="240299 - Oscar Fernando Santillan Castañeda", size=12, color=self.colorSubtitulo)
        ]

        self.spacing = 20
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment=ft.MainAxisAlignment.CENTER,  