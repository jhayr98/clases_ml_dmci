from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pandas as pd
import mlflow
import mlflow.sklearn
from pycaret.classification import setup, compare_models, tune_model, finalize_model, save_model
import uvicorn

# Configurar MLflow con el servidor local
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Definir nombre del experimento
EXPERIMENT_NAME = "credito_experiment"
mlflow.set_experiment(EXPERIMENT_NAME)

# Configuración de FastAPI
app = FastAPI()
security = HTTPBasic()
users = {"admin": "password123"}  # Usuario para autenticación

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if users.get(credentials.username) != credentials.password:
        raise HTTPException(status_code=401, detail="Acceso denegado")
    return credentials.username

@app.get("/train")
def train_model(user: str = Depends(authenticate)):
    print("🚀 Iniciando entrenamiento del modelo...")

    try:
        # Cargar dataset
        df = pd.read_csv("dataset_credito.csv")
        print(f"✅ Dataset cargado correctamente con {df.shape[0]} filas y {df.shape[1]} columnas.")
    except Exception as e:
        print(f"❌ Error al cargar dataset: {e}")
        return {"error": str(e)}

    # Configurar PyCaret SIN log automático en MLflow
    print("🔍 Configurando PyCaret...")
    exp = setup(df, target="aprobado", log_experiment=False, session_id=123, data_split_shuffle=True)

    # Iniciar manualmente un run en MLflow
    with mlflow.start_run(run_name="Mlflow_Tracking"):
        try:
            print("🔍 Comparando modelos...")
            best_model = compare_models(n_select=1)
            tuned_model = tune_model(best_model)
            final_model = finalize_model(tuned_model)

            print("💾 Guardando modelo...")
            model_path = "credito_modelo"
            save_model(final_model, model_path)

            print("📌 Registrando modelo en MLflow...")
            mlflow.sklearn.log_model(final_model, "best_model")

            print("📊 Registrando parámetros en MLflow...")
            mlflow.log_param("session_id", 123)
            mlflow.log_param("data_split_shuffle", True)

            print("🎯 Entrenamiento finalizado con éxito")
            return {"message": "Modelo entrenado y registrado en MLflow"}
        
        except Exception as e:
            print(f"❌ Error durante el entrenamiento: {e}")
            return {"error": str(e)}

@app.post("/predict/")
def predict(data: dict, user: str = Depends(authenticate)):
    model_uri = "models:/best_model/1"
    model = mlflow.pyfunc.load_model(model_uri)
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    return {"prediction": int(prediction[0])}

@app.get("/model/version")
def get_model_version(user: str = Depends(authenticate)):
    return {"message": "Última versión registrada en MLflow: 1"}

# Iniciar FastAPI en un script .py
if __name__ == "__main__":
    uvicorn.run("mlflow3:app", host="0.0.0.0", port=8000, reload=True)