class Persona:
    def __init__(self, nombre, edad , nacionalidad):
        self.__nombre = nombre
        self.__edad = edad
        self.__nacionalidad = nacionalidad

    # getters: metodos para acceder a los atributos privados
    def get_nombre(self):
        return self.__nombre
    
    def get_edad(self):
        return self.__edad
    
    def get_nacionalidad(self):
        return self.__nacionalidad

    # setters: metodos para modificar a los atributos privados
    def set_nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre
    
    def get_edad(self, nuevo_edad):
        self.__edad = nuevo_edad
    
    def get_nacionalidad(self, nuevo_nacionalidad):
        self.__nacionalidad = nuevo_nacionalidad

    def hablar():
        print("Hola, estoy hablando por telefono")

class Empleado(Persona):  # <---- HERENCIA
    def __init__(self, nombre, edad, nacionalidad, trabajo, salario):
        super().__init__(nombre, edad, nacionalidad)  # Llamamos al constructor de la clase base
        self.__trabajo = trabajo
        self.__salario = salario

    # Getters y setters para los nuevos atributos privados
    def get_trabajo(self):
        return self.__trabajo

    def get_salario(self):
        return self.__salario

    def set_trabajo(self, nuevo_trabajo):
        self.__trabajo = nuevo_trabajo

    def set_salario(self, nuevo_salario):
        self.__salario = nuevo_salario

    # POLIMORFISMO: Se sobrescribe el método hablar()
    def hablar(self):
        print(f"Hola, soy {self.get_nombre()} y estoy hablando sobre mi trabajo como {self.__trabajo}.")


# Crear un objeto de la clase Empleado
empleado1 = Empleado("Daniel", 32, "Peruano", "Programador", 4500)

# Acceder a los atributos con getters
print(empleado1.get_nombre())   # Daniel
print(empleado1.get_salario())  # 4500

# Llamar al método sobrescrito (polimorfismo)
empleado1.hablar()  # Mensaje personalizado de Empleado

