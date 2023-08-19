import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar el archivo CSV
csv_path = "../models/avalanche_fatalities_22_23.csv"
data = pd.read_csv(csv_path)

def main():
    st.title("Europe Avalanches 2022-2023")
    
    # Cambiar el color de fondo y el color del texto
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f0f0;
            color: #333333;
        }
        .expander-content {
            background-color: #007BFF;
            border-radius: 10px;
            padding: 10px;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    countries = data['Country'].unique()
    countries = ['Seleccionar'] + list(countries)
    selected_country = st.selectbox("Choose a country", countries)
    
    if selected_country != 'Seleccionar':
        st.write(f"## <span style='font-size:18px'>Avalanche Fatalities in {selected_country}</span>", unsafe_allow_html=True)
        
        country_data = data[data['Country'] == selected_country]
        
        # Filtrar los datos por país seleccionado
        deaths_info = country_data.groupby('Date')['Dead'].sum().reset_index()
        
        # Dividir el espacio en dos columnas
        col1, col2 = st.columns([2, 1])  # Ajusta el ancho de las columnas aquí
        
        # Crear una caja desplegable (expander) para el gráfico
        with col1.expander("Deaths Over Time", expanded=True):
            # Mostrar gráfico interactivo en la caja desplegable
            fig = px.line(deaths_info, x='Date', y='Dead', title='Deaths Over Time')
            st.plotly_chart(fig, use_container_width=True)  # Utilizar el ancho de la caja desplegable
        
        # Agregar un espacio entre la caja del gráfico y la tabla
        col1.empty()
        
        # Crear una caja desplegable (expander) para la tabla
        with col2.expander("Avalanche Fatalities Table", expanded=True):
            # Eliminar los índices del DataFrame antes de mostrar la tabla
            deaths_info_table = deaths_info.copy()
            deaths_info_table.index = range(1, len(deaths_info_table) + 1)
            st.table(deaths_info_table)
    
if __name__ == '__main__':
    main()
