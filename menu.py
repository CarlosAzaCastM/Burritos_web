#menu.py
import flet as ft
from whatstest import WhatsTest

from datetime import datetime


class Menu(ft.Column):

    
    def __init__(self, id_usuario, nombre, aula, salon, aula_ingles, salon_ingles, on_go_home, db):
        super().__init__(expand=True)

        self.fecha_actual = datetime.now()

        self.whatsapp = WhatsTest()

        self.idUsuario = id_usuario
        self.nombre = nombre
        self.aula = aula
        self.salon = salon
        self.aula_ingles = aula_ingles
        self.salon_ingles = salon_ingles
        self.db = db
        #Numero de cuenta donde Angel le van a llegar las transferencias
        self.numeroCuenta = "638180000177661017"
    
        self.ids_productos = {
            'rojo': 1,
            'verde': 2,
            'carnitas': 3,
            'tinga': 4,
            'desebrada': 5,
            'papas_picadillo': 6,
            'pastor': 7
        }

        self.precio = 15
        self.precioEspecial = 20
        
  

        self.burritosPrecioTotal = 0

        self.burritosRojoCantidad = 0
        self.burritosVerdeCantidad = 0
        self.burritosOtroCantidad = 0

        self.tipoPago = "Ninguno"

        #Paleta de colores
        self.colorFondo = "#f6efe7"
        self.colorTitulo = "#8b5e3c"
        self.colorSubtitulo = "#d18c60"
        self.colorExtra = "#a1b58c"

        #Logo de la abuela
        self.drive_image_id = "1D3EKaKUhD0dupYd0dbuM5nEjAlD_fSYU"  # Reemplaza con tu ID real
        self.drive_url = f"https://lh3.googleusercontent.com/d/{self.drive_image_id}=s200?authuser=0"
    

        self.img_control = ft.Image(
        src=self.drive_url,
        width=200,  # Ancho en píxeles
        height=100,  # Alto en píxeles
        fit=ft.ImageFit.CONTAIN,  # Ajuste: CONTAIN, COVER, FILL, etc.
        repeat=ft.ImageRepeat.NO_REPEAT,
        border_radius=ft.border_radius.all(10),  # Esquinas redondeadas
        tooltip="Imagen desde Google Drive",
        error_content=ft.Text("Error al cargar la imagen")  # Mensaje si falla
        )

        self.txtUser = ft.Text(value=f"Usuario: {self.nombre}", size=12, color=self.colorSubtitulo)
        self.txtTitle = ft.Text(value="Menú", size=25, color=self.colorTitulo, weight=ft.FontWeight.BOLD)

        self.btnHome = ft.IconButton(icon=ft.Icons.HOME, icon_color=ft.Colors.BLACK, on_click=lambda e:  on_go_home(e))
        
        # Elementos para Chicharrón Rojo
        self.txtRojo = ft.Text(value="Chicharron rojo", size=20, color="#9b3b3b")
        self.fieldRojo = ft.TextField(width=44, height=70, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK, read_only=True)
        self.btnRojoMas = ft.IconButton(icon=ft.Icons.ADD, bgcolor=self.colorSubtitulo, on_click=self.add_rojo, icon_color=ft.Colors.BLACK)
        self.btnRojoMenos = ft.IconButton(icon=ft.Icons.REMOVE, bgcolor=self.colorSubtitulo, on_click=self.remove_rojo, icon_color=ft.Colors.BLACK)
        self.existencia("1","Chicharron rojo",self.txtRojo,self.btnRojoMas,self.btnRojoMenos)
        
        # Elementos para Chicharrón Verde
        self.txtVerde = ft.Text(value="Chicharrón verde", size=20, color="#6d9b3b")
        self.fieldVerde = ft.TextField(width=44, height=70, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK, read_only=True)
        self.btnVerdeMas = ft.IconButton(icon=ft.Icons.ADD, bgcolor=self.colorSubtitulo, on_click=self.add_verde, icon_color=ft.Colors.BLACK)
        self.btnVerdeMenos = ft.IconButton(icon=ft.Icons.REMOVE, bgcolor=self.colorSubtitulo, on_click=self.remove_verde, icon_color=ft.Colors.BLACK)
        self.existencia("2","Chicharron verde",self.txtVerde,self.btnVerdeMas,self.btnVerdeMenos)

        # Elementos para otro sabor
        self.txtOtro = ft.Text(value=self.verificarDia(), size=20, color="#3b519b")
        self.fieldOtro = ft.TextField(width=44, height=70, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK, read_only=True)
        self.btnOtroMas = ft.IconButton(icon=ft.Icons.ADD, bgcolor=self.colorSubtitulo, on_click=self.add_otro, icon_color=ft.Colors.BLACK)
        self.btnOtroMenos = ft.IconButton(icon=ft.Icons.REMOVE, bgcolor=self.colorSubtitulo, on_click=self.remove_otro, icon_color=ft.Colors.BLACK)
        self.existencia(str(self.ids_productos[self.verificarCodigo()]),self.verificarDia(),self.txtOtro,self.btnOtroMas,self.btnOtroMenos)
        
        # Elementos tipo de pago
        self.tipoPagotxt = ft.Text(value="Tipo de pago", size=20, color="#3b519b")

        # Crear el dropdown
        self.tipoPagoDropdown = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("Transferencia"),
                ft.dropdown.Option("Efectivo"),
            ],
            on_change = self.tipo_pago_dropdown_changed,
            color = ft.Colors.BLACK
        )
        self.txtNumeroCuenta = ft.Text(value="Cuenta: "+self.numeroCuenta, color=ft.Colors.BLACK, visible=False)

        self.txtLugar = ft.Text(value="Lugar", size=20, color="#3b519b")
        self.lugarDropdown = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("Mi aula"),
                ft.dropdown.Option("En ingles"),
                ft.dropdown.Option("Cafeteria"),
                ft.dropdown.Option("Gradas"),
                ft.dropdown.Option("Otro"),
            ],
            on_change = self.lugar_dropdown_changed,
            color = ft.Colors.BLACK
        )
        self.lugarField = ft.TextField(width=160, height=70, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK, visible=False)
            
        # Elementos para el total
        self.txtTotal = ft.Text(value="Total costo", size=20, color=ft.Colors.BLACK)
        self.fieldTotal = ft.TextField(width=80, height=70, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK, read_only=True)

        #Boton enviar
        self.btnEnviar = ft.Button("ENVIAR", bgcolor=self.colorExtra,  color=ft.Colors.BLACK, on_click=self.click_enviar)
        
        self.controls = [
            ft.Row(
                controls=[
                    self.txtUser,
                    self.btnHome,
                ],
                alignment=ft.MainAxisAlignment.CENTER,  
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing= 100,
            ),
            self.img_control,
            self.txtTitle,
            ft.Row(
                controls=[
                    self.txtRojo,
                    self.btnRojoMenos,
                    self.fieldRojo,
                    self.btnRojoMas,
                ],
                alignment=ft.MainAxisAlignment.CENTER,  
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.txtVerde,
                    self.btnVerdeMenos,
                    self.fieldVerde,
                    self.btnVerdeMas,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.txtOtro,
                    self.btnOtroMenos,
                    self.fieldOtro,
                    self.btnOtroMas,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                   self.txtLugar,
                   self.lugarDropdown, 
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            self.lugarField,
            ft.Row(
                controls=[
                    self.tipoPagotxt,
                    self.tipoPagoDropdown,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            self.txtNumeroCuenta,
            ft.Row(
                controls=[
                    self.txtTotal,
                    self.fieldTotal,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            self.btnEnviar
        ]
        self.spacing = 20
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment=ft.MainAxisAlignment.CENTER,  
   

    def add_rojo(self, e):
        self.burritosRojoCantidad += 1
        self.fieldRojo.value = str(self.burritosRojoCantidad)

        if(self.verificarDia() == "Pastor" or self.verificarDia() == "Carnitas"):
            self.burritosSubNormal = (self.burritosVerdeCantidad + self.burritosRojoCantidad) * self.precio
            self.burritosSubEspecial = self.burritosOtroCantidad * self.precioEspecial
            self.burritosPrecioTotal = self.burritosSubEspecial + self.burritosSubNormal
        else:
            self.burritosPrecioTotal = (self.burritosVerdeCantidad + self.burritosRojoCantidad + self.burritosOtroCantidad) * self.precio
            
        self.fieldTotal.value = str(self.burritosPrecioTotal)
        self.update()

    def remove_rojo(self, e):
        if(self.burritosRojoCantidad>0):
            self.burritosRojoCantidad -= 1
            self.fieldRojo.value = str(self.burritosRojoCantidad)

        if(self.verificarDia() == "Pastor" or self.verificarDia() == "Carnitas"):
            self.burritosSubNormal = (self.burritosVerdeCantidad + self.burritosRojoCantidad) * self.precio
            self.burritosSubEspecial = self.burritosOtroCantidad * self.precioEspecial
            self.burritosPrecioTotal = self.burritosSubEspecial + self.burritosSubNormal
        else:
            self.burritosPrecioTotal = (self.burritosVerdeCantidad + self.burritosRojoCantidad + self.burritosOtroCantidad) * self.precio
            
        self.fieldTotal.value = str(self.burritosPrecioTotal)
        self.update()
    
    def add_verde(self, e):
        self.burritosVerdeCantidad += 1
        self.fieldVerde.value = str(self.burritosVerdeCantidad)

        if(self.verificarDia() == "Pastor" or self.verificarDia() == "Carnitas"):
            self.burritosSubNormal = (self.burritosVerdeCantidad + self.burritosRojoCantidad) * self.precio
            self.burritosSubEspecial = self.burritosOtroCantidad * self.precioEspecial
            self.burritosPrecioTotal = self.burritosSubEspecial + self.burritosSubNormal
        else:
            self.burritosPrecioTotal = (self.burritosVerdeCantidad + self.burritosRojoCantidad + self.burritosOtroCantidad) * self.precio
            
        self.fieldTotal.value = str(self.burritosPrecioTotal)
        self.update()
    def remove_verde(self, e):

        if (self.burritosVerdeCantidad>0):
            self.burritosVerdeCantidad -= 1
            self.fieldVerde.value = str(self.burritosVerdeCantidad)

        if(self.verificarDia() == "Pastor" or self.verificarDia() == "Carnitas"):
            self.burritosSubNormal = (self.burritosVerdeCantidad + self.burritosRojoCantidad) * self.precio
            self.burritosSubEspecial = self.burritosOtroCantidad * self.precioEspecial
            self.burritosPrecioTotal = self.burritosSubEspecial + self.burritosSubNormal
        else:
            self.burritosPrecioTotal = (self.burritosVerdeCantidad + self.burritosRojoCantidad + self.burritosOtroCantidad) * self.precio
            
        self.fieldTotal.value = str(self.burritosPrecioTotal)
        self.update()

    def add_otro(self, e):
        self.burritosOtroCantidad += 1
        self.fieldOtro.value = str(self.burritosOtroCantidad)

        if(self.verificarDia() == "Pastor" or self.verificarDia() == "Carnitas"):
            self.burritosSubNormal = (self.burritosVerdeCantidad + self.burritosRojoCantidad) * self.precio
            self.burritosSubEspecial = self.burritosOtroCantidad * self.precioEspecial
            self.burritosPrecioTotal = self.burritosSubEspecial + self.burritosSubNormal
        else:
            self.burritosPrecioTotal = (self.burritosVerdeCantidad + self.burritosRojoCantidad + self.burritosOtroCantidad) * self.precio
            
        self.fieldTotal.value = str(self.burritosPrecioTotal)
        self.update()
    def remove_otro(self, e):

        if(self.burritosOtroCantidad>0):
            self.burritosOtroCantidad -= 1
            self.fieldOtro.value = str(self.burritosOtroCantidad)

        if(self.verificarDia() == "Pastor" or self.verificarDia() == "Carnitas"):
            self.burritosSubNormal = (self.burritosVerdeCantidad + self.burritosRojoCantidad) * self.precio
            self.burritosSubEspecial = self.burritosOtroCantidad * self.precioEspecial
            self.burritosPrecioTotal = self.burritosSubEspecial + self.burritosSubNormal
        else:
            self.burritosPrecioTotal = (self.burritosVerdeCantidad + self.burritosRojoCantidad + self.burritosOtroCantidad) * self.precio
            
        self.fieldTotal.value = str(self.burritosPrecioTotal)
        self.update()

    def tipo_pago_dropdown_changed(self, e):
        self.tipoPago = self.tipoPagoDropdown.value
        self.page.update()
        if(self.tipoPago=="Transferencia"):
            self.txtNumeroCuenta.visible = True
            self.page.update()
        else:
            self.txtNumeroCuenta.visible = False
            self.page.update()

    def lugar_dropdown_changed(self, e):
        self.lugar = self.lugarDropdown.value
        self.page.update()
        if(self.lugar=="Cafeteria"):
            self.lugarField.visible = False
            self.page.update()
        elif(self.lugar=="Gradas"):
            self.lugarField.visible = False
            self.page.update()
        elif(self.lugar=="En mi Aula"):
            self.lugarField.visible = False
            self.lugar = self.aula
            self.page.update()
        elif(self.lugar=="En Ingles"):
            self.lugarField.visible = False
            self.lugar = self.aula_ingles
            self.page.update()
        elif(self.lugar=="Otro"):
            self.lugarField.visible = True
            self.page.update()
        
        

    def verificarDia(self):
        nombre_dia = self.fecha_actual.strftime("%A")

        if(nombre_dia == "Monday"):
            return "Carnitas"
        elif(nombre_dia == "Tuesday"):
            return "Tinga"
        elif(nombre_dia == "Wednesday"):
            return "Desebrada"
        elif(nombre_dia == "Thursday"):
            return "Papas con picadillo"
        elif(nombre_dia == "Friday"):
            return "Pastor"
        else:
            return "Sabor del dia"
        
    def verificarCodigo(self):
        nombre_dia = self.fecha_actual.strftime("%A")

        if(nombre_dia == "Monday"):
            return 'carnitas'
        elif(nombre_dia == "Tuesday"):
            return 'tinga'
        elif(nombre_dia == "Wednesday"):
            return 'desebrada'
        elif(nombre_dia == "Thursday"):
            return 'papas_picadillo'
        elif(nombre_dia == "Friday"):
            return 'pastor'
        else:
            return 'carnitas'
        
        
             

    def click_enviar(self, e):

        self.whatsapp.enviarMensaje()

    def existencia(self, id, nombreProd, text_widget: ft.Text, btnMas : ft.IconButton, btnMenos : ft.IconButton):
        resultado = self.db.existenciaText_producto(id)
        valorExistencia = resultado[0][0]
        print(valorExistencia)
        if (valorExistencia == True):
            text_widget.value = nombreProd
        else:
            text_widget.color = ft.Colors.GREY
            text_widget.value = "Agotado"
            btnMas.bgcolor = ft.Colors.GREY
            btnMas.disabled = True
            btnMenos.disabled = True
            btnMenos.bgcolor = ft.Colors.GREY