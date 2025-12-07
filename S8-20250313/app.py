#pip install streamlit requests

import streamlit as st
import requests

#URL del API en FastAPI
API_URL="http://127.0.0.1:8000/predict/"

#Interfaz de la app
st.set_page_config(page_title="Predcción de Crédito",page_icon="💰",layout="centered")

st.title("💳Predicción de Aprobación de Credito")
#Ingresando el mensaje para registrar los datos del cliente de credito
st.write("Ingresa los datos del cliente para predecir si su credito será aprobado")

#Formulario de entrada:
id_cliente = st.number_input("ID Cliente",min_value=1,step=1)
edad= st.number_input("Edad",min_value=18,max_value=100,step=1)
ingreso_mensual= st.number_input("Ingreso Mensual",min_value=0,step=100)
deuda_total=st.number_input("Deuda Total",min_value=0,step=100)
historial_crediticio = st.selectbox("Historial Crediticio", ["bueno","regular","malo"])
numero_tarjetas= st.number_input("Número de Tarjetas",min_value=0,step=1)
estado_civil= st.selectbox("Estado Civil",["soltero","casado","divorciado"])

#Boton para predecir

if st.button("📊Predecir Crédito"):
    data = {
        "id_cliente":id_cliente,
        "edad":edad,
        "ingreso_mensual":ingreso_mensual,
        "deuda_total":deuda_total,
        "historial_crediticio":historial_crediticio,
        "numero_tarjetas":numero_tarjetas,
        "estado_civil":estado_civil
    }

    try:
        response = requests.post(API_URL,json=data,auth=("admin","password123"))
        if response.status_code==200:
            prediction = response.json().get("prediction")

            #Mostrar resultados:
            if prediction==1:
                st.success("✅ Excelente! Credito aprobado.")
            else:
                st.error("❌Credito Rechazado, revisa tu historial.")
        else:
            st.error(f"Error en el API:{response.text}")
    except Exception as e:
        st.error(f"Error en la conexión:{e}")