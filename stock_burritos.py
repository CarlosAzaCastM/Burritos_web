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
            'desebrada': 5,
            'papas_picadillo': 6,
            'pastor': 7
        }

        # Obtener el sabor del día
        self.sabor_dia = self.verificarDia()
        
        # Función para crear indicadores de estado con valor inicial (se actualizará al cargar)
        def crear_indicador_estado():
            return ft.Container(
                width=20,
                height=20,
                border_radius=10,
                bgcolor=ft.Colors.RED_400
            )
        
        # Componentes UI con indicadores de estado
        self.indicador_rojo = crear_indicador_estado()
        self.txtBurritosRojo = ft.Text(value="Chicharrón Rojo", size=20, color="#000000")
        self.checkBoxBurritosRojo = ft.Checkbox(
            width=30, 
            height=30,
            value=False,  # Valor inicial, se actualizará al cargar
            on_change=lambda e: self.actualizar_stock('rojo', e.control.value)
        )
        
        self.indicador_verde = crear_indicador_estado()
        self.txtBurritosVerde = ft.Text(value="Chicharrón Verde", size=20, color="#000000")
        self.checkBoxBurritosVerde = ft.Checkbox(
            width=30, 
            height=30,
            value=False,  # Valor inicial, se actualizará al cargar
            on_change=lambda e: self.actualizar_stock('verde', e.control.value)
        )
        
        # Texto dinámico para el sabor del día
        self.indicador_sabor_dia = crear_indicador_estado()
        self.txtSaborDia = ft.Text(value=self.sabor_dia, size=20, color="#000000")
        self.checkBoxSaborDia = ft.Checkbox(
            width=30, 
            height=30,
            value=False,  # Valor inicial, se actualizará al cargar
            on_change=lambda e: self.actualizar_stock(self.obtener_clave_sabor(), e.control.value)
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
                    self.indicador_rojo,
                    self.txtBurritosRojo, 
                    self.checkBoxBurritosRojo
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Row(
                controls=[
                    self.indicador_verde,
                    self.txtBurritosVerde, 
                    self.checkBoxBurritosVerde
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Row(
                controls=[
                    self.indicador_sabor_dia,
                    self.txtSaborDia, 
                    self.checkBoxSaborDia
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Row(controls=[self.btnVolver], alignment=ft.MainAxisAlignment.CENTER)
        ]
        
        self.spacing = 20
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER
        
        # Carga diferida hasta que esté en la página
        self.on_add = lambda _: self.cargar_stock_actual()

    def actualizar_indicadores(self):
        """Actualiza los indicadores visuales según el estado de los checkboxes"""
        self.indicador_rojo.bgcolor = ft.Colors.GREEN_400 if self.checkBoxBurritosRojo.value else ft.Colors.RED_400
        self.indicador_verde.bgcolor = ft.Colors.GREEN_400 if self.checkBoxBurritosVerde.value else ft.Colors.RED_400
        self.indicador_sabor_dia.bgcolor = ft.Colors.GREEN_400 if self.checkBoxSaborDia.value else ft.Colors.RED_400
        self.update()

    def cargar_stock_actual(self):
        """Carga el estado actual del stock desde la base de datos"""
        try:
            # Obtener clave del sabor del día
            clave_sabor = self.obtener_clave_sabor()
            
            # Obtener IDs de productos a consultar (los 2 fijos + el del día)
            ids_a_consultar = [
                self.ids_productos['rojo'],
                self.ids_productos['verde'],
                self.ids_productos[clave_sabor]
            ]
            
            # Obtener datos de la base de datos
            stock_data = self.db.obtener_stock_productos(ids_a_consultar)
            
            if stock_data:
                # Asignar valores a los checkboxes desde la base de datos
                def convertir_a_bool(valor):
                    return str(valor).lower() in ("1", "true", "t", "yes")
                
                rojo_id = self.ids_productos['rojo']
                verde_id = self.ids_productos['verde']
                sabor_id = self.ids_productos[clave_sabor]

                print("Stock desde base de datos:", stock_data)

                self.checkBoxBurritosRojo.value = convertir_a_bool(stock_data.get(rojo_id, 0))
                self.checkBoxBurritosVerde.value = convertir_a_bool(stock_data.get(verde_id, 0))
                self.checkBoxSaborDia.value = convertir_a_bool(stock_data.get(sabor_id, 0))

                
                # Actualizar texto del sabor del día
                self.txtSaborDia.value = self.sabor_dia
                
                # Actualizar indicadores visuales según los valores de los checkboxes
                self.actualizar_indicadores()
                
                if self.page is not None:
                    self.page.snack_bar = ft.SnackBar(
                        ft.Text("Datos cargados correctamente desde la base de datos"),
                        bgcolor=ft.Colors.GREEN_400
                    )
                    self.page.snack_bar.open = True
                    self.page.update()

        except Exception as e:
            print(f"Error al cargar stock: {e}")
            if self.page is not None:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Error al cargar datos: {str(e)}"),
                    bgcolor=ft.Colors.RED_400
                )
                self.page.snack_bar.open = True
                self.page.update()

    def actualizar_stock(self, tipo_burrito, disponible):
        """Actualiza el stock en la base de datos"""
        try:
            id_producto = self.ids_productos[tipo_burrito]
            success = self.db.actualizar_stock_producto(id_producto, disponible)
            if success:
                self.actualizar_indicadores()
                if self.page is not None:
                    self.page.snack_bar = ft.SnackBar(
                        ft.Text("Estado actualizado correctamente en la base de datos"),
                        bgcolor=ft.Colors.GREEN_400
                    )
                    self.page.snack_bar.open = True
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
            return "desebrada"
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
            return "Desebrada"
        elif nombre_dia == "Thursday":
            return "Papas con picadillo"
        elif nombre_dia == "Friday":
            return "Pastor"
        else:
            return "Sabor del día"