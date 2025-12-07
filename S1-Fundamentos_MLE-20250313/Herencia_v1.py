class Persona:
    def __init__(self, nombre, edad , nacionalidad):
        self.nombre = nombre
        self.edad = edad
        self.nacionalidad = nacionalidad

    def hablar(self):
        print("Hola, estoy hablando por telefono")


class Empleado(Persona): #<-----------------------Aqui la herencia
    pass

Empleado1 = Empleado("Daniel", "32", "Peruano")

print(Empleado1.nombre)
