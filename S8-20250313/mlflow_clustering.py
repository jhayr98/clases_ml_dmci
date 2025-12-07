import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Cargar datos
df = pd.read_csv("Mall_Customers.csv")
data = df[['Annual Income (k$)', 'Spending Score (1-100)']]

# Normalizar datos
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Encontrar el número óptimo de clusters usando el método del codo
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
    kmeans.fit(data_scaled)
    wcss.append(kmeans.inertia_)

optimal_k = 5  # Supongamos que el número óptimo de clusters es 5

# Entrenar modelo K-Means
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
kmeans.fit(data_scaled)

# Guardar modelo con MLflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")  # Usando SQLite para persistencia
mlflow.set_experiment("Clustering_Experiment")

with mlflow.start_run():
    mlflow.sklearn.log_model(kmeans, "kmeans_model")
    mlflow.log_params({"n_clusters": optimal_k})
    mlflow.log_artifact("Mall_Customers.csv")
    mlflow.end_run()

# API con FastAPI
app = FastAPI()

# Cargar el modelo desde MLflow