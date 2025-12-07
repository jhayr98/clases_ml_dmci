class Animal:
    def __init__(self, nombre, sonido): 
        self.nombre = nombre	# Atributo 
        self.sonido = sonido	# Atributo

def hablar(self):	# Método
    return f"{self.nombre} dice {self.sonido}"

# Creando un objeto de la clase Animal gato = Animal("Felix", "miau") print(gato.hablar())	# Felix dice miau


#-------------------------------------------------------------------
# Clase base o superclase 
class Animal :
    def __init__(self, nombre ): 
        self.nombre = nombre

    def presentarse(self):
        return f"Yo soy un {self.nombre }"

# Clase derivada o subclase 
class Perro(Animal ):
    def hablar (self): 
        return "Guau!"

# Uso de la clase derivada 
my_dog = Perro("Perro" )
print(my_dog .presentarse ())	# Yo soy un Perro 
print(my_dog .hablar ())	# Guau!
