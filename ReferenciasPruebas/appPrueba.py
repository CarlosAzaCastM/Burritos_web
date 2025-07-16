import flet as ft
import psycopg2

# Conexión a la base de datos
def get_connection():
    return psycopg2.connect(
        dbname="dbburritos",
        user="root",         # <- Reemplaza con tu usuario de PostgreSQL
        password="LQOvHjZ7Gn54wiN7mqw9fGiYvoOTBhR2",  # <- Reemplaza con tu contraseña
        host="dpg-d0t90eadbo4c739e4510-a.oregon-postgres.render.com",
        port="5432"
    )

# Insertar usuario
def insertar_usuario(id_usuario, nombre, contraseña, aula, salon, aula_ingles, salon_ingles):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO "Usuario" ("Id", "nombre_usu", "contraseña_usu", "aula_usu", "salon_usu", "aulaIngles_usu", "salonIngles_usu")
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (id_usuario, nombre, contraseña, aula, salon, aula_ingles, salon_ingles))
    conn.commit()
    cur.close()
    conn.close()

# Obtener usuarios
def obtener_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                SELECT * FROM "Usuario"
                """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Aplicación Flet
def main(page: ft.Page):
    page.title = "Registro de Usuarios"
    page.window_width = 500
    page.window_height = 800
    page.scroll = "auto"

    matricula = ft.TextField(label="Matrícula (ID)", keyboard_type=ft.KeyboardType.NUMBER)
    nombre = ft.TextField(label="Nombre")
    contraseña = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
    aula = ft.TextField(label="Aula", keyboard_type=ft.KeyboardType.NUMBER)
    salon = ft.TextField(label="Salón", keyboard_type=ft.KeyboardType.NUMBER)
    aula_ingles = ft.TextField(label="Aula Inglés", keyboard_type=ft.KeyboardType.NUMBER)
    salon_ingles = ft.TextField(label="Salón Inglés", keyboard_type=ft.KeyboardType.NUMBER)
    resultado = ft.Text("")

    def registrar(e):
        try:
            insertar_usuario(
                int(matricula.value),
                nombre.value,
                contraseña.value,
                int(aula.value),
                int(salon.value),
                int(aula_ingles.value),
                int(salon_ingles.value)
            )
            resultado.value = "✅ Usuario registrado con éxito."
            for campo in [matricula, nombre, contraseña, aula, salon, aula_ingles, salon_ingles]:
                campo.value = ""
        except Exception as ex:
            resultado.value = f"❌ Error: {ex}"
        page.update()

    def mostrar_usuarios(e):
        usuarios = obtener_usuarios()
        contenido = "\n\n".join([
            f"Matrícula: {u[0]}\nNombre: {u[1]}\nAula: {u[3]}\nSalón: {u[4]}\nAula Inglés: {u[5]}\nSalón Inglés: {u[6]}"
            for u in usuarios
        ]) or "No hay usuarios registrados."

        page.views.append(
            ft.View("/ver", [
                ft.Text("Usuarios Registrados", size=20, weight="bold"),
                ft.Text(contenido),
                ft.ElevatedButton("← Volver", on_click=lambda e: page.go("/"))
            ])
        )
        page.update()

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                ft.View("/", [
                    ft.Text("Registro de Usuario", size=25, weight="bold"),
                    matricula, nombre, contraseña,
                    aula, salon, aula_ingles, salon_ingles,
                    ft.ElevatedButton("Registrar", on_click=registrar),
                    ft.ElevatedButton("Ver Usuarios Registrados", on_click=mostrar_usuarios),
                    resultado
                ])
            )
        page.update()

    page.on_route_change = route_change
    page.go("/")

# Ejecutar como app web
ft.app(target=main, view=ft.WEB_BROWSER)
