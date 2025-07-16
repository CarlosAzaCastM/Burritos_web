import flet as ft

class MenuElecciones(ft.Column):
    def __init__(self, on_pedir_burritos, on_actulizar, on_go_login, on_corte, on_pedido, on_detalles, on_stock,matricula_usu):
        super().__init__()
        
        self.colorFondo = "#f6efe7"
        self.colorTitulo = "#8b5e3c"
        self.colorSubtitulo = "#d18c60"
        self.colorExtra = "#a1b58c"
        self.verdeHoja = "#A1B58C"
        self.matricula_usu = matricula_usu

        self.espacioArriba = ft.Container(width=10, height=20)

        self.img_control = ft.Image(
            src="https://lh3.googleusercontent.com/d/1D3EKaKUhD0dupYd0dbuM5nEjAlD_fSYU=s200?authuser=0",
            width=300,
            height=200,
            fit=ft.ImageFit.CONTAIN,
            border_radius=ft.border_radius.all(10),
            error_content=ft.Text("Error al cargar la imagen")
        )

        self.btnLogout = ft.IconButton(
            icon=ft.Icons.LOGOUT,
            icon_color=ft.Colors.BLACK,
            on_click=lambda e: on_go_login(e)
        )

        self.btnPedirBurritos = ft.ElevatedButton(
            "Pedir burritos", 
            width=160, 
            height=35, 
            bgcolor=self.verdeHoja, 
            color=ft.Colors.BLACK,
            on_click=on_pedir_burritos  # Aquí conectamos el callback
        )
        
        self.btnActulizar = ft.ElevatedButton(
            "Actualizar Usuario", 
            width=160, 
            height=35, 
            bgcolor=self.verdeHoja, 
            color=ft.Colors.BLACK,
            on_click=on_actulizar
        )

        self.btnCorte = ft.ElevatedButton(
            "Corte", 
            width=70, 
            height=30, 
            bgcolor=self.colorSubtitulo, 
            color=ft.Colors.BLACK,
            on_click=on_corte
        )
        
        self.btnPedido = ft.ElevatedButton(
            "Pedido", 
            width=70, 
            height=30, 
            bgcolor=self.colorSubtitulo, 
            color=ft.Colors.BLACK,
            on_click=on_pedido
        )
        
        self.btnDetallePedido = ft.ElevatedButton(
            "Detalles Pedido", 
            width=70, 
            height=50, 
            bgcolor=self.colorSubtitulo, 
            color=ft.Colors.BLACK,
            on_click=on_detalles
        )

        self.btnStockBurritos = ft.ElevatedButton(
            "Stock", 
            width=70, 
            height=30, 
            bgcolor=self.colorSubtitulo, 
            color=ft.Colors.BLACK,
            on_click=on_stock
        )

        
        base_controls = [
            self.espacioArriba,
            self.btnLogout,
            self.img_control,          
            self.btnPedirBurritos,
            self.btnActulizar
        ]
        
        if self.matricula_usu == "240325" or self.matricula_usu == "230193":  
            admin_buttons = ft.Row(
                controls=[
                    self.btnCorte,
                    self.btnPedido,
                    self.btnDetallePedido,
                    self.btnStockBurritos
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
            base_controls.append(admin_buttons)

        self.controls = base_controls
        
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 40
        self.expand = True

    
    
   