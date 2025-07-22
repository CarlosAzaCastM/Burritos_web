from db import Database
import flet as ft

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

    def mostrar_pedidos(self):
        pedidos = self.db.obtener_pedidos()

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

        self.controls.append(self.table)

    def mostrar_DetallesPedidos(self):
        detalles = self.db.obtener_pedidoDestales()

        self.table = ft.DataTable(
            bgcolor=self.colorSubtitulo,
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("ID Pedido")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Subtotal")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(d[0]))),  # id
                        ft.DataCell(ft.Text(d[1])),       # id_pedido
                        ft.DataCell(ft.Text(str(d[2]))),  # nombre_prod
                        ft.DataCell(ft.Text(str(d[3]))),  # cantidad_prod
                        ft.DataCell(ft.Text(f"${d[4]:,.2f}")),  # subtotal_pedido
                    ]
                )
                for d in detalles
            ],
        )

        self.controls.append(self.table)

    def mostrar_CorteDiario(self):
        corte = self.db.obtener_corte()

        self.table = ft.DataTable(
            bgcolor=self.colorSubtitulo,
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Total dia")),
                ft.DataColumn(ft.Text("Fecha")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(c[0]))),  # id
                        ft.DataCell(ft.Text(c[1])),       # nombre_prod
                        ft.DataCell(ft.Text(f"${c[2]:,.2f}")),  # venta_total_dia  
                        ft.DataCell(ft.Text(str(c[3]))),  # fecha_corte
                    ]
                )
                for c in corte
            ],
        )

        self.controls.append(self.table)

