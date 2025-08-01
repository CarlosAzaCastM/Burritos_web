# inicio_sesion.py
import flet as ft
from db import Database


class InicioSesion(ft.Column):
    def __init__(self, on_login_success, on_go_to_register, on_audio,db: Database):
        super().__init__()
        self.db = db
        
        # Configuración de colores
        self.colorFondo = "#f6efe7"
        self.colorTitulo = "#8b5e3c"
        self.colorSubtitulo = "#d18c60"
        self.colorExtra = "#a1b58c"
        self.verdeHoja = "#A1B58C"

        self.on_login_success = on_login_success
        self.on_go_to_register = on_go_to_register

        # Componentes UI
        self.espacioArriba = ft.Container(width=10, height=20)
        self.img_control = ft.Image(
            src="https://lh3.googleusercontent.com/d/1D3EKaKUhD0dupYd0dbuM5nEjAlD_fSYU=s200?authuser=0",
            width=300,
            height=200,
            fit=ft.ImageFit.CONTAIN,
            border_radius=ft.border_radius.all(10),
            error_content=ft.Text("Error al cargar la imagen")
        )
        
        # Campos de formulario
        self.txtTitle = ft.Text(value="Inicio de Sesión", size=28, weight=ft.FontWeight.BOLD, color=self.colorTitulo)
        self.txtMatricula = ft.Text(value="Matrícula", size=13, color=self.colorTitulo)
        self.fieldMatricula = ft.TextField(
            label="Matrícula",
            width=200,
            color=ft.Colors.BLACK,
            bgcolor=self.verdeHoja,
            border_radius=40,
            max_length=8  # Porque matricula es VARCHAR(8)
        )
        
        self.txtPassword = ft.Text(value="Contraseña", size=13, color=self.colorTitulo)
        self.fieldPassword = ft.TextField(
            label="Contraseña",
            password=True,
            width=200,
            color=ft.Colors.BLACK,
            bgcolor=self.verdeHoja,
            border_radius=40,
            max_length=20  # Porque contraseña es VARCHAR(20)
        )
        
        # Botones
        self.btnLogin = ft.ElevatedButton(
            "Iniciar Sesión",
            on_click=self.login,
            bgcolor=self.colorSubtitulo,
            color=ft.Colors.WHITE,
            width=200
        )
        
        self.btnRegister = ft.TextButton(
            "¿No tienes cuenta? Regístrate",
            on_click=self.go_to_register,
        )
        
        # Mensaje de error
        self.error_message = ft.Text(color=ft.Colors.RED, visible=False)

        self.speakerIcon = ft.IconButton(icon=ft.Icons.VOLUME_UP, icon_color=ft.Colors.BLACK, on_click=on_audio)
        
        # Configuración de controles
        self.controls = [
            self.speakerIcon,
            self.espacioArriba,
            self.img_control,
            self.txtTitle,
            self.txtMatricula,
            self.fieldMatricula,
            self.txtPassword,
            self.fieldPassword,
            self.error_message,
            self.btnLogin,
            self.btnRegister
        ]
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 15
    
    
    def go_to_register(self, e):
        """Navega al formulario de registro"""
        self.on_go_to_register(e)

    
    def login(self, e):
        """Lógica de inicio de sesión con validación en base de datos"""
        if not self.fieldMatricula.value or not self.fieldPassword.value:
            self.error_message.value = "Todos los campos son obligatorios"
            self.error_message.visible = True
            if hasattr(self, 'page'):  # Verifica si el control está en una página
                self.update()
            return
        
        try:
            if self.db.verificar_credenciales(
                matricula_usu=self.fieldMatricula.value.strip(),
                contraseña_usu=self.fieldPassword.value.strip()
            ): 
                usuario = self.db.obtener_usuario_completo_por_matricula(self.fieldMatricula.value)
                snackBar = ft.SnackBar(ft.Text(f"Bienvenido", color=ft.Colors.WHITE),bgcolor=ft.Colors.GREEN)
                self.page.open(snackBar)
                self.page.update()
                if usuario:
                    self.error_message.visible = False                    
                    self.on_login_success(e, usuario[0])
                    return  
                else:
                    self.error_message.value = "Error al obtener datos del usuario"
            else:
                self.error_message.value = "Matrícula o contraseña incorrectos"
            
            self.error_message.visible = True
            if hasattr(self, 'page'):  # Verifica si el control está en una página
                self.update()            
                
        except Exception as ex:
            self.error_message.value = f"Error al iniciar sesión: {str(ex)}"
            self.error_message.visible = True
            if hasattr(self, 'page'):
                self.update()
            