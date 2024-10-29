class Iterator():
    def __init__(self,cantidad_frases: int = 0):
        self.cantidad_frases = cantidad_frases
        self.contador: int = 1

    def incrementar_contador(self):
        if self.contador < self.cantidad_frases:
            self.contador = self.contador + 1
        elif self.contador == self.cantidad_frases:
            self.contador=1
    
    def establecer_cantidad_frases(self, cantidad_frases: int):
        self.cantidad_frases = cantidad_frases

    def mostrar_cantidad_frases(self):
        print(f"La cantidad de frases: {self.cantidad_frases}\n")

    def retornar_id(self):
        return self.contador