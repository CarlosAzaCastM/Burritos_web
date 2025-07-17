#main.py
import flet as ft
from inicio_sesion import InicioSesion
from registro import Registro
from db import Database
from menu import Menu
from menu_elecciones import MenuElecciones
from actulizar import Actulizar
from corte_pedido_detalles import CortePedidoDetalles
from stock_burritos import StockBurritos

def main(page: ft.Page):
    # Configuración de la página para web
    page.title = "Mi Aplicación Web"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#f6efe7"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO 

    db = Database(
        dbname="burritosbd",
        user="root",
        password="8ETAhe0iScPkNlNnEXwrQHGQgqy59iIu",
        host="d1rj3615pdvs73e5oi10-a.oregon-postgres.render.com"
    )
    
    # Contenedor principal que cambiará entre vistas
    main_container = ft.Column(expand=True)
    page.add(main_container)  
    
    def show_login():
        """Muestra la vista de inicio de sesión"""
        main_container.controls.clear()
        main_container.controls.append(InicioSesion(
            on_login_success=lambda e, data: show_menu_elecciones(data),
            on_go_to_register=lambda e: show_register(),
            db=db
        ))
        page.update()

    def show_register():
        """Muestra la vista de registro"""
        main_container.controls.clear()
        main_container.controls.append(Registro(
            on_register_success=lambda e: show_login(),
            on_go_to_login=lambda e: show_login(),
            db=db
        ))
        page.update()

    def show_menu_elecciones(usuario_data):
        """Muestra el menú de elecciones"""
        main_container.controls.clear()
        main_container.controls.append(MenuElecciones(
            on_pedir_burritos=lambda e: show_menu(usuario_data, db=db),
            on_actulizar=lambda e: show_actulizar(usuario_data, db=db),
            on_go_login=lambda e: show_login(),
            on_corte=lambda e: show_corte_pedido_detalles(usuario_data, "Corte"),
            on_pedido=lambda e: show_corte_pedido_detalles(usuario_data, "Pedido"),
            on_detalles=lambda e: show_corte_pedido_detalles(usuario_data, "Detalles"),
            on_stock=lambda e: show_stock(usuario_data,db=db),
            matricula_usu=usuario_data['matricula_usu']
        ))
        page.update() 

    def show_menu(usuario_data, db):
        """Muestra el menú principal de burritos"""
        main_container.controls.clear()
        main_container.controls.append(Menu(
            id_usuario=usuario_data['id_usuario'],
            nombre=usuario_data['nombre_usu'],
            aula=usuario_data['aula_usu'],
            salon=usuario_data['salon_usu'],
            aula_ingles=usuario_data['aulaIngles_usu'],
            salon_ingles=usuario_data['salonIngles_usu'],
            on_go_home=lambda e: show_menu_elecciones(usuario_data),
            db=db
        ))
        page.update()

    def show_actulizar(usuario_data, db):
        """Muestra la vista de actualización"""
        main_container.controls.clear()
        main_container.controls.append(Actulizar(
            datos_usuario=usuario_data,  
            on_go_home=lambda e: show_menu_elecciones(usuario_data),
            db=db
        ))
        page.update()

    def show_corte_pedido_detalles(usuario_data, pantalla):
        main_container.controls.clear()
        main_container.controls.append(CortePedidoDetalles(  
            on_go_home=lambda e: show_menu_elecciones(usuario_data),
            titulo = pantalla
        ))
        page.update()

    def show_stock(usuario_data, db):
        main_container.controls.clear()
        main_container.controls.append(StockBurritos(  
            datos_usuario=usuario_data,
            on_go_home=lambda e: show_menu_elecciones(usuario_data),
            db=db
        ))
        page.update()


    # Iniciar con la vista de inicio de sesión
    show_login()
    
    # Cerrar conexión al salir
    page.on_close = lambda _: db.close()

ft.app(target=main, view=ft.WEB_BROWSER)