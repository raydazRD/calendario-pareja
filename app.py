import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import calendar

st.set_page_config(page_title="Organizador Pareja", page_icon="👩‍❤️‍👨", layout="wide")

# Estilo para el calendario
st.markdown("""
    <style>
    .calendario-tabla { width: 100%; border-collapse: collapse; table-layout: fixed; background-color: white; color: black; }
    .calendario-tabla th, .calendario-tabla td { border: 1px solid #ddd; padding: 5px; text-align: center; vertical-align: top; height: 80px; font-size: 12px; }
    .tarea-item { background-color: #e1f5fe; border-radius: 3px; padding: 2px; margin-top: 2px; font-size: 9px; color: #01579b; border-left: 2px solid #0288d1; }
    .urgente { background-color: #ffebee; color: #b71c1c; border-left: 2px solid #d32f2f; }
    </style>
    """, unsafe_allow_html=True)

st.title("👩‍❤️‍👨 Nuestro Organizador 2026")

# CONEXIÓN
url = "https://docs.google.com/spreadsheets/d/1Zx8qzNt2DEeO2XTG6yip6jQnzVdp0TjHHjfGf5yV5KM/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# LEER DATOS
try:
    df = conn.read(spreadsheet=url, ttl=0) # ttl=0 para que siempre esté actualizado
    df = df.dropna(how="all")
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
except:
    df = pd.DataFrame(columns=["Fecha", "Tarea", "Tipo"])

# FORMULARIO LATERAL
with st.sidebar:
    st.header("📝 Nueva Tarea")
    f_fecha = st.date_input("Fecha:")
    f_tarea = st.text_input("¿Qué hay que hacer?")
    f_tipo = st.selectbox("Tipo:", ["Personal", "Laboral", "Familiar", "Urgente"])
    
    if st.button("Guardar"):
        nueva = pd.DataFrame([{"Fecha": f_fecha, "Tarea": f_tarea, "Tipo": f_tipo}])
        df_new = pd.concat([df, nueva], ignore_index=True)
        conn.update(spreadsheet=url, data=df_new)
        st.success("¡Guardado! Refresca la página.")
        st.rerun()

# MOSTRAR CALENDARIO
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
sel_mes = st.selectbox("Mes:", meses, index=0)
m_num = meses.index(sel_mes) + 1

cal = calendar.monthcalendar(2026, m_num)
html = '<table class="calendario-tabla"><tr><th>Lu</th><th>Ma</th><th>Mi</th><th>Ju</th><th>Vi</th><th>Sá</th><th>Do</th></tr>'

for semana in cal:
    html += '<tr>'
    for dia in semana:
        if dia == 0:
            html += '<td></td>'
        else:
            # Buscar tareas para este día
            fecha_dia = pd.to_datetime(f"2026-{m_num}-{dia}").date()
            tareas_hoy = df[df['Fecha'] == fecha_dia]
            
            celda_contenido = f"<b>{dia}</b>"
            for _, t in tareas_hoy.iterrows():
                clase_t = "tarea-item urgente" if t['Tipo'] == "Urgente" else "tarea-item"
                celda_contenido += f'<div class="{clase_t}">{t["Tarea"]}</div>'
            
            html += f'<td>{celda_contenido}</td>'
    html += '</tr>'
html += '</table>'

st.markdown(html, unsafe_allow_html=True)
