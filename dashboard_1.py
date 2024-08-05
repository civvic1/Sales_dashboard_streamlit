import streamlit as st
import pandas as pd
import grafico_mapa_1 as graf1
import grafico_lineas_1 as graf2
import grafico_barras_1 as graf3
import grafico_pizza_1 as graf4
import procesamiento as pro
import plotly.graph_objects as go

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

# Calcular el valor total inicial (sin filtros)
valor_total_inicial = df_final['valor_total'].sum()

# Configuración de los filtros en la barra lateral
st.sidebar.image('logo10.png')
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
else:
    año = None  # Se usa para indicar que no hay un año específico seleccionado

# Aplicación de los filtros al DataFrame
df_filtrado = df_final.copy()

if ciudades:
    # Filtrar por estados seleccionados
    df_filtrado = df_filtrado[df_filtrado['Estado'].isin(ciudades)]

if producto != 'Todos':
    # Filtrar por el producto seleccionado
    df_filtrado = df_filtrado[df_filtrado['tipo_producto'] == producto]

# Filtrar por año si se ha seleccionado un año específico
if año:
    df_filtrado = df_filtrado[df_filtrado['fecha_compra'].dt.year == año]
    año_actual = año
else:
    año_actual = df_filtrado['fecha_compra'].dt.year.max()

# Calcular el valor total del año actual y del año anterior usando el DataFrame original (sin filtrar)
df_año_actual = df_final[df_final['fecha_compra'].dt.year == año_actual]
df_año_anterior = df_final[df_final['fecha_compra'].dt.year == (año_actual - 1)]

valor_total_actual = df_año_actual['valor_total'].sum()
valor_total_anterior = df_año_anterior['valor_total'].sum()

# Valor total después de aplicar los filtros
valor_total_filtrado = df_filtrado['valor_total'].sum()

# Calcular el porcentaje de cambio para el valor total
if valor_total_anterior != 0:
    porcentaje_cambio_valor_total = ((valor_total_actual - valor_total_anterior) / valor_total_anterior) * 100
else:
    porcentaje_cambio_valor_total = 0

# Calcular el total de ventas (cantidad) del año actual y del año anterior
cantidad_actual = df_año_actual['cantidad'].sum()
cantidad_anterior = df_año_anterior['cantidad'].sum()

# Calcular el porcentaje de cambio para la cantidad total
if cantidad_anterior != 0:
    porcentaje_cambio_cantidad = ((cantidad_actual - cantidad_anterior) / cantidad_anterior) * 100
else:
    porcentaje_cambio_cantidad = 0

# Generar los gráficos con los datos filtrados
graf_mapa = graf1.crear_grafico(df_filtrado)
graf_lineas = graf2.crear_grafico(df_filtrado)
graf_barras = graf3.crear_grafico(df_filtrado)
graf_pizza = graf4.crear_grafico(df_filtrado)

# Configuración de las columnas en la página principal
col1, col2 = st.columns(2)
with col1:
    # Crear un contenedor para la métrica y el delta
    metric_container = st.container()
    # Formatear el valor total filtrado
    valor_formateado = formata_numero(valor_total_filtrado, '$')
    
    # Crear la métrica con el delta
    metric_container.metric(
        label="**Total de Revenues**",
        value=valor_formateado,
        delta=f"{porcentaje_cambio_valor_total:.2f}%",
        #delta_color="inverse"  # Esto hará que los valores negativos sean rojos
    )
  
    # Mostrar el gráfico de mapa en la primera columna
    st.plotly_chart(graf_mapa, use_container_width=True)
    # Mostrar el gráfico de barras en la primera columna
    st.plotly_chart(graf_barras, use_container_width=True)
with col2:
    # Crear un contenedor para la métrica y el delta de ventas
    metric_container = st.container()
    # Formatear el total de ventas filtrado
    cantidad_formateada = formata_numero(df_filtrado['cantidad'].sum(), '')
    
    # Crear la métrica con el delta
    metric_container.metric(
        label="**Total de Ventas**",
        value=cantidad_formateada,
        delta=f"{porcentaje_cambio_cantidad:.2f}%",
        #delta_color="inverse"  # Esto hará que los valores negativos sean rojos
    )

    # Mostrar el gráfico de líneas en la segunda columna
    st.plotly_chart(graf_lineas, use_container_width=True)
    # Mostrar el gráfico de pizza en la segunda columna
    st.plotly_chart(graf_pizza, use_container_width=True)
