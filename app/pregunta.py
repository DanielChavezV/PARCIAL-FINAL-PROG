class Pregunta:
    def __init__(self, texto, tipo):
        self.texto = texto
        self.tipo = tipo
        self.opciones = []

    def agregar_opcion(self, opcion):
        if self.tipo == "multiple":
            self.opciones.append(opcion)

    def __str__(self):
        return f"Pregunta: {self.texto} (Tipo: {self.tipo})"