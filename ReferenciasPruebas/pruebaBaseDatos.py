import flet as ft
import psycopg2
from psycopg2 import sql

# Configuración de la base de datos
DB_CONFIG = {
    "host": "localhost",
    "database": "burritos",  # Reemplaza con el nombre de tu BD
    "user": "postgres",           # Reemplaza con tu usuario
    "password": "Ambar72$"     # Reemplaza con tu contraseña
}

# Crear tabla si no existe (ajusta según tu estructura exacta)
def create_table_if_not_exists():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(30),
                matricula VARCHAR(8),
                contraseña VARCHAR(20),
                aula VARCHAR(20),
                salon VARCHAR(20),
                aulaIngles VARCHAR(20),
                salonIngles VARCHAR(20)
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Error al crear tabla: {e}")
    finally:
        if conn:
            conn.close()

# Función para insertar un nuevo usuario
def insert_user(nombre, matricula, contraseña, aula, salon, aulaIngles, salonIngles):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO usuarios (nombre, matricula, contraseña, aula, salon, aulaIngles, salonIngles)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, matricula, contraseña, aula, salon, aulaIngles, salonIngles))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al insertar usuario: {e}")
        return False
    finally:
        if conn:
            conn.close()

def main(page: ft.Page):
    page.title = "Registro de Usuarios"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 600
    page.window_height = 800
    page.window_resizable = False
    
    # Campos del formulario
    nombre = ft.TextField(label="Nombre", width=400)
    matricula = ft.TextField(label="Matrícula", width=400, max_length=8)
    contraseña = ft.TextField(label="Contraseña", width=400, password=True, can_reveal_password=True)
    aula = ft.TextField(label="Aula", width=400)
    salon = ft.TextField(label="Salón", width=400)
    aulaIngles = ft.TextField(label="Aula de Inglés", width=400)
    salonIngles = ft.TextField(label="Salón de Inglés", width=400)
    
    # Mensaje de estado
    status_message = ft.Text("", color=ft.Colors.RED)
    
    def register_click(e):
        if not all([nombre.value, matricula.value, contraseña.value]):
            status_message.value = "Nombre, matrícula y contraseña son obligatorios"
            status_message.color = ft.Colors.RED
            page.update()
            return
        
        success = insert_user(
            nombre.value,
            matricula.value,
            contraseña.value,
            aula.value,
            salon.value,
            aulaIngles.value,
            salonIngles.value
        )
        
        if success:
            status_message.value = "Usuario registrado con éxito!"
            status_message.color = ft.Colors.GREEN
            # Limpiar campos
            nombre.value = ""
            matricula.value = ""
            contraseña.value = ""
            aula.value = ""
            salon.value = ""
            aulaIngles.value = ""
            salonIngles.value = ""
        else:
            status_message.value = "Error al registrar usuario"
            status_message.color = ft.Colors.RED
        
        page.update()
    
    # Crear la interfaz
    page.add(
        ft.Column(
            [
                ft.Text("Registro de Usuarios", size=30, weight=ft.FontWeight.BOLD),
                nombre,
                matricula,
                contraseña,
                aula,
                salon,
                aulaIngles,
                salonIngles,
                ft.ElevatedButton("Registrar", on_click=register_click, width=400),
                status_message
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

# Crear tabla al iniciar
create_table_if_not_exists()

# Ejecutar la aplicación
ft.app(target=main)