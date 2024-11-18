import csv
from participante import Participante

class Estudio:
    def __init__(self, nombre, encuesta):
        self.nombre = nombre
        self.encuesta = encuesta
        self.participantes = []
        self.respuestas = []

    def agregar_participante(self, participante):
        self.participantes.append(participante)

    def agregar_respuesta(self, respuesta):
        self.respuestas.append(respuesta)

    def cargar_participantes_csv(self, archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                participante = Participante(
                    row['nombre'],
                    row['email'],
                    row['celular'],
                    int(row['edad']),
                    row['genero']
                )
                self.agregar_participante(participante)

    def generar_informe(self):
        informe = {
            'nombre_estudio': self.nombre,
            'total_participantes': len(self.participantes),
            'total_respuestas': len(self.respuestas),
            'tasa_respuesta': len(self.respuestas) / (len(self.participantes) * len(self.encuesta.preguntas)) if self.participantes and self.encuesta.preguntas else 0,
            'resultados_por_pregunta': {}
        }

        for pregunta in self.encuesta.preguntas:
            respuestas_pregunta = [r.respuesta for r in self.respuestas if r.pregunta == pregunta]
            informe['resultados_por_pregunta'][pregunta.texto] = {
                'total_respuestas': len(respuestas_pregunta),
                'respuestas': respuestas_pregunta
            }

        return informe

    def __str__(self):
        return f"Estudio: {self.nombre}\nEncuesta: {self.encuesta.titulo}\nParticipantes: {len(self.participantes)}\nRespuestas: {len(self.respuestas)}"