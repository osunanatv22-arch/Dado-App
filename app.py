- Encabezado
- slider para número de tiradas
- Botón para re-lanzar
- Checkboxes para **histograma** y **dispersión** (cumple el requisito)
- Manejo de `session_state` para no chocar con IDs y evitar errores de keys duplicados

```python
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dado de 6 caras", page_icon="🎲", layout="centered")

# Título
st.header("🎲 Tirar un dado de 6 caras")

# Estado de la app: guardamos la última simulación para que la UI sea estable
if "rolls" not in st.session_state:
    st.session_state["rolls"] = pd.DataFrame({"tiro": [], "valor": []})

# Controles
n = st.slider("¿Cuántas tiradas?", min_value=1, max_value=5000, value=100, step=1, key="slider_tiradas")

col1, col2 = st.columns(2)
with col1:
    do_hist = st.checkbox("Mostrar histograma", value=True, key="chk_hist")
with col2:
    do_scatter = st.checkbox("Mostrar dispersión (tiro vs valor)", value=True, key="chk_scatter")

# Botón para relanzar
if st.button("🎯 Lanzar dado", key="btn_lanzar"):
    valores = np.random.randint(1, 7, size=n)  # 1..6
    st.session_state["rolls"] = pd.DataFrame({
        "tiro": np.arange(1, n + 1),
        "valor": valores
    })

# Si no hay tiradas hechas en esta sesión aún, crear una primera por defecto
if st.session_state["rolls"].empty:
    valores = np.random.randint(1, 7, size=n)
    st.session_state["rolls"] = pd.DataFrame({
        "tiro": np.arange(1, n + 1),
        "valor": valores
    })

df = st.session_state["rolls"]

# Resumen
st.subheader("Resumen")
freq = df["valor"].value_counts().sort_index()
st.write("Frecuencias por cara:")
st.dataframe(freq.rename_axis("cara").reset_index(name="frecuencia"), use_container_width=True)

# Gráficos
if do_hist:
    st.subheader("Histograma")
    fig_hist = px.histogram(df, x="valor", nbins=6, range_x=[0.5, 6.5])
    fig_hist.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig_hist, use_container_width=True)

if do_scatter:
    st.subheader("Dispersión (tiro vs valor)")
    fig_scatter = px.scatter(df, x="tiro", y="valor", range_y=[0.5, 6.5])
    fig_scatter.update_yaxes(dtick=1)
    st.plotly_chart(fig_scatter, use_container_width=True)

st.caption("Tip: usa el control de tiradas y el botón para re-lanzar.")
