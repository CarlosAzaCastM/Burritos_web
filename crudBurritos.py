# crudBurritos.py
import flet as ft
from datetime import datetime

class ProductoCRUD(ft.Column):
    def __init__(self, datos_usuario, on_go_home, db):
        super().__init__(expand=True)
        self.datos_usu = datos_usuario
        self.db = db
        self.on_go_home = on_go_home
        self.db.connect()

        # Paleta de colores
        self.colorFondo = "#f6efe7"
        self.colorTitulo = "#8b5e3c"
        self.colorSubtitulo = "#d18c60"
        self.colorExtra = "#a1b58c"
        
        # Controles de la interfaz
        self.txtTitulo = ft.Text(value="Gestión de Productos", size=28, weight=ft.FontWeight.BOLD, color=self.colorTitulo)
        self.btnHome = ft.IconButton(icon=ft.Icons.HOME, icon_color=ft.Colors.BLACK, on_click=lambda e: on_go_home(e))
        
        # Formulario para agregar/editar productos
        self.id_producto_actual = None
        self.nombre_prod = ft.TextField(label="Nombre", width=300, color=ft.Colors.BLACK)
        self.descripcion_prod = ft.TextField(label="Descripción", width=300, color=ft.Colors.BLACK, multiline=True)
        self.precio_prod = ft.TextField(label="Precio", width=300, color=ft.Colors.BLACK, keyboard_type=ft.KeyboardType.NUMBER)
        self.existencia_prod = ft.Row(
            controls=[
                ft.Checkbox(
                    label="Disponible", 
                    value=True, 
                    fill_color=self.colorExtra,
                    label_style=ft.TextStyle(
                        color=ft.Colors.BLACK,  
                        size=16  
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        # Botones del formulario
        self.btnGuardar = ft.ElevatedButton(
            text="Guardar",
            on_click=self.guardar_producto,
            bgcolor=self.colorExtra,
            color=ft.Colors.WHITE
        )
        
        self.btnLimpiar = ft.ElevatedButton(
            text="Limpiar",
            on_click=self.limpiar_formulario,
            bgcolor=self.colorSubtitulo,
            color=ft.Colors.WHITE
        )
        
        # Tabla de productos
        self.tabla_productos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Disponible")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            bgcolor=self.colorSubtitulo,
            width=800,
            column_spacing=20 
        )
        
        # Barra de búsqueda
        self.buscar_producto = ft.TextField(
            label="Buscar producto",
            width=300,
            color=ft.Colors.BLACK,
            on_change=self.buscar_productos
        )
        
        # Organización de los controles
        self.formulario = ft.Column(
            controls=[
                ft.Row(controls=[self.btnHome], alignment=ft.MainAxisAlignment.END),
                ft.Row(controls=[self.txtTitulo], alignment=ft.MainAxisAlignment.CENTER),
                self.nombre_prod,
                self.descripcion_prod,
                self.precio_prod,
                self.existencia_prod,
                ft.Row(controls=[self.btnGuardar, self.btnLimpiar], vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
            ],
            spacing=20,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.controls = [
            self.formulario,
            ft.Divider(),
            ft.Row(controls=[self.buscar_producto], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(
                controls=[
                    ft.Container(
                        content=self.tabla_productos,
                        alignment=ft.alignment.center
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True  # Añade esto para que ocupe todo el espacio disponible
            )
        ]

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER
        

    def cargar_productos(self):
        """Carga todos los productos en la tabla"""
        productos = self.db.obtener_todos_productos()
        self.tabla_productos.rows = []
        
        for prod in productos:
            self.tabla_productos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(prod[0]))),  # ID
                        ft.DataCell(ft.Text(prod[1])),       # Nombre
                        ft.DataCell(ft.Text(f"${prod[3]:.2f}")),  # Precio
                        ft.DataCell(ft.Text("Sí" if prod[4] else "No")),  # Disponible
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color="blue",
                                    on_click=lambda e, id=prod[0]: self.editar_producto(id)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color="red",
                                    on_click=lambda e, id=prod[0]: self.eliminar_producto(id)
                                )
                            ])
                        )
                    ],
                )
            )
        self.update()

    def guardar_producto(self, e):
        """Guarda un producto nuevo o actualiza uno existente"""
        try:
            precio = float(self.precio_prod.value)
        except ValueError:
            self.mostrar_mensaje("Error", "El precio debe ser un número válido")
            return
            
        if not self.nombre_prod.value:
            self.mostrar_mensaje("Error", "El nombre es requerido")
            return
            
        datos_producto = {
            "nombre_prod": self.nombre_prod.value,
            "descripcion_prod": self.descripcion_prod.value,
            "precio_prod": precio,
            "existencia_prod": self.existencia_prod.controls[0].value
        }
        
        if self.id_producto_actual:
            # Actualizar producto existente
            if self.db.actualizar_producto(
                self.id_producto_actual,
                **datos_producto
            ):
                self.mostrar_mensaje("Éxito", "Producto actualizado correctamente")
            else:
                self.mostrar_mensaje("Error", "No se pudo actualizar el producto")
        else:
            # Crear nuevo producto
            nuevo_id = self.db.crear_producto(**datos_producto)
            if nuevo_id:
                self.mostrar_mensaje("Éxito", f"Producto creado con ID: {nuevo_id}")
            else:
                self.mostrar_mensaje("Error", "No se pudo crear el producto")
        
        self.limpiar_formulario()
        self.cargar_productos()

    def editar_producto(self, id_producto):
        """Carga un producto en el formulario para editar"""
        producto = self.db.obtener_producto(id_producto)
        if producto:
            self.id_producto_actual = producto[0]
            self.nombre_prod.value = producto[1]
            self.descripcion_prod.value = producto[2]
            self.precio_prod.value = str(producto[3])
            self.existencia_prod.controls[0].value = producto[4]
            self.update()

    def eliminar_producto(self, id_producto):
        """Elimina un producto"""
        def confirmar_eliminar(e):
            if self.db.eliminar_producto(id_producto):
                self.mostrar_mensaje("Éxito", "Producto eliminado correctamente")
                self.cargar_productos()
            else:
                self.mostrar_mensaje("Error", "No se pudo eliminar el producto")
            dialog.open = False
            self.page.update()
            
        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text("¿Estás seguro de que quieres eliminar este producto?"),
            actions=[
                ft.TextButton("Sí", on_click=confirmar_eliminar),
                ft.TextButton("No", on_click=lambda e: setattr(dialog, "open", False))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.open(dialog)        
        self.page.update()

    def limpiar_formulario(self, e=None):
        """Limpia el formulario para agregar un nuevo producto"""
        self.id_producto_actual = None
        self.nombre_prod.value = ""
        self.descripcion_prod.value = ""
        self.precio_prod.value = ""
        self.existencia_prod.controls[0].value = True
        self.update()

    def buscar_productos(self, e):
        """Busca productos por nombre"""
        texto_busqueda = self.buscar_producto.value.strip()
        if texto_busqueda:
            resultados = self.db.buscar_productos_por_nombre(texto_busqueda)
            self.actualizar_tabla(resultados)
        else:
            self.cargar_productos()

    def actualizar_tabla(self, productos):
        """Actualiza la tabla con los productos proporcionados"""
        self.tabla_productos.rows = []
        
        for prod in productos:
            self.tabla_productos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(prod[0]))),  # ID
                        ft.DataCell(ft.Text(prod[1])),       # Nombre
                        ft.DataCell(ft.Text(f"${prod[3]:.2f}")),  # Precio
                        ft.DataCell(ft.Text("Sí" if prod[4] else "No")),  # Disponible
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color="blue",
                                    on_click=lambda e, id=prod[0]: self.editar_producto(id)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color="red",
                                    on_click=lambda e, id=prod[0]: self.eliminar_producto(id)
                                )
                            ])
                        )
                    ],
                    
                )
            )
        self.update()

    def mostrar_mensaje(self, titulo, mensaje):
        """Muestra un mensaje emergente"""
        if hasattr(self, "page") and self.page:
            self.page.snack_bar = ft.SnackBar(
                ft.Text(mensaje),
                bgcolor="green" if titulo == "Éxito" else "red"
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def did_mount(self):
        """Se ejecuta cuando el control se añade a la página"""
        self.db.connect()
        self.cargar_productos()
    
    def will_unmount(self):
        """Se llama cuando la vista va a ser eliminada"""
        self.db.close()