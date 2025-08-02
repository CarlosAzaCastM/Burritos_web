from db import Database
import flet as ft
from datetime import datetime

class CortePedidoDetalles(ft.Column):
    def __init__(self, on_go_home, titulo, db: Database):
        super().__init__(expand=True) 

        # Paleta de colores
        self.colorFondo = "#f6efe7"
        self.colorTitulo = "#8b5e3c"
        self.colorSubtitulo = "#d18c60"
        self.colorExtra = "#a1b58c"

        self.scroll = ft.ScrollMode.AUTO

        self.db = db
        self.titulo = titulo

        self.db.connect()

        self.id_pedidoField = ft.TextField(
            label="ID del Pedido",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER,
            color=ft.Colors.BLACK
        )

        self.btnFiltrarDetalles = ft.ElevatedButton(
            text="Filtrar",
            on_click=self.filtrar_detalles,
            bgcolor=self.colorExtra,
            color=ft.Colors.WHITE
        )

        self.txtFormatoFecha = ft.Text("YYYY-MM-DD", color=self.colorSubtitulo, visible=False)

        self.field_fecha = ft.TextField(
            label="Fecha",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER,
            color=ft.Colors.BLACK,
            visible=False
        )

        self.btnFiltrarPedido = ft.ElevatedButton(
            text="Filtrar",
            on_click=self.filtrar_fecha_pedido,
            bgcolor=self.colorExtra,
            color=ft.Colors.WHITE,
            visible=False
        )


        self.ultimosDropdown = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("Buscar por fecha"),
                ft.dropdown.Option("Últimos 3 días"),
                ft.dropdown.Option("Última semana"),
                ft.dropdown.Option("Último mes"),
                ft.dropdown.Option("Último año"),
            ],
            on_change = self.ultimo_dropdown_changed,
            color = ft.Colors.BLACK
        )

        self.ultimosDropdownCorte = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("Buscar por fecha"),
                ft.dropdown.Option("Últimos 3 días"),
                ft.dropdown.Option("Última semana"),
                ft.dropdown.Option("Último mes"),
                ft.dropdown.Option("Último año"),
            ],
            on_change = self.ultimo_dropdown_changedCorte,
            color = ft.Colors.BLACK
        )

        self.btnFiltrarCorte = ft.ElevatedButton(
            text="Filtrar",
            on_click=self.filtrar_fecha_pedido,
            bgcolor=self.colorExtra,
            color=ft.Colors.WHITE,
            visible=False
        )

        self.field_fechaCorte = ft.TextField(
            label="Fecha",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER,
            color=ft.Colors.BLACK,
            visible=False
        )

        self.btnFiltrarCorte = ft.ElevatedButton(
            text="Filtrar",
            on_click=self.filtrar_fecha_corte,
            bgcolor=self.colorExtra,
            color=ft.Colors.WHITE,
            visible=False
        )

        self.txtTitulo = ft.Text(value=self.titulo, size=28, weight=ft.FontWeight.BOLD, color=self.colorTitulo)
        self.btnHome = ft.IconButton(icon=ft.Icons.HOME, icon_color=ft.Colors.BLACK, on_click=lambda e:  on_go_home(e))

        self.table = None  # la tabla se llenará después

        self.controls = [
            self.txtTitulo,
            ft.Row(controls=[self.btnHome], alignment=ft.MainAxisAlignment.END),
        ]

        

        self.spacing = 20
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER

        # Mostrar la tabla de pedidos al cargar
        if(self.titulo == "Pedido"):
            self.mostrar_pedidos()
        elif(self.titulo == "Detalle"):
            self.mostrar_DetallesPedidos()
        elif(self.titulo == "Corte"):
            self.mostrar_CorteDiario()
        else:
            self.mostrar_DetallesPedidos()

    def mostrar_pedidos(self, fecha_pedido = None):
        self.db.connect()
        if fecha_pedido is not None:
            try:
                pedidos = self.db.obtener_pedidos_fecha(fecha_pedido)
            except:
                self.controls.append(ft.Text("Seleccione una fecha válida.", color="red"))
        else:
            pedidos = self.db.obtener_pedidos()

        if self.table:
            self.controls.remove(self.table) 
            self.controls.remove(self.filtros)
        

        self.table = ft.DataTable(
            bgcolor=self.colorSubtitulo,
            columns=[
                ft.DataColumn(ft.Text("ID Pedido")),
                ft.DataColumn(ft.Text("Usuario")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Total")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(p[0]))),  # id_pedido
                        ft.DataCell(ft.Text(p[1])),       # nombre_usu
                        ft.DataCell(ft.Text(str(p[2]))),  # fecha_pedido
                        ft.DataCell(ft.Text(f"${p[3]:,.2f}")),  # total_pedido
                    ]
                )
                for p in pedidos
            ],
        )
        self.filtros = ft.Row(controls=[self.ultimosDropdown,self.txtFormatoFecha,self.field_fecha, self.btnFiltrarPedido],alignment=ft.MainAxisAlignment.CENTER)
        
        self.controls.append(self.filtros)
        self.controls.append(self.table)


    def mostrar_DetallesPedidos(self, id_pedido=None):
        self.db.connect()
        if id_pedido is not None:
            detalles = self.db.pedidoDestalles_por_Idpedido(id_pedido)
        else:
            detalles = self.db.obtener_pedidoDestales()

        if self.table:
            self.controls.remove(self.table) 
            self.controls.remove(self.filtros)

        self.table = ft.DataTable( 
            bgcolor=self.colorSubtitulo,
            columns=[
                ft.DataColumn(ft.Text("ID Pedido")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Subtotal")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(d[1])),       # id_pedido
                        ft.DataCell(ft.Text(str(d[2]))),  # nombre_prod
                        ft.DataCell(ft.Text(str(d[3]))),  # cantidad_prod
                        ft.DataCell(ft.Text(f"${d[4]:,.2f}")),  # subtotal_pedido
                    ]
                )
                for d in detalles
            ],
        )
        self.filtros = ft.Row(controls=[self.id_pedidoField, self.btnFiltrarDetalles], alignment=ft.MainAxisAlignment.CENTER)
        

        self.controls.append(self.filtros)
        self.controls.append(self.table)

    def mostrar_CorteDiario(self, fecha_pedido = None):
        self.db.connect()
        if fecha_pedido is not None:
            try:
                corte = self.db.obtener_corte_fecha(fecha_pedido)
            except:
                print("Aqui en corteDiario")
                self.controls.append(ft.Text("Seleccione una fecha válida.", color="red"))
        else:
            corte = self.db.obtener_corte()
        
        if self.table:
            self.controls.remove(self.table) 
            self.controls.remove(self.filtros)
        

        self.table = ft.DataTable(
            bgcolor=self.colorSubtitulo, 
            columns=[
                ft.DataColumn(ft.Text("Producto mas vendido")),
                ft.DataColumn(ft.Text("Total dia")),
                ft.DataColumn(ft.Text("Fecha")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(c[1])),       # nombre_prod
                        ft.DataCell(ft.Text(f"${c[2]:,.2f}")),  # venta_total_dia  
                        ft.DataCell(ft.Text(str(c[3]))),  # fecha_corte
                    ]
                )
                for c in corte
            ],
        )
        self.filtros = ft.Row(controls=[self.ultimosDropdownCorte,self.txtFormatoFecha,self.field_fechaCorte, self.btnFiltrarCorte],alignment=ft.MainAxisAlignment.CENTER)
        

        self.controls.append(self.filtros)
        self.controls.append(self.table)

    def filtrar_detalles(self, e):
        self.db.connect()
        try:
            id_pedido = int(self.id_pedidoField.value.strip())
        except ValueError:
            self.controls.append(ft.Text("Por favor ingrese un ID válido.", color="red"))
            self.update()
            return

        self.mostrar_DetallesPedidos(id_pedido)
        self.update()

    def validar_fecha(self, fecha_str):
        try:
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def filtrar_fecha_pedido(self, e):
        self.db.connect()
        fecha = self.field_fecha.value.strip()
        if not fecha:
            self.controls.append(ft.Text("Seleccione una fecha válida.", color="red"))
            self.update()
            return
        if not self.validar_fecha(fecha):
            self.controls.append(ft.Text("Formato de fecha inválido. Use YYYY-MM-DD", color="red"))

        self.mostrar_pedidos(fecha)
        self.update()

    def filtrar_fecha_corte(self, e):
        self.db.connect()
        fecha = self.field_fechaCorte.value.strip()
        if not fecha:
            self.controls.append(ft.Text("Seleccione una fecha válida.", color="red"))
            self.update()
            return
        if not self.validar_fecha(fecha):
            self.controls.append(ft.Text("Formato de fecha inválido. Use YYYY-MM-DD", color="red"))

        self.mostrar_CorteDiario(fecha)
        self.update()
    
    def ultimo_dropdown_changed(self, e):
        self.db.connect()
        self.lugar = self.ultimosDropdown.value
        if self.lugar == "Buscar por fecha":
            self.txtFormatoFecha.visible = True
            self.field_fecha.visible = True
            self.btnFiltrarPedido.visible = True
        else:
            self.txtFormatoFecha.visible = False
            self.field_fecha.visible = False
            self.btnFiltrarPedido.visible = False
            
            if self.lugar == "Últimos 3 días":
                dias = 3
            elif self.lugar == "Última semana":
                dias = 7
            elif self.lugar == "Último mes":
                dias = 30
            elif self.lugar == "Último año":
                dias = 365
            else:
                dias = None
                
            if dias is not None:
                pedidos = self.db.obtener_pedido_ultimos_dias(dias)
                self.mostrar_pedidos_filtrados(pedidos)
        
        self.page.update()

    def ultimo_dropdown_changedCorte(self, e):
        self.db.connect()
        self.lugar = self.ultimosDropdownCorte.value
        if self.lugar == "Buscar por fecha":
            self.txtFormatoFecha.visible = True
            self.field_fechaCorte.visible = True
            self.btnFiltrarCorte.visible = True
        else:
            self.txtFormatoFecha.visible = False
            self.field_fechaCorte.visible = False
            self.btnFiltrarCorte.visible = False
            
            if self.lugar == "Últimos 3 días":
                dias = 3
            elif self.lugar == "Última semana":
                dias = 7
            elif self.lugar == "Último mes":
                dias = 30
            elif self.lugar == "Último año":
                dias = 365
            else:
                dias = None
                
            if dias is not None:
                pedidos = self.db.obtener_corte_ultimos_dias(dias)
                self.mostrar_pedidos_filtradosCorte(pedidos)
        
        self.page.update()

    def mostrar_pedidos_filtrados(self, pedidos):
        self.db.connect()
        if self.table:
            self.controls.remove(self.table)
            self.controls.remove(self.filtros)
        
        self.table = ft.DataTable(
            bgcolor=self.colorSubtitulo,
            columns=[
                ft.DataColumn(ft.Text("ID Pedido")),
                ft.DataColumn(ft.Text("Usuario")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Total")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(p[0]))),  # id_pedido
                        ft.DataCell(ft.Text(p[1])),       # nombre_usu
                        ft.DataCell(ft.Text(str(p[2]))),  # fecha_pedido
                        ft.DataCell(ft.Text(f"${p[3]:,.2f}")),  # total_pedido
                    ]
                )
                for p in pedidos
            ],
        )
        
        self.controls.append(self.filtros)
        self.controls.append(self.table)
        self.update()

    def mostrar_pedidos_filtradosCorte(self, pedidos):
        self.db.connect()
        if self.table:
            self.controls.remove(self.table)
            self.controls.remove(self.filtros)
        
        self.table = ft.DataTable(
            bgcolor=self.colorSubtitulo,
            columns=[
                ft.DataColumn(ft.Text("Burrito Mas Vendido")),
                ft.DataColumn(ft.Text("Total del dia")),
                ft.DataColumn(ft.Text("Fecha corte")),
            ],
            rows=[
                ft.DataRow(
                    cells=[ 
                        ft.DataCell(ft.Text(p[0])),       
                        ft.DataCell(ft.Text(str(p[1]))),  
                        ft.DataCell(ft.Text(str(p[2]))),  
                    ]
                )
                for p in pedidos
            ],
        )
        self.controls.append(self.filtros)
        self.controls.append(self.table)
        self.update()

    def will_unmount(self):
        """Se llama cuando la vista va a ser eliminada"""
        self.db.close()