class Usuario:
    def __init__(self, nombre, email, rol):
        self.nombre = nombre
        self.email = email
        self.rol = rol

    def __str__(self):
        return f"Usuario: {self.nombre}, Email: {self.email}, Rol: {self.rol}"