import flet as ft
from db import Database

class Actulizar(ft.Column):
    def __init__(self, datos_usuario, on_go_home, on_audio,db: Database):
        super().__init__(expand=True) 
        
        # Configuración de colores
        self.colorFondo = "#f6efe7"
        self.colorTitulo = "#8b5e3c"
        self.colorSubtitulo = "#d18c60"
        self.colorExtra = "#a1b58c"
        self.verdeHoja = "#A1B58C"
        self.datos_usu = datos_usuario

        self.db = db

        self.snack_bar = ft.SnackBar(
            content=ft.Text("¡Datos actualizados correctamente!", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN,
        )
        
        # Elementos de la interfaz
        self.txtActulizar = ft.Text(
            value="Actualizar Información", 
            color=self.colorTitulo, 
            weight=ft.FontWeight.BOLD, 
            size=30
        )

        self.btnHome = ft.IconButton(
            icon=ft.Icons.HOME,
            icon_color=ft.Colors.BLACK,
            on_click= lambda e: on_go_home(e)
        )

        # Campos de actualización
        self.txtAula = ft.Text(value="Aula:", color=self.colorSubtitulo, size=20)
        self.dropdownAula = ft.Dropdown(
            options=[ft.dropdown.Option(aula) for aula in ["aula1", "aula2", "aula3","aula4", "aula5", "aula6", "aula7"]],
            value=self.datos_usu['aula_usu'],
            color=ft.Colors.BLACK,
            width=200,
            disabled=True,
            bgcolor=self.colorExtra,
            text_style=ft.TextStyle(
                color=ft.Colors.BLACK,  
                size=14
            ),
            border_radius=20
        )
        self.btnEditAula = ft.IconButton(
            icon=ft.Icons.EDIT,
            icon_color=ft.Colors.BLACK,
            on_click=lambda e: self.toggle_dropdown(e, self.dropdownAula, self.btnEditAula)
        )
                
        
        self.txtSalon = ft.Text(value="Salón:", color=self.colorSubtitulo, size=20)
        self.fieldSalon = ft.TextField(
            value=self.datos_usu['salon_usu'],
            width=200,
            height=40,
            bgcolor=self.colorExtra,
            border_radius=20,
            border_color=self.colorExtra,
            read_only=True,
            color= ft.Colors.BLACK
        )
        self.btnEditSalon = ft.IconButton(
            icon=ft.Icons.EDIT,
            icon_color=ft.Colors.BLACK,
            on_click = lambda e: self.toggle_edit(e, self.fieldSalon, self.btnEditSalon)
        )
        
        self.txtAulaIngles = ft.Text(value="Aula Inglés:", color=self.colorSubtitulo, size=20)
        self.dropdownAulaIngles = ft.Dropdown(
            options=[ft.dropdown.Option(aulaIngles) for aulaIngles in ["aula1", "aula2", "aula3","aula4", "aula5", "aula6", "aula7"]],
            value=self.datos_usu['aulaIngles_usu'],
            color=ft.Colors.BLACK,
            width=200,
            disabled=True,
            bgcolor=self.colorExtra,
            text_style=ft.TextStyle(
                color=ft.Colors.BLACK,  
                size=14
            ),
            border_radius=20
        )
        self.btnEditAulaIngles = ft.IconButton(
            icon=ft.Icons.EDIT,
            icon_color=ft.Colors.BLACK,
            on_click=lambda e: self.toggle_dropdown(e, self.dropdownAulaIngles, self.btnEditAulaIngles)
        )

        self.txtSalonIngles = ft.Text(value="Salón Inglés:", color=self.colorSubtitulo, size=20)
        self.fieldSalonIngles = ft.TextField(
            value=self.datos_usu['salonIngles_usu'],
            width=200,
            height=40,
            bgcolor=self.colorExtra,
            border_radius=20,
            border_color=self.colorExtra,
            read_only=True,
            color= ft.Colors.BLACK
        )
        self.btnEditSalonIngles = ft.IconButton(
            icon=ft.Icons.EDIT,
            icon_color=ft.Colors.BLACK,
            on_click = lambda e: self.toggle_edit(e, self.fieldSalonIngles, self.btnEditSalonIngles)
        )

        # Botón de guardar
        self.btnGuardar = ft.ElevatedButton(
            text="GUARDAR CAMBIOS",
            bgcolor=self.colorExtra,
            color=ft.Colors.BLACK,
            on_click= self.boton_guardar
        
        )

        self.speakerIcon = ft.IconButton(icon=ft.Icons.VOLUME_UP, icon_color=ft.Colors.BLACK, on_click=on_audio)

        # Organización de los controles
        self.controls = [
            self.speakerIcon,
            ft.Row(
                controls=[self.txtActulizar, self.btnHome],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            self.txtAula, 
            ft.Row(
                controls=[self.dropdownAula, self.btnEditAula],
                alignment=ft.MainAxisAlignment.CENTER
            ),  
            self.txtSalon,
            ft.Row(
                controls=[self.fieldSalon, self.btnEditSalon],
                alignment=ft.MainAxisAlignment.CENTER
            ), 
            self.txtAulaIngles,
            ft.Row(
                controls=[self.dropdownAulaIngles, self.btnEditAulaIngles],
                alignment=ft.MainAxisAlignment.CENTER
            ),   
            self.txtSalonIngles,
            ft.Row(
                controls=[self.fieldSalonIngles, self.btnEditSalonIngles],
                alignment=ft.MainAxisAlignment.CENTER
            ),
           
            self.btnGuardar
        ]
        
        
        # Configuración adicional del contenedor
        self.spacing = 10
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.bgcolor = self.colorFondo

    def toggle_edit(self, e, field, btn):
        """Alterna el modo de edición de un campo y cambia el icono del botón"""
        field.read_only = not field.read_only
        btn.icon = ft.Icons.CHECK if not field.read_only else ft.Icons.EDIT
        self.update()
    
    def toggle_dropdown(self, e, dropdown, btn):
        dropdown.disabled = not dropdown.disabled
        btn.icon = ft.Icons.CHECK if not dropdown.disabled else ft.Icons.EDIT
        self.update()

    def boton_guardar(self, e):
        try:
            # Actualizar la base de datos
            updated = self.db.actualizar_usuario(
                aula_usu=self.dropdownAula.value,
                salon_usu=self.fieldSalon.value,
                aulaIngles_usu=self.dropdownAulaIngles.value,
                salonIngles_usu=self.fieldSalonIngles.value,
                matricula_usu=self.datos_usu['matricula_usu']
            )

            snackBar = ft.SnackBar(ft.Text("Usuario actulizado", color=ft.Colors.WHITE),bgcolor=ft.Colors.GREEN)
            self.page.open(snackBar)
            self.page.update()
            
            if updated:
                
                # Actualizar los datos locales (usuario_data)
                self.datos_usu.update({
                    'aula_usu': self.dropdownAula.value,
                    'salon_usu': self.fieldSalon.value,
                    'aulaIngles_usu': self.dropdownAulaIngles.value,
                    'salonIngles_usu': self.fieldSalonIngles.value,
                })
                
                
                
            else:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("No se encontró el usuario para actualizar.", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED,
                )
                self.page.snack_bar.open = True
        except Exception as e:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error al actualizar: {str(e)}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED,
            )
            self.page.snack_bar.open = True
        finally:
            self.page.update()

    


