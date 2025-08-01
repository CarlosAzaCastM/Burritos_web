import flet as ft

class Audio(ft.Column):

    def __init__(self, on_go_home, on_go_sesion, preInicio):
        super().__init__(expand=True)

        self.preInicio = preInicio

        self.on_go_home = on_go_home
        self.on_go_sesion = on_go_sesion

        self.__btnHome = ft.IconButton(icon=ft.Icons.HOME, icon_color=ft.Colors.BLACK, on_click=self.tipoDeRegreso)

        self.speakerIcon = ft.IconButton(icon=ft.Icons.VOLUME_UP, icon_color=ft.Colors.BLACK, icon_size=100)
      
        self.controls=[
            self.__btnHome,
            self.speakerIcon,
            
        ]

        self.spacing = 20
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment=ft.MainAxisAlignment.CENTER,  
    
   
    def tipoDeRegreso(self, e):
        if self.preInicio:
            self.on_go_sesion(e)
        else:
            self.on_go_home(e)