# streamlit run main.py
import streamlit as st
import pandas as pd
from data_loader import load_data
from distance_matrix import build_distance_matrix
from vrp_model import solve_cvrp
import numpy as np
import folium
from streamlit_folium import st_folium


def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')


# Mapa con rutas
def draw_routes_on_map(df, routes):
    depot_lat = df.loc[df["id"] == 0, "lat"].values[0]
    depot_lon = df.loc[df["id"] == 0, "lon"].values[0]

    m = folium.Map(location=[depot_lat, depot_lon], zoom_start=13)

    # Puntos
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            tooltip=f'ID {row["id"]}, Demanda {row["demanda"]}'
        ).add_to(m)

    # Líneas de rutas
    colors = [
        'red', 'blue', 'green', 'purple', 'orange',
        'darkred', 'lightred', 'darkblue', 'darkgreen'
    ]

    for idx, route in enumerate(routes):
        coords = [(df.loc[df["id"] == node, "lat"].values[0],
                   df.loc[df["id"] == node, "lon"].values[0]) for node in route]

        folium.PolyLine(
            locations=coords,
            color=colors[idx % len(colors)],
            weight=5,
            popup=f"Ruta {idx}"
        ).add_to(m)

    return m



# Configuración de página
st.set_page_config(page_title="Optimizador VRP", layout="wide")

st.title("🚚 Optimizador de Rutas (CVRP)")
st.write("Carga un archivo con clientes y coordenadas para generar rutas óptimas.")


# Inicializamos session_state
if "vrp_solved" not in st.session_state:
    st.session_state.vrp_solved = False
    st.session_state.vrp_result = None
    st.session_state.vrp_df = None
    st.session_state.vrp_distance_matrix = None



# Subida del archivo
uploaded_file = st.file_uploader("Sube un archivo CSV o XLSX:", type=["csv", "xlsx"])

with st.sidebar:
    st.header("Parámetros del modelo")
    K = st.number_input("Cantidad de vehículos:", min_value=1, max_value=20, value=3)
    Q = st.number_input("Capacidad del vehículo:", min_value=1.0, value=10.0)
    time_limit = st.number_input("Time limit (segundos):", min_value=5, value=40)




#  Si se subió el archivo → procesamos
if uploaded_file is not None:

    # 1) Cargar archivo
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        df = df.sort_values("id").reset_index(drop=True)
        st.success("Archivo cargado correctamente.")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error cargando archivo: {e}")
        st.stop()

    # 2) Construir matriz de distancias
    try:
        distance_matrix = build_distance_matrix(df)
        st.info("Matriz de distancias generada correctamente.")
    except Exception as e:
        st.error(f"Error generando matriz de distancias: {e}")
        st.stop()

    # 3) Botón de optimización
    if st.button("🟩 Ejecutar optimización"):

        st.write("Ejecutando solver...")

        demands = df["demanda"].tolist()

        result = solve_cvrp(
            distance_matrix=distance_matrix,
            demands=demands,
            vehicle_count=K,
            vehicle_capacity=Q,
            time_limit=time_limit,
            solver_msg=False
        )

        # Guardamos en estado persistente
        st.session_state.vrp_solved = True
        st.session_state.vrp_result = result
        st.session_state.vrp_df = df
        st.session_state.vrp_distance_matrix = distance_matrix


#   MOSTRAR RESULTADOS
if st.session_state.vrp_solved:

    result = st.session_state.vrp_result
    df = st.session_state.vrp_df
    routes = result["routes"]

    st.success(f"Estado del solver: {result['status']}")
    st.write(f"### Distancia total = **{result['objective']:.2f} km**")

    # Tabla de rutas
    st.subheader("📋 Rutas encontradas")
    routes_data = []
    for idx, r in enumerate(routes):
        routes_data.append({
            "Vehículo": idx,
            "Ruta": " → ".join(map(str, r)),
        })
    routes_df = pd.DataFrame(routes_data)
    st.table(routes_df)

    # Mapa
    st.subheader("🗺️ Mapa de rutas")
    map_obj = draw_routes_on_map(df, routes)
    st_folium(map_obj, width=900, height=550)

    # Botón descarga CSV
    csv_data = convert_df_to_csv(routes_df)
    st.download_button(
        label="Descargar rutas (CSV)",
        data=csv_data,
        file_name="rutas_optimizadas.csv",
        mime="text/csv"
    )
