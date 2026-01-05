import streamlit as st
import pandas as pd
import calendar
import os
from datetime import datetime

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Organizador Pareja", page_icon="👩‍❤️‍👨", layout="wide")
ARCHIVO_DATOS = "tareas.csv"

# 2. ESTILO VISUAL (CUADRÍCULA)
st.markdown("""
    <style>
    .calendario-tabla { width: 100%; border-collapse: collapse; table-layout: fixed; background-color: white; color: black; }
    .calendario-tabla th, .calendario-tabla td { border: 1px solid #444; padding: 5px; text-align: center; vertical-align: top; height: 100px; font-size: 14px; color: black; }
    .calendario-tabla th { background-color: #f0f2f6; font-weight: bold; }
    
    /* Estilo de las notitas */
    .tarea-item { 
        background-color: #e3f2fd; 
        border-left: 4px solid #2196f3; 
        padding: 2px 4px; 
        margin-top: 2px; 
        font-size: 11px; 
        text-align: left; 
        border-radius: 2px;
        color: black;
        overflow: hidden;
    }
    .urgente { background-color: #ffebee; border-left: 4px solid #f44336; color: black; }
    .laboral { background-color: #e8f5e9; border-left: 4px solid #4caf50; color: black; }
    </style>
    """, unsafe_allow_html=True)

st.title("👩‍❤️‍👨 Nuestro Organizador (Modo Local)")

# 3. CARGAR O CREAR EL ARCHIVO DE DATOS
if os.path.exists(ARCHIVO_DATOS):
    try:
        df = pd.read_csv(ARCHIVO_DATOS)
        # Aseguramos que la columna Fecha sea tipo fecha
        df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
    except:
        df = pd.DataFrame(columns=["Fecha", "Tarea", "Tipo"])
else:
    df = pd.DataFrame(columns=["Fecha", "Tarea", "Tipo"])

# 4. FORMULARIO BARRA LATERAL
with st.sidebar:
    st.header("📝 Nueva Nota")
    with st.form("form_tarea", clear_on_submit=True):
        f_fecha = st.date_input("Fecha")
        f_tarea = st.text_input("Tarea / Evento")
        f_tipo = st.selectbox("Etiqueta", ["Personal", "Laboral", "Familiar", "Urgente"])
        submitted = st.form_submit_button("Guardar Nota")
    
    if submitted and f_tarea:
        nuevo_dato = pd.DataFrame([{"Fecha": f_fecha, "Tarea": f_tarea, "Tipo": f_tipo}])
        # Unimos los datos
        df = pd.concat([df, nuevo_dato], ignore_index=True)
        # Guardamos en el archivo CSV local
        df.to_csv(ARCHIVO_DATOS, index=False)
        st.success("¡Guardado!")
        st.rerun()

# 5. DIBUJAR CALENDARIO
col1, col2 = st.columns([1, 3])
with col1:
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    sel_mes = st.selectbox("Seleccionar Mes:", meses)
    m_num = meses.index(sel_mes) + 1

# Lógica del calendario
cal = calendar.monthcalendar(2026, m_num)
html = '<table class="calendario-tabla"><thead><tr><th>Lu</th><th>Ma</th><th>Mi</th><th>Ju</th><th>Vi</th><th>Sá</th><th>Do</th></tr></thead><tbody>'

for semana in cal:
    html += '<tr>'
    for dia in semana:
        if dia == 0:
            html += '<td style="background-color: #f9f9f9;"></td>'
        else:
            # Filtrar tareas de este día
            fecha_actual = pd.to_datetime(f"2026-{m_num}-{dia}").date()
            tareas_hoy = df[df['Fecha'] == fecha_actual]
            
            contenido_celda = f"<b>{dia}</b>"
            for _, row in tareas_hoy.iterrows():
                clase_css = "tarea-item"
                if row['Tipo'] == "Urgente": clase_css += " urgente"
                if row['Tipo'] == "Laboral": clase_css += " laboral"
                
                contenido_celda += f'<div class="{clase_css}">{row["Tarea"]}</div>'
            
            html += f'<td>{contenido_celda}</td>'
    html += '</tr>'

html += '</tbody></table>'
st.markdown(html, unsafe_allow_html=True)
