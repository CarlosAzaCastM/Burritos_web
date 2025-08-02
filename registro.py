#registro.py
import flet as ft
from db import Database

class Registro(ft.Column):
    def __init__(self, on_register_success, on_go_to_login, on_audio, db: Database):
        super().__init__()
        self.on_register_success = on_register_success
        self.on_go_to_login = on_go_to_login
        self.db = db
        
        # Configuración de colores
        self.colorFondo = "#f6efe7"
        self.colorTitulo = "#8b5e3c"
        self.colorSubtitulo = "#d18c60"
        self.verdeHoja = "#A1B58C"

        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO
        self.spacing = 20

        # Componentes UI
        self.txtTitle = ft.Text(value="Registro", size=28, weight=ft.FontWeight.BOLD, color=self.colorTitulo)
        
        # Campos del formulario
        self.fieldNombre = ft.TextField(
            label="Primer Nombre",
            width=300,
            color=ft.Colors.BLACK,
            bgcolor=self.verdeHoja,
            border_radius=40,
            label_style=ft.TextStyle(
                color=ft.Colors.BLACK,  
                size=14
            )
        )
        
        self.fieldMatricula = ft.TextField(
            label="Matrícula",
            width=300,
            color=ft.Colors.BLACK,
            bgcolor=self.verdeHoja,
            border_radius=40,
            max_length=8,
            label_style=ft.TextStyle(
                color=ft.Colors.BLACK,  
                size=14
            )
        )
        
        self.fieldPassword = ft.TextField(
            label="Contraseña",
            width=300,
            password=True,
            can_reveal_password=True,
            color=ft.Colors.BLACK,
            bgcolor=self.verdeHoja,
            border_radius=40,
            max_length=20,
            label_style=ft.TextStyle(
                color=ft.Colors.BLACK,  
                size=14
            )
        )
        
        self.fieldConfirmPassword = ft.TextField(
            label="Confirmar contraseña",
            width=300,
            password=True,
            can_reveal_password=True,
            color=ft.Colors.BLACK,
            bgcolor=self.verdeHoja,
            border_radius=40,
            max_length=20,
            label_style=ft.TextStyle(
                color=ft.Colors.BLACK,  
                size=14
            )
        )

        self.fieldAula = ft.Dropdown(
            label="Aula",
            width=300,
            label_style=ft.TextStyle(
                color=ft.Colors.BLACK,  
                size=14
            ),
            text_style=ft.TextStyle(
                color=ft.Colors.BLACK,  
                size=14
            ),
            options=[
                ft.dropdown.Option("aula1"),
                ft.dropdown.Option("aula2"),
                ft.dropdown.Option("aula3"),
                ft.dropdown.Option("aula4"),
                ft.dropdown.Option("aula5"),
                ft.dropdown.Option("aula6"),
                ft.dropdown.Option("aula7"),
            ]
        )
        
        self.fieldSalon = ft.TextField(
            label="Salón",
            width=300,
            color=ft.Colors.BLACK,
            bgcolor=self.verdeHoja,
            border_radius=40,
            label_style=ft.TextStyle(
                color=ft.Colors.BLACK,  
                size=14
            )
        )
        
        self.fieldAulaIngles = ft.Dropdown(
            label="Aula de Inglés",
            width=300,
            label_style=ft.TextStyle(
                color=ft.Colors.BLACK,  
                size=14
            ),
            text_style=ft.TextStyle(
                color=ft.Colors.BLACK,  
                size=14
            ),
            options=[
                ft.dropdown.Option("aula1"),
                ft.dropdown.Option("aula2"),
                ft.dropdown.Option("aula3"),
                ft.dropdown.Option("aula4"),
                ft.dropdown.Option("aula5"),
                ft.dropdown.Option("aula6"),
                ft.dropdown.Option("aula7"),
            ]
        )
        
        self.fieldSalonIngles = ft.TextField(
            label="Salón de Inglés",
            width=300,
            color=ft.Colors.BLACK,
            bgcolor=self.verdeHoja,
            border_radius=40,
            label_style=ft.TextStyle(
                color=ft.Colors.BLACK,  
                size=14
            )
        )
        
        # Botones
        self.btnRegister = ft.ElevatedButton(
            "Registrarse",
            on_click=self.register,
            bgcolor=self.colorSubtitulo,
            color=ft.Colors.WHITE,
            width=300,
        )
        
        self.btnLogin = ft.TextButton(
            "¿Ya tienes cuenta? Inicia sesión",
            on_click=self.go_to_login,
        )
        
        # Mensaje de error
        self.error_message = ft.Text(color=ft.Colors.RED, visible=False)

        self.speakerIcon = ft.IconButton(icon=ft.Icons.VOLUME_UP, icon_color=ft.Colors.BLACK, on_click=on_audio)

        def create_centered_row(control):
            return ft.Row(
                controls=[control],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                 # Asegura que use el ancho completo
            )
        
        # Configuración de controles
        self.controls = [
            create_centered_row(self.speakerIcon),
            create_centered_row(self.txtTitle),
            create_centered_row(self.fieldNombre),
            create_centered_row(self.fieldMatricula),
            create_centered_row(self.fieldPassword),
            create_centered_row(self.fieldConfirmPassword),
            create_centered_row(self.fieldAula),
            create_centered_row(self.fieldSalon),
            create_centered_row(self.fieldAulaIngles),
            create_centered_row(self.fieldSalonIngles),
            create_centered_row(self.error_message),
            create_centered_row(self.btnRegister),
            create_centered_row(self.btnLogin)
        ]
        

    def register(self, e):
        """Lógica de registro con base de datos"""
        self.db.connect()
        # Validar campos
        if (not self.fieldNombre.value or not self.fieldMatricula.value or 
            not self.fieldPassword.value or not self.fieldConfirmPassword.value or
            not self.fieldAula.value or not self.fieldSalon.value or
            not self.fieldAulaIngles.value or not self.fieldSalonIngles.value):
            self.error_message.value = "Todos los campos son obligatorios"
            self.error_message.visible = True
            self.update()
            return
            
        if self.fieldPassword.value != self.fieldConfirmPassword.value:
            self.error_message.value = "Las contraseñas no coinciden"
            self.error_message.visible = True
            self.update()
            return
        
        # Verificar si la matrícula ya existe
        if self.db.obtener_usuario_por_matricula(self.fieldMatricula.value):
            self.error_message.value = "La matrícula ya está registrada"
            self.error_message.visible = True
            self.update()
            return
        
        try:
            # Registrar el usuario en la base de datos
            self.db.crear_usuario(
                nombre_usu=self.fieldNombre.value,
                matricula_usu=self.fieldMatricula.value,
                contraseña_usu=self.fieldPassword.value,
                aula_usu=self.fieldAula.value,
                salon_usu=self.fieldSalon.value,
                aulaIngles_usu=self.fieldAulaIngles.value,
                salonIngles_usu=self.fieldSalonIngles.value
            )
            snackBar = ft.SnackBar(ft.Text("Registrado con exito", color=ft.Colors.WHITE),bgcolor=ft.Colors.GREEN)
            self.page.open(snackBar)
            self.page.update()
            
            # Éxito, volver a inicio de sesión
            self.on_register_success(e)
        except Exception as ex:
            self.error_message.value = f"Error al registrar: {str(ex)}"
            self.error_message.visible = True
            self.update()

    def go_to_login(self, e):
        """Navega al formulario de inicio de sesión"""
        self.on_go_to_login(e)

    def will_unmount(self):
        """Se llama cuando la vista va a ser eliminada"""
        self.db.close()