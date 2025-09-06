import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Leer los datos del archivo CSV
car_data = pd.read_csv('vehicles_us.csv')

st.header(' Análisis de Vehículos Usados')

# Crear casillas de verificación
hist_checkbox = st.checkbox('Mostrar histograma de odómetro')
scatter_checkbox = st.checkbox('Mostrar diagrama de dispersión (precio vs odómetro)')

# Lógica para mostrar el histograma
if hist_checkbox:
    st.write('**Histograma del Odómetro**')
    
    # Crear histograma
    fig1 = go.Figure(data=[go.Histogram(x=car_data['odometer'])])
    fig1.update_layout(
        title_text='Distribución del Odómetro',
        xaxis_title='Odómetro (millas)',
        yaxis_title='Frecuencia'
    )
    
    # Mostrar el gráfico
    st.plotly_chart(fig1, use_container_width=True)

# Lógica para mostrar el diagrama de dispersión
if scatter_checkbox:
    st.write('**Diagrama de Dispersión: Precio vs Odómetro**')
    
    # Crear diagrama de dispersión
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=car_data['odometer'], 
        y=car_data['price'],
        mode='markers',
        marker=dict(
            size=5,
            opacity=0.6,
            color='blue'
        ),
        name='Vehículos'
    ))
    
    fig2.update_layout(
        title_text='Relación entre Precio y Odómetro',
        xaxis_title='Odómetro (millas)',
        yaxis_title='Precio ($)'
    )
    
    # Mostrar el gráfico
    st.plotly_chart(fig2, use_container_width=True)