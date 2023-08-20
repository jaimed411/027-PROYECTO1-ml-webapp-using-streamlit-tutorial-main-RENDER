import streamlit as st
import pandas as pd
import plotly.express as px
import random
from sklearn.linear_model import LinearRegression

# Cargar el archivo CSV
csv_path = "../models/avalanche_fatalities_22_23.csv"
data = pd.read_csv(csv_path)

# Función para predecir la cantidad de muertos
def predict_fatalities(dates, data):
    data['Date'] = pd.to_datetime(data['Date'])  # Convertir la columna de fechas a datetime
    X = data['Date'].dt.dayofyear.values.reshape(-1, 1)
    y = data['Dead'].values

    model = LinearRegression()
    model.fit(X, y)

    prediction_dates = pd.to_datetime(dates)  # Convertir las fechas de predicción a datetime
    prediction_dayofyear = prediction_dates.dayofyear.values.reshape(-1, 1)
    predictions = model.predict(prediction_dayofyear)
    
    return predictions

def main():
    '''st.title("Europe Avalanches 2022-2023")'''
    
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
    countries = ['Select'] + list(countries)
    
    st.sidebar.title("Europe avalanche fatalities 2023-2024.")
    
    selected_option = st.sidebar.radio("Select an option:", ["Predict Fatalities 2023-2024", "Fatalities 2022-2023"])
    
    if selected_option == "Fatalities 2022-2023":
        selected_country = st.sidebar.selectbox("Select a country", countries)
        
        if selected_country != 'Select':
            st.write(f"## <span style='font-size:25px'>Avalanche Fatalities in {selected_country}</span>", unsafe_allow_html=True)
            
            country_data = data[data['Country'] == selected_country]
            
            # Filtrar los datos por país seleccionado
            deaths_info = country_data.groupby('Date')['Dead'].sum().reset_index()
            
            # Mostrar mapa en la columna izquierda
            country_deaths = country_data.groupby('Country')['Dead'].sum().reset_index()
            map_fig = px.choropleth(country_deaths, locations='Country', locationmode='country names', color='Dead',
                                    color_continuous_scale='viridis', title='Total Deaths')
            # Configurar el zoom en Europa y mantener las líneas de los países
            map_fig.update_geos(
                center=dict(lon=10, lat=50),
                projection_scale=5
            )
            st.plotly_chart(map_fig, use_container_width=True)  # Utilizar el ancho de la caja desplegable
            
            # Dividir el espacio en dos columnas
            col1, col2 = st.columns([2, 1])  # Ajusta el ancho de las columnas aquí
            
            # Mostrar gráfico interactivo en la primera columna
            fig = px.line(deaths_info, x='Date', y='Dead', title='Deaths Over Time')
            fig.update_traces(mode='lines+markers', marker=dict(color='#ff4733'))  # Cambiar el color de los puntos a azul
            col1.plotly_chart(fig, use_container_width=True)  # Utilizar el ancho de la columna
            
            # Mostrar tabla en la segunda columna
            # Eliminar los índices del DataFrame antes de mostrar la tabla
            deaths_info_table = deaths_info.copy()
            deaths_info_table.index = range(1, len(deaths_info_table) + 1)
            col2.table(deaths_info_table)
    
    elif selected_option == "Predict Fatalities 2023-2024":
        st.write(" ")
        
        selected_country_for_prediction = st.selectbox("Select a country for prediction", countries)
        
        if selected_country_for_prediction != 'Select':
            country_data_for_prediction = data[data['Country'] == selected_country_for_prediction]
            
            # Calcular las predicciones para los próximos 15 días
            prediction_dates = pd.date_range(start='2023-08-19', periods=15, freq='D')
            predictions = predict_fatalities(prediction_dates, country_data_for_prediction)
            
            # Seleccionar un valor aleatorio de las predicciones
            random_prediction = random.choice(predictions)
            
            st.write(f"Predicted Fatalities in {selected_country_for_prediction} for the next 15 days: {int(random_prediction)}")
    
if __name__ == '__main__':
    main()