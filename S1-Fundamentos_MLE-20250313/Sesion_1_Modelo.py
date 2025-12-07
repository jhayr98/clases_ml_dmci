from sklearn.linear_model import LinearRegression
import numpy as np

class ModeloRegresion:
    def __init__(self, variables_independientes, precios):
        self.X = np.array(variables_independientes)  # Matriz de variables
        self.y = np.array(precios)  # Precios (variable dependiente)
        self.modelo = LinearRegression()  # Instancia del modelo

    def entrenar(self):
        self.modelo.fit(self.X, self.y)
        print("Modelo entrenado con éxito.")

    def predecir(self, nuevas_variables):
        return self.modelo.predict([nuevas_variables])

# Crear un objeto con datos de entrenamiento
X_entrenamiento = [[10, 5], [15, 7], [8, 3]]  # Variables (ej: peso y calidad)
y_entrenamiento = [200, 300, 150]  # Precios

modelo = ModeloRegresion(X_entrenamiento, y_entrenamiento)
modelo.entrenar()

# Predecir el precio de un nuevo producto con peso=12 y calidad=6
precio_predicho = modelo.predecir([12, 6])
print(f"Precio estimado: {precio_predicho[0]:.2f}")


###########-----------HERENCIA---------------
from sklearn.metrics import r2_score

class ModeloAvanzado(ModeloRegresion):
    def evaluar(self, X_test, y_test):
        y_pred = self.modelo.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        print(f"Precisión del modelo (R²): {r2:.2f}")

# Crear un objeto de ModeloAvanzado
modelo_avanzado = ModeloAvanzado(X_entrenamiento, y_entrenamiento)
modelo_avanzado.entrenar()

# Evaluar con nuevos datos
X_prueba = [[9, 4], [14, 6]]
y_real = [180, 280]
modelo_avanzado.evaluar(X_prueba, y_real)

###########--------ENCAPSULAMIENTO-------------
class ModeloSeguro:
    def __init__(self, variables, precios):
        self.__X = np.array(variables)
        self.__y = np.array(precios)
        self.__modelo = LinearRegression()

    def entrenar(self):
        self.__modelo.fit(self.__X, self.__y)
        print("Modelo entrenado.")

    def obtener_coeficientes(self):
        return self.__modelo.coef_

# Crear un modelo seguro
modelo_seguro = ModeloSeguro(X_entrenamiento, y_entrenamiento)
modelo_seguro.entrenar()

# Acceder a coeficientes de forma segura
print("Coeficientes del modelo:", modelo_seguro.obtener_coeficientes())


###########------------POLIMORFISMO------------
class RegresionLineal:
    def entrenar(self, X, y):
        print("Entrenando modelo de regresión lineal...")
        self.modelo = LinearRegression().fit(X, y)

class RegresionPolinomica(RegresionLineal):
    def entrenar(self, X, y):
        print("Entrenando modelo de regresión polinómica...")
        X_poli = np.column_stack((X, np.power(X, 2)))  # Agrega término cuadrático
        self.modelo = LinearRegression().fit(X_poli, y)

# Prueba de polimorfismo
modelos = [RegresionLineal(), RegresionPolinomica()]
for modelo in modelos:
    modelo.entrenar(X_entrenamiento, y_entrenamiento)


