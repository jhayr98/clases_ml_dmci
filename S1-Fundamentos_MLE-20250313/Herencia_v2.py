class Persona:
    def __init__(self, nombre, edad , nacionalidad):
        self.nombre = nombre
        self.edad = edad
        self.nacionalidad = nacionalidad

    def hablar(self):
        print("Hola, estoy hablando por telefono")


class Empleado(Persona): #<-----------------------Aqui la herencia
    def __init__(self, nombre, edad, nacionalidad, trabajo, salario):
        super().__init__(nombre, edad, nacionalidad)
        self.trabajo = trabajo
        self.salario = salario

Empleado1 = Empleado("Daniel", "32", "Peruano", "programador", "4500 soles")

print(Empleado1.nombre)
print(Empleado1.salario)
Empleado1.hablar()

