import mlflow
import mlflow.sklearn
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib
from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import HTTPBasic,HTTPBasicCredentials
import uvicorn

#Configuarar el MLFLOW en el servidor local:
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000" #si tu puerto esta ocupado, usas otro
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("Clustering_Subscribers")



#-------------------------------
#Vamos a trabajar con API para entrenar el modelo
#El API DEBE TENER SEGURIDAD
app = FastAPI()
security = HTTPBasic()
users= {"admin":"dmc_ml"}

def authenticate(credentials:HTTPBasicCredentials =Depends(security)):
    if users.get(credentials.username) != credentials.password:
        raise HTTPException(status_code=401,detail="Acceso denegado, error en pswd")
    return credentials.username



#Carga de datos:
df = pd.read_csv("Data_Clientes_Subscriptores.csv")
data = df[['Monthly_Spend','Login_Frequency','Support_Tickets','Tenure_Months']]
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)
joblib.dump(scaler,"scaler.pkl")


#Para entrenar el modelo como un API:
@app.post("/train")
def train_model(user:str =Depends(authenticate)):
    try:
        kmeans = KMeans(n_clusters=4,random_state=42,n_init=10)
        kmeans.fit(data_scaled)
        #Registrar modelo en mlflow:
        with mlflow.start_run():
            mlflow.sklearn.log_model(kmeans,"kmeans_model")
            mlflow.log_params({"n_clusters":4})
        return {"message":"Modelo entrenado y registrado en MLFLOW_Nombre"}
    except Exception as e:
        return {"error": str(e)}

#EJERCICIO: DADO ESTE CODIGO, TRASFORMAR EL CODIGO COMO UN API, PARA INVOCAR EL SERVICIO.

@app.post("/predict_cluster")
def predict_cluster(data:dict, user:str =Depends(authenticate)):
    model = mlflow.sklearn.load_model("runs:/latest/kmeans_model")
    scaler = pd.DataFrame([data])
    df_scaled = scaler.transform(df)
    prediction = model.predict(df_scaled)
    return {"cluster": int(prediction[0])}



