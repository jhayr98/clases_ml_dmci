
# Atributos, son variables que pertenecen a una clase
# Metodo, funciones dentro de la "clase". Acciones del objeto.
"""
class laptop():
    def __init__(self):
        pass # palabra reservada de paso, existe la clase laptop con metodos vacio
"""
class laptop():
    # método constructor
    def __init__(self, marca, ram, camara): # un forma de hacer referencia a si mismo
        self.marca = marca
        self.ram = ram
        self.camara = camara

    # Metodos
    def editar(self):
        print(f"Editando un documento con la laptop: {self.marca}")

    def organizar(self):
        print(f"Organizando la información con la laptop: {self.marca}")

laptop1 = laptop("Toshiba", "16gb", "4mp")
laptop2 = laptop("Hp", "8gb", "8mp")

laptop1.editar()
laptop2.organizar()

