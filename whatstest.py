import webbrowser

class WhatsTest:

    def enviarMensaje(self):
        telefono = "524495693298"
        mensaje = "Hola, quiero pedir burritos"
        url = f"https://wa.me/{telefono}?text={mensaje.replace(' ', '%20')}"
        webbrowser.open(url)
