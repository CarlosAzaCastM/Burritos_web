import flet as ft

class Menu(ft.Column):
    burritosRojoCantidad = 0
    burritosVerdeCantidad = 0
    burritosOtroCantidad = 0
    PRECIO = 15
    burritosPrecioTotal = 0

    def __init__(self):
        super().__init__()
        self.txtUser = ft.Text(value="Usuario: Carlos", size=12, color=ft.Colors.BLACK)
        self.txtTitle = ft.Text(value="Menú", size=20, color=ft.Colors.BLACK)
        
        # Elementos para Chicharrón Rojo
        self.txtRojo = ft.Text(value="Chicharrón rojo", size=20, color=ft.Colors.RED)
        self.fieldRojo = ft.TextField(width=44, height=70, bgcolor=ft.Colors.YELLOW_100, color=ft.Colors.BLACK, read_only=True)
        self.btnRojo = ft.IconButton(icon=ft.Icons.ADD, bgcolor=ft.Colors.RED, on_click=self.add_rojo)
        
        # Elementos para Chicharrón Verde
        self.txtVerde = ft.Text(value="Chicharrón verde", size=20, color=ft.Colors.GREEN)
        self.fieldVerde = ft.TextField(width=44, height=70, bgcolor=ft.Colors.YELLOW_100, color=ft.Colors.BLACK, read_only=True)
        self.btnVerde = ft.IconButton(icon=ft.Icons.ADD, bgcolor=ft.Colors.GREEN, on_click=self.add_verde)

        # Elementos para otro sabor
        self.txtOtro = ft.Text(value="Sabor del dia", size=20, color=ft.Colors.GREEN)
        self.fieldOtro = ft.TextField(width=44, height=70, bgcolor=ft.Colors.YELLOW_100, color=ft.Colors.BLACK, read_only=True)
        self.btnOtro = ft.IconButton(icon=ft.Icons.ADD, bgcolor=ft.Colors.GREEN, on_click=self.add_otro)
        
        
        # Elementos para el total
        self.txtTotal = ft.Text(value="Total costo", size=20, color=ft.Colors.BLACK)
        self.fieldTotal = ft.TextField(width=80, height=70, bgcolor=ft.Colors.YELLOW_100, color=ft.Colors.BLACK, read_only=True)
        self.btnEnviar = ft.Button("ENVIAR", bgcolor=ft.Colors.BLUE)
        
        self.controls = [
            self.txtUser,
            self.txtTitle,
            ft.Row(
                controls=[
                    self.txtRojo,
                    self.fieldRojo,
                    self.btnRojo,
                ],
                alignment=ft.MainAxisAlignment.CENTER,  
            ),
            ft.Row(
                controls=[
                    self.txtVerde,
                    self.fieldVerde,
                    self.btnVerde,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.txtOtro,
                    self.fieldOtro,
                    self.btnOtro,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.txtTotal,
                    self.fieldTotal,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            self.btnEnviar
        ]
        self.spacing = 20
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def add_rojo(self, e):
        self.burritosRojoCantidad += 1
        self.fieldRojo.value = str(self.burritosRojoCantidad)
        self.burritosPrecioTotal = (self.burritosVerdeCantidad + self.burritosRojoCantidad + self.burritosOtroCantidad) * self.PRECIO
        self.fieldTotal.value = str(self.burritosPrecioTotal)
        self.update()
    
    def add_verde(self, e):
        self.burritosVerdeCantidad += 1
        self.fieldVerde.value = str(self.burritosVerdeCantidad)
        self.burritosPrecioTotal = (self.burritosVerdeCantidad + self.burritosRojoCantidad + self.burritosOtroCantidad) * self.PRECIO
        self.fieldTotal.value = str(self.burritosPrecioTotal)
        self.update()

    def add_otro(self, e):
        self.burritosOtroCantidad += 1
        self.fieldOtro.value = str(self.burritosOtroCantidad)
        self.burritosPrecioTotal = (self.burritosVerdeCantidad + self.burritosRojoCantidad + self.burritosOtroCantidad) * self.PRECIO
        self.fieldTotal.value = str(self.burritosPrecioTotal)
        self.update()


    def click_enviar(self, e):
        pass

class InicioSesion(ft.Column):

    def __init__(self):
        super().__init__()


def main(page: ft.Page):
    page.title = "Menú de Burritos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    menu = Menu()
    page.add(menu)

ft.app(main)