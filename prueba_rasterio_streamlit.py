import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Mapa Interactivo con Estadísticas", layout="wide")

# Título de la aplicación
st.title("Dashboard de Datos Geográficos")

data = {
    'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao'],
    'Latitud': [40.4168, 41.3851, 39.4699, 37.3891, 43.2630],
    'Longitud': [-3.7038, 2.1734, -0.3763, -5.9845, -2.9350],
    'Población': [3223000, 1620000, 791413, 688711, 346843],
    'Índice_Económico': [85, 82, 75, 70, 78]
}

df = pd.DataFrame(data)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Mapa Interactivo")
    
    # Crear el mapa base
    m = folium.Map(location=[40.4168, -3.7038], zoom_start=6)
    
    # Añadir marcadores al mapa
    for idx, row in df.iterrows():
        folium.CircleMarker(
            location=[row['Latitud'], row['Longitud']],
            radius=row['Población']/100000,  # Tamaño proporcional a la población
            popup=f"Ciudad: {row['Ciudad']}<br>"
                  f"Población: {row['Población']:,}<br>"
                  f"Índice Económico: {row['Índice_Económico']}",
            color='red',
            fill=True,
            fill_color='red'
        ).add_to(m)
    
    # Mostrar el mapa
    folium_static(m)

with col2:
    st.subheader("Estadísticas")
    
    # Mostrar estadísticas básicas
    st.write("Población total:", f"{df['Población'].sum():,}")
    st.write("Promedio Índice Económico:", f"{df['Índice_Económico'].mean():.1f}")
    
    # Gráfico de barras de población
    fig1 = px.bar(
        df,
        x='Ciudad',
        y='Población',
        title='Población por Ciudad'
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Gráfico de dispersión
    fig2 = px.scatter(
        df,
        x='Población',
        y='Índice_Económico',
        text='Ciudad',
        title='Relación Población vs Índice Económico'
    )
    st.plotly_chart(fig2, use_container_width=True)

# Añadir filtros en la barra lateral
st.sidebar.header("Filtros")
poblacion_min = st.sidebar.slider(
    "Población mínima",
    min_value=int(df['Población'].min()),
    max_value=int(df['Población'].max()),
    value=int(df['Población'].min())
)

indice_min = st.sidebar.slider(
    "Índice Económico mínimo",
    min_value=int(df['Índice_Económico'].min()),
    max_value=int(df['Índice_Económico'].max()),
    value=int(df['Índice_Económico'].min())
)

# Aplicar filtros
df_filtrado = df[
    (df['Población'] >= poblacion_min) &
    (df['Índice_Económico'] >= indice_min)
]

# Mostrar datos filtrados
st.subheader("Datos Filtrados")
st.dataframe(df_filtrado)