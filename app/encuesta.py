class Encuesta:
    def __init__(self, titulo, descripcion):
        self.titulo = titulo
        self.descripcion = descripcion
        self.preguntas = []

    def agregar_pregunta(self, pregunta):
        self.preguntas.append(pregunta)

    def __str__(self):
        return f"Encuesta: {self.titulo}\nDescripción: {self.descripcion}\nPreguntas: {len(self.preguntas)}"