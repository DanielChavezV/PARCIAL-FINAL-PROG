class Participante:
    def __init__(self, nombre, email, celular, edad, genero):
        self.nombre = nombre
        self.email = email
        self.celular = celular
        self.edad = edad
        self.genero = genero

    def __str__(self):
        return f"Participante: {self.nombre}, Email: {self.email}, Edad: {self.edad}, Género: {self.genero}"