import flet as ft

class CortePedidoDetalles(ft.Column):
    def __init__(self, on_go_home, titulo):
        super().__init__(expand=True) 

        #Paleta de colores
        self.colorFondo = "#f6efe7"
        self.colorTitulo = "#8b5e3c"
        self.colorSubtitulo = "#d18c60"
        self.colorExtra = "#a1b58c"

        self.titulo = titulo
        self.txtTitulo = ft.Text(value=self.titulo, size=28, weight=ft.FontWeight.BOLD, color=self.colorTitulo)
        self.btnHome = ft.IconButton(icon=ft.Icons.HOME, icon_color=ft.Colors.BLACK, on_click=lambda e:  on_go_home(e))

        self.controls = [
            self.txtTitulo,
            ft.Row(controls=[self.btnHome],alignment=ft.MainAxisAlignment.END)
        ]

        self.spacing = 20
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment=ft.MainAxisAlignment.CENTER, 
