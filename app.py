import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Organizador Pareja 2026", page_icon="👩‍❤️‍👨", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>👩‍❤️‍👨 Nuestro Organizador Personal</h1>", unsafe_allow_html=True)

# 2. CONEXIÓN A TU GOOGLE SHEETS
# Reemplaza con tu URL si es diferente, pero esta es la que me pasaste:
url = "https://docs.google.com/spreadsheets/d/1Zx8qzNt2DEeO2XTG6yip6jQnzVdp0TjHHjfGf5yV5KM/edit?usp=sharing"

# Creamos la conexión
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer los datos actuales
try:
    df = conn.read(spreadsheet=url, usecols=[0, 1, 2])
    df = df.dropna(how="all")
except:
    df = pd.DataFrame(columns=["Fecha", "Tarea", "Tipo"])

# 3. FORMULARIO EN LA BARRA LATERAL PARA AGREGAR TAREAS
with st.sidebar:
    st.header("📝 Nueva Tarea")
    with st.form("formulario_tareas", clear_on_submit=True):
        fecha = st.date_input("Fecha:")
        tarea = st.text_input("¿Qué hay que hacer?")
        tipo = st.selectbox("Categoría:", ["Personal", "Laboral", "Familiar", "Urgente"])
        boton_guardar = st.form_submit_button("Guardar en Calendario")

    if boton_guardar and tarea:
        # Crear nueva fila
        nueva_fila = pd.DataFrame([{"Fecha": str(fecha), "Tarea": tarea, "Tipo": tipo}])
        # Unir con los datos viejos
        df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
        # Subir a Google Sheets
        conn.update(spreadsheet=url, data=df_actualizado)
        st.success("¡Tarea guardada con éxito!")
        st.balloons()

# 4. VISUALIZACIÓN DE TAREAS POR MES
st.markdown("---")
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
mes_sel = st.selectbox("Selecciona un mes para revisar:", meses)
mes_num = meses.index(mes_sel) + 1

if not df.empty:
    # Convertir fecha a formato real para filtrar
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    filtro_mes = df[df['Fecha'].dt.month == mes_num].copy()
    
    if not filtro_mes.empty:
        filtro_mes = filtro_mes.sort_values(by="Fecha")
        # Mostrar las tareas en una lista limpia
        for index, fila in filtro_mes.iterrows():
            emoji = "🔴" if fila['Tipo'] == "Urgente" else "🔵"
            st.write(f"{emoji} **{fila['Fecha'].strftime('%d/%m')}**: {fila['Tarea']} ({fila['Tipo']})")
    else:
        st.info(f"No hay tareas anotadas para {mes_sel}.")
else:
    st.info("Aún no hay tareas en la lista. ¡Usa el panel de la izquierda!")
