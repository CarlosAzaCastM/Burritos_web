import flet as ft
from datetime import datetime

class StockBurritos(ft.Column):
    def __init__(self, datos_usuario, on_go_home, db):
        super().__init__(expand=True)
        self.datos_usu = datos_usuario
        self.db = db
        self.on_go_home = on_go_home
        self.fecha_actual = datetime.now()

        # IDs de producto
        self.ids_productos = {
            'rojo': 1,
            'verde': 2,
            'carnitas': 3,
            'tinga': 4,
            'deshebrada': 5,
            'papas_picadillo': 6,
            'pastor': 7
        }

        # Obtener el sabor del día
        self.sabor_dia = self.verificarDia()
        
        self.txtBurritosRojo = ft.Text(value="Chicharrón Rojo", size=20, color="#000000")
        self.checkBoxBurritosRojo = ft.Checkbox(
            width=30, 
            height=30,
            value=bool(self.db.existenciaText_producto(1)),  
            on_change=lambda e: self.actualizar_stock('rojo', e.control.value)
        )
        
        
        self.txtBurritosVerde = ft.Text(value="Chicharrón Verde", size=20, color="#000000")
        self.checkBoxBurritosVerde = ft.Checkbox(
            width=30, 
            height=30,
            value=bool(self.db.existenciaText_producto(2)),  
            on_change=lambda e: self.actualizar_stock('verde', e.control.value)
        )
        

        self.txtBurritosCarnitas = ft.Text(value="Carnitas", size=20, color="#000000")
        self.checkBoxBurritosCarnitas= ft.Checkbox(
            width=30, 
            height=30,
            value=bool(self.db.existenciaText_producto(3)),
            on_change=lambda e: self.actualizar_stock('carnitas', e.control.value)
        )
        

        self.txtBurritosTinga = ft.Text(value="Tinga", size=20, color="#000000")
        self.checkBoxBurritosTinga = ft.Checkbox(
            width=30, 
            height=30,
            value=bool(self.db.existenciaText_producto(4)),  
            on_change=lambda e: self.actualizar_stock('tinga', e.control.value)
        )
        
        
        self.txtBurritosDeshebrada = ft.Text(value="Deshebrada", size=20, color="#000000")
        self.checkBoxBurritosDeshebrada = ft.Checkbox(
            width=30, 
            height=30,
            value=bool(self.db.existenciaText_producto(5)),  
            on_change=lambda e: self.actualizar_stock('deshebrada', e.control.value)
        )
        

        self.txtBurritosPapas = ft.Text(value="Papas con picadillo", size=20, color="#000000")
        self.checkBoxBurritosPapas= ft.Checkbox(
            width=30, 
            height=30,
            value=bool(self.db.existenciaText_producto(6)), 
            on_change=lambda e: self.actualizar_stock('papas_picadillo', e.control.value)
        )
        
        self.txtBurritosPastor = ft.Text(value="Pastor", size=20, color="#000000")
        self.checkBoxBurritosPastor= ft.Checkbox(
            width=30, 
            height=30,
            value=bool(self.db.existenciaText_producto(7)), 
            on_change=lambda e: self.actualizar_stock('pastor', e.control.value)
        )
        

        self.btnVolver = ft.ElevatedButton(
            text="Volver al menú",
            on_click=lambda e: on_go_home(e),
            bgcolor="#4a6741",
            color="white"
        )

        self.controls = [
            ft.Row(
                controls=[
                    self.txtBurritosRojo, 
                    self.checkBoxBurritosRojo
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Row(
                controls=[
                    self.txtBurritosVerde, 
                    self.checkBoxBurritosVerde
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Row(
                controls=[
                    self.txtBurritosCarnitas, 
                    self.checkBoxBurritosCarnitas
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Row(
                controls=[
                    self.txtBurritosTinga, 
                    self.checkBoxBurritosTinga
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Row(
                controls=[
                    self.txtBurritosDeshebrada, 
                    self.checkBoxBurritosDeshebrada
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Row(
                controls=[
                    self.txtBurritosPapas, 
                    self.checkBoxBurritosPapas
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Row(
                controls=[
                    self.txtBurritosPastor, 
                    self.checkBoxBurritosPastor
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Row(controls=[self.btnVolver], alignment=ft.MainAxisAlignment.CENTER)
        ]
        
        
        self.spacing = 20
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER
        

    def actualizar_stock(self, tipo_burrito, disponible):
        """Actualiza el stock en la base de datos"""
        try:
            id_producto = self.ids_productos[tipo_burrito]
            success = self.db.actualizar_stock_producto(id_producto, disponible)
            if success:
                if self.page is not None:
                    self.snack_bar1 = ft.SnackBar(
                        ft.Text("Estado actualizado correctamente en la base de datos"),
                        bgcolor=ft.Colors.GREEN_400
                    )
                    self.page.open(self.snack_bar1)
                    self.page.update()
            else:
                print(f"No se pudo actualizar el stock para {tipo_burrito}")
        except Exception as e:
            print(f"Error al actualizar stock: {e}")

    # ... (resto de los métodos permanecen igual)
    def obtener_clave_sabor(self):
        """Devuelve la clave del diccionario para el sabor del día"""
        nombre_dia = self.fecha_actual.strftime("%A")
        if nombre_dia == "Monday":
            return "carnitas"
        elif nombre_dia == "Tuesday":
            return "tinga"
        elif nombre_dia == "Wednesday":
            return "deshebrada"
        elif nombre_dia == "Thursday":
            return "papas_picadillo"
        elif nombre_dia == "Friday":
            return "pastor"
        else:
            return "carnitas"  # Valor por defecto

    def verificarDia(self):
        nombre_dia = self.fecha_actual.strftime("%A")

        if nombre_dia == "Monday":
            return "Carnitas"
        elif nombre_dia == "Tuesday":
            return "Tinga"
        elif nombre_dia == "Wednesday":
            return "Deshebrada"
        elif nombre_dia == "Thursday":
            return "Papas con picadillo"
        elif nombre_dia == "Friday":
            return "Pastor"
        else:
            return "Sabor del día"