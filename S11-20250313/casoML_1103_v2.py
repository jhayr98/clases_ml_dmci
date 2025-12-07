import os
import uvicorn
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from pycaret.classification import setup, compare_models, finalize_model, save_model, load_model

# Configuración de FastAPI
app = FastAPI()

# Ruta donde se guarda el modelo
MODEL_PATH = "ml_model"

# Cargar el modelo al iniciar la API
if os.path.exists(f"{MODEL_PATH}.pkl"):
    model = load_model(MODEL_PATH)
else:
    model = None

# Definimos el esquema de entrada para las predicciones
class ModelInput(BaseModel):
    feature1: float
    feature2: float
    feature3: float  # Puedes cambiar estos nombres por los de tu dataset

# 1️ Endpoint para entrenar el modelo
@app.get("/train")
def train_model():
    df = pd.read_csv("data.csv")  # El dataset debe estar en la misma carpeta
    setup(df, target='target', silent=True, session_id=123)
    best_model = compare_models()
    final_model = finalize_model(best_model)
    save_model(final_model, MODEL_PATH)
    return {"message": "Modelo entrenado y guardado"}

#2 Endpoint para predecir
@app.post("/predict")
def predict(data: ModelInput):
    if model is None:
        return {"error": "Modelo no entrenado"}
    
    df = pd.DataFrame([data.dict()])
    prediction = model.predict(df)
    return {"prediction": prediction.tolist()}

# 3 Ejecutar la API
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
