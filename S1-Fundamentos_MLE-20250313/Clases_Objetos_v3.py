"""
Clase: 
> receta para construir un objeto
> permite definir las caracteristicas y cualidades de los objetos
> molde o plantilla para crear objetos

Objeto:
> Instancia de una clase, con sus propias características (atributos) y 
  comportamientos (métodos).

Palabra reservada:
    class, sefl
"""

class laptop():
    marca = "Toshiba"
    ram = "16gb"
    camara = "4mp"

laptop1 = laptop() #---> Se puede crear muchas laptops del mismo tipo con las mismas caracteristicas
# laptop2 = laptop(); laptop3 = laptop(); laptop4 = laptop(); ......n creaciones
print(laptop1.camara)

# es posible cambiar valores
laptop.camara = "8mp"
print(laptop1.camara)

# tal cual, no es muy practico. Lo ideal seria decirle que laptop deseo crear
# para este caso el FIJO

