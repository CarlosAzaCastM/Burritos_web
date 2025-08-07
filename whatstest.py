import webbrowser

class WhatsTest:

    def enviarMensaje(self, nombre, burritosRojoCantidad, burritosVerdeCantidad, burritoDia, burritoDiaCantidad, lugar, tipoDePago, Total):
        telefono = "524495693298"
        mensaje = f"Hola Ángel, mi nombre es {nombre}. Quiero pedir burritos. Burritos rojo: {burritosRojoCantidad}, burritos verde: {burritosVerdeCantidad}, burritos {burritoDia}: {burritoDiaCantidad}. Estoy en {lugar}. Voy a pagar con {tipoDePago}. El total es: ${Total} pesos"
        url = f"https://wa.me/{telefono}?text={mensaje.replace(' ', '%20')}"
        webbrowser.open(url)
