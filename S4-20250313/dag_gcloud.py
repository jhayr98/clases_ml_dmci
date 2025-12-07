from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Configuración del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 11),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ml_pipeline_with_sklearn_numpy_pandas_joblib',
    default_args=default_args,
    description='Entrena un modelo ML usando scikit-learn, numpy, pandas y joblib en Cloud Composer',
    schedule_interval='@daily',
    catchup=False
)

# Variables de GCS
BUCKET_NAME = 'bucket-brango-dmc' #REEMPLAZAR CON EL  NOMBRE DE TU BUCKET!!!!!
#from airflow.models import Variable
#BUCKET_NAME = Variable.get("GCS_BUCKET_NAME")
MODEL_FILE = 'models/random_forest_model.pkl'

# Función para generar datos sintéticos
def generate_data():
    np.random.seed(42)
    data = {
        'feature1': np.random.rand(1000),
        'feature2': np.random.rand(1000),
        'feature3': np.random.rand(1000),
        'feature4': np.random.rand(1000),
        'target': np.random.choice([0, 1], size=1000)
    }
    df = pd.DataFrame(data)
    df.to_csv('/tmp/data.csv', index=False)

# Función para entrenar el modelo
def train_model():
    df = pd.read_csv('/tmp/data.csv')
    X = df.drop(columns=['target'])
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f'Accuracy del modelo: {accuracy:.4f}')

    #Guardar el modelo usas joblib , eso facilita su serialización
    joblib.dump(model, '/tmp/random_forest_model.pkl')

# Tarea 1: Generar datos sintéticos
generate_data_task = PythonOperator(
    task_id='generate_data',
    python_callable=generate_data,
    dag=dag
)

# Tarea 2: Entrenar modelo
train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

# Tarea 3: Subir modelo a Google Cloud Storage
upload_model_task = LocalFilesystemToGCSOperator(
    task_id='upload_model_to_gcs',
    src='/tmp/random_forest_model.pkl',
    dst=MODEL_FILE,
    bucket=BUCKET_NAME,
    mime_type='application/octet-stream',
    dag=dag
)


# Definir dependencias
generate_data_task >> train_model_task >> upload_model_task 