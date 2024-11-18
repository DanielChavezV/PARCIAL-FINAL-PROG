class Respuesta:
    def __init__(self, participante, pregunta, respuesta):
        self.participante = participante
        self.pregunta = pregunta
        self.respuesta = respuesta

    def __str__(self):
        return f"Respuesta de {self.participante.nombre} a '{self.pregunta.texto}': {self.respuesta}"