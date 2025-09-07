import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Leer los datos del archivo CSV
car_data = pd.read_csv('vehicles_us.csv')

st.header('📊 Análisis de Vehículos Usados')

# Crear casillas de verificación
hist_checkbox = st.checkbox('Mostrar histograma de odómetro')
scatter_checkbox = st.checkbox('Mostrar diagrama de dispersión (precio vs odómetro)')
price_hist_checkbox = st.checkbox('Mostrar histograma de precios por modelo y año')

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

# Lógica para mostrar el histograma de precios por modelo y año
if price_hist_checkbox:
    st.write('**Histograma de Precios por Modelo y Año**')
    
    # Crear filtros para el usuario
    col1, col2 = st.columns(2)
    
    with col1:
        # Selector de modelo (obtener modelos únicos, excluyendo valores nulos)
        available_models = sorted(car_data['model'].dropna().unique())
        selected_model = st.selectbox(
            'Selecciona el modelo del vehículo:',
            options=['Todos'] + list(available_models),
            index=0
        )
    
    with col2:
        # Selector de año (obtener años únicos, excluyendo valores nulos)
        available_years = sorted(car_data['model_year'].dropna().unique())
        selected_year = st.selectbox(
            'Selecciona el año del vehículo:',
            options=['Todos'] + list(available_years),
            index=0
        )
    
    # Filtrar los datos según las selecciones del usuario
    filtered_data = car_data.copy()
    
    # Aplicar filtro de modelo
    if selected_model != 'Todos':
        filtered_data = filtered_data[filtered_data['model'] == selected_model]
    
    # Aplicar filtro de año
    if selected_year != 'Todos':
        filtered_data = filtered_data[filtered_data['model_year'] == selected_year]
    
    # Verificar que hay datos después del filtrado
    if len(filtered_data) > 0:
        # Crear histograma de precios
        fig3 = go.Figure()
        
        # Añadir histograma principal
        fig3.add_trace(go.Histogram(
            x=filtered_data['price'],
            name='Distribución de Precios',
            marker_color='lightblue',
            opacity=0.7
        ))
        
        # Configurar el layout del gráfico
        title_text = 'Distribución de Precios'
        if selected_model != 'Todos' and selected_year != 'Todos':
            title_text += f' - {selected_model} ({int(selected_year)})'
        elif selected_model != 'Todos':
            title_text += f' - {selected_model}'
        elif selected_year != 'Todos':
            title_text += f' - Año {int(selected_year)}'
        
        fig3.update_layout(
            title_text=title_text,
            xaxis_title='Precio ($)',
            yaxis_title='Frecuencia',
            bargap=0.2
        )
        
        # Mostrar estadísticas básicas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de vehículos", len(filtered_data))
        with col2:
            st.metric("Precio promedio", f"${filtered_data['price'].mean():.2f}")
        with col3:
            st.metric("Precio mínimo", f"${filtered_data['price'].min():.2f}")
        with col4:
            st.metric("Precio máximo", f"${filtered_data['price'].max():.2f}")
        
        # Mostrar el gráfico
        st.plotly_chart(fig3, use_container_width=True)
        
    else:
        st.warning('⚠️ No hay datos disponibles para la combinación seleccionada de modelo y año.')

    