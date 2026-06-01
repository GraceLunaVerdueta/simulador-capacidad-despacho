import streamlit as st
import pandas as pd

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
st.set_page_config(
    page_title="Simulador Supply Chain",
    layout="wide"
)

st.title("Simulador de Capacidad de Transporte")

# -----------------------------
# CARGA DE DATOS
# -----------------------------
archivo = "Abasto_Post.xlsx"

df = pd.read_excel(
    archivo,
    sheet_name="Capacidad_Despacho"
)
st.write(df["Ruta"].unique())
# -----------------------------
# SELECCIÓN DE RUTA
# -----------------------------
rutas = (
    df["Ruta"]
    .dropna()
    .astype(str)
    .unique()
)

rutas = sorted(rutas)

ruta_seleccionada = st.selectbox(
    "Seleccione una ruta",
    rutas
)

fila = df[df["Ruta"] == ruta_seleccionada].iloc[0]

# -----------------------------
# DATOS ACTUALES
# -----------------------------
req_dia = fila["Requerimiento/Dia [Paletas]"]
lt = fila["LT"]
regularizacion = fila["Regularizacion [DIA]"]

camiones_actual = fila["Camiones/dia"]

# -----------------------------
# SLIDER
# -----------------------------
camiones_simulados = st.slider(
    "Camiones por día",
    min_value=1,
    max_value=30,
    value=int(camiones_actual)
)

# -----------------------------
# CÁLCULOS
# -----------------------------

capacidad_actual = fila["Capacacidad [Paletas]"]

capacidad_nueva = (
    camiones_simulados
    * lt
    * 24
)

dp7 = req_dia * 7
dp15 = req_dia * 15

tiempo7_nuevo = (
    dp7 / capacidad_nueva
) + regularizacion

tiempo15_nuevo = (
    dp15 / capacidad_nueva
) + regularizacion

# -----------------------------
# MÉTRICAS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Requerimiento Día",
        f"{req_dia:,.0f}"
    )

with col2:
    st.metric(
        "LT",
        f"{lt}"
    )

with col3:
    st.metric(
        "Camiones actuales",
        f"{camiones_actual}"
    )

with col4:
    st.metric(
        "Camiones simulados",
        f"{camiones_simulados}"
    )

st.divider()

# -----------------------------
# RESULTADOS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Capacidad Actual",
        f"{capacidad_actual:,.0f}"
    )

with col2:
    st.metric(
        "Capacidad Simulada",
        f"{capacidad_nueva:,.0f}"
    )

with col3:
    diferencia = capacidad_nueva - capacidad_actual

    st.metric(
        "Diferencia",
        f"{diferencia:,.0f}"
    )

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Tiempo 7Dp",
        f"{tiempo7_nuevo:.2f} días"
    )

with col2:
    st.metric(
        "Tiempo 15Dp",
        f"{tiempo15_nuevo:.2f} días"
    )

# -----------------------------
# TABLA RESUMEN
# -----------------------------
st.subheader("Resumen")

resumen = pd.DataFrame({
    "Variable": [
        "Ruta",
        "LT",
        "Regularización",
        "Requerimiento Día",
        "Camiones",
        "Capacidad",
        "7Dp",
        "15Dp",
        "Tiempo 7Dp",
        "Tiempo 15Dp"
    ],
    "Valor": [
        ruta_seleccionada,
        lt,
        regularizacion,
        round(req_dia, 2),
        camiones_simulados,
        round(capacidad_nueva, 2),
        round(dp7, 2),
        round(dp15, 2),
        round(tiempo7_nuevo, 2),
        round(tiempo15_nuevo, 2)
    ]
})

st.dataframe(
    resumen,
    use_container_width=True
)
