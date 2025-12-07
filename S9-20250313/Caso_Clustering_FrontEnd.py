#Creación del front end
import streamlit as st
import requests

st.title("Segmentación de Clientes")
monthly_spend = st.number_input("Gasto Mensual (S/.)", min_value=5.0,max_value=200.0)
login_frequency = st.number_input("Frecuencia de Login", min_value=1,max_value=30)
support_tickets = st.number_input("Tickets de Soporte",min_value=0,max_value=10)
tenure_months = st.number_input("Antiguedad (meses)",min_value=1,max_value=48)

if st.button("Predecir Cluster"):
    response = requests.post("http://localhost:8000/predict_cluster",json={
        "Monthly_Spend":monthly_spend,
        "Login_Frequency":login_frequency,
        "Support_Tickets": support_tickets,
        "Tenure_Months":tenure_months
    })
    st.write("Cluster asignado:", response.json(["cluster"]))