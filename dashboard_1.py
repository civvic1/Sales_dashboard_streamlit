import streamlit as st
import pandas as pd
import grafico_mapa_1 as graf1
import grafico_lineas_1 as graf2
import grafico_barras_1 as graf3
import grafico_pizza_1 as graf4
import procesamiento as pro

# Configura la disposición de la página como 'wide' (ancha)
st.set_page_config(layout='wide')

# Título del dashboard
st.title('Dashboard de Ventas :shopping_trolley:')

# Función para formatear números con prefijo (por ejemplo, 'k' para miles, 'M' para millones)
def formata_numero(valor, prefijo=''):
    for unidad in ['', 'k']:
        if valor < 1000:
            return f'{prefijo} {valor:.2f} {unidad}'
        valor /= 1000
    return f'{prefijo} {valor:.2f} M'

# Obtener el DataFrame procesado desde "procesamiento.py"
df_final = pro.generar_dataframe()

# Configuración de los filtros en la barra lateral
st.sidebar.image('logo.png')
st.sidebar.title('Filtros')

# Crear una lista de estados únicos y ordenados para el filtro
estados = sorted(list(df_final['Estado'].unique()))
# Multiselect para filtrar por estados
ciudades = st.sidebar.multiselect('Estados', estados)

# Crear una lista de productos únicos, insertando 'Todos' al inicio para opción de no filtrar
productos = sorted(list(df_final['tipo_producto'].dropna().unique()))
productos.insert(0, 'Todos')
# Selectbox para seleccionar un producto específico
producto = st.sidebar.selectbox('Productos', productos)

# Checkbox para seleccionar todo el periodo o un año específico
años = st.sidebar.checkbox('Todo el periodo', value=True)
if not años:
    # Slider para seleccionar el año si 'Todo el periodo' no está marcado
    año = st.sidebar.slider('Año', df_final['fecha_compra'].dt.year.min(), df_final['fecha_compra'].dt.year.max())

# Aplicación de los filtros al DataFrame
if ciudades:
    # Filtrar por estados seleccionados
    df_final = df_final[df_final['Estado'].isin(ciudades)]

if producto != 'Todos':
    # Filtrar por el producto seleccionado
    df_final = df_final[df_final['tipo_producto'] == producto]

if not años:
    # Filtrar por el año seleccionado
    df_final = df_final[df_final['fecha_compra'].dt.year == año]

# Generar los gráficos con los datos filtrados
graf_mapa = graf1.crear_grafico(df_final)
graf_lineas = graf2.crear_grafico(df_final)
graf_barras = graf3.crear_grafico(df_final)
graf_pizza = graf4.crear_grafico(df_final)

# Configuración de las columnas en la página principal
col1, col2 = st.columns(2)
with col1:
    # Métrica del total de ingresos
    st.metric('**Total de Revenues**', formata_numero(df_final['valor_total'].sum(), '$'))
    # Mostrar el gráfico de mapa en la primera columna
    st.plotly_chart(graf_mapa, use_container_width=True)
    # Mostrar el gráfico de barras en la primera columna
    st.plotly_chart(graf_barras, use_container_width=True)
with col2:
    # Métrica del total de ventas
    st.metric('**Total de Ventas**', formata_numero(df_final['cantidad'].sum()))
    # Mostrar el gráfico de líneas en la segunda columna
    st.plotly_chart(graf_lineas, use_container_width=True)
    # Mostrar el gráfico de pizza en la segunda columna
    st.plotly_chart(graf_pizza, use_container_width=True)
