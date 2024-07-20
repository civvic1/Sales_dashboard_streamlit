import streamlit as st
import pandas as pd
import grafico_mapa as graf1
import grafico_lineas as graf2
import grafico_barras as graf3
import grafico_pizza as graf4
# !pip install geobr
# import geobr
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import FancyBboxPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker
import requests
from io import BytesIO
#mostrar todas las columnas:
pd.set_option('display.max_columns', None)

global df_items_pedidos, df_pedidos, df_productos, df_vendedores, df_final
#se puede hacer en la pagina web, pero aquí lo definimos antes
st.set_page_config(layout = 'wide')

st.title('Dashboard de Ventas :shopping_trolley:')

def formata_numero(valor, prefijo = ''):
	for unidad in ['', 'k']:
		if valor<1000:
			return f'{prefijo} {valor:.2f} {unidad}'
		valor /= 1000
	return f'{prefijo} {valor:.2f} M'

#Abrimos las bases de datos
df_items_pedidos = pd.read_csv('https://raw.githubusercontent.com/ElProfeAlejo/Bootcamp_Databases/main/itens_pedidos.csv')
df_items_pedidos.rename(columns={'ciudad': 'ISO_3166_2'},inplace=True)
df_pedidos = pd.read_csv('https://raw.githubusercontent.com/ElProfeAlejo/Bootcamp_Databases/main/pedidos.csv')
df_productos = pd.read_csv('https://raw.githubusercontent.com/ElProfeAlejo/Bootcamp_Databases/main/productos.csv')
df_vendedores = pd.read_csv('https://raw.githubusercontent.com/ElProfeAlejo/Bootcamp_Databases/main/vendedores.csv')
def preprocesamiento():
    global df_items_pedidos, df_pedidos, df_productos, df_vendedores

    # Eliminar registros con valores nulos en columnas primary o foreign key
    df_items_pedidos.dropna(subset=['pedido_id', 'producto_id'], inplace=True)
    df_pedidos.dropna(subset=['pedido_id', 'producto_id', 'vendedor_id'], inplace=True)
    df_productos.dropna(subset=['producto_id','producto'], inplace=True)### Elimino también los NaN de producto
    df_vendedores.dropna(subset=['vendedor_id'], inplace=True)

    #eliminar la fila con Vendedor='Unknown':
    df_vendedores = df_vendedores[df_vendedores['nombre_vendedor'] != 'Unknown']

    # Eliminar registros duplicados
    df_items_pedidos.drop_duplicates(inplace=True)
    df_pedidos.drop_duplicates(inplace=True)
    df_productos.drop_duplicates(inplace=True)
    df_vendedores.drop_duplicates(inplace=True)

    # Asegurar tipos de datos correctos:
    df_items_pedidos['id_recibo'] = df_items_pedidos['id_recibo'].astype(int)
    df_items_pedidos['producto_id'] = df_items_pedidos['producto_id'].astype(int)
    df_items_pedidos['pedido_id'] = df_items_pedidos['pedido_id'].astype(int)
    df_items_pedidos['ISO_3166_2'] = df_items_pedidos['ISO_3166_2'].astype(str)
    df_items_pedidos['costo_envio'] = df_items_pedidos['costo_envio'].astype(float)

    df_pedidos['pedido_id'] = df_pedidos['pedido_id'].astype(int)
    df_pedidos['producto_id'] = df_pedidos['producto_id'].astype(int)
    df_pedidos['vendedor_id'] = df_pedidos['vendedor_id'].astype(int)
    df_pedidos['fecha_compra'] = pd.to_datetime(df_pedidos['fecha_compra'])

    df_productos['producto_id'] = df_productos['producto_id'].astype(int)
    df_productos['precio'] = df_productos['precio'].astype(float)
    df_productos['sku'] = df_productos['sku'].astype(str)

    df_vendedores['vendedor_id'] = df_vendedores['vendedor_id'].astype(int)
    df_vendedores['nombre_vendedor'] = df_vendedores['nombre_vendedor'].astype(str)

    return df_items_pedidos, df_pedidos, df_productos, df_vendedores

df_items_pedidos, df_pedidos, df_productos, df_vendedores = preprocesamiento()
# https://drive.google.com/file/d/1HDZH0m1OMJplUg2JZrJ4slzIpuVGTxM8/view?usp=sharing
file_id = '1HDZH0m1OMJplUg2JZrJ4slzIpuVGTxM8'
url = f'https://drive.google.com/uc?export=download&id={file_id}'
df_population = pd.read_csv(url)
df_population
df_final = (
    df_items_pedidos.merge(df_pedidos, on='pedido_id')
            .drop(columns=['producto_id_y'])
            .rename(columns={'producto_id_x': 'producto_id'})
            .merge(df_productos, on='producto_id')
            .merge(df_vendedores, on='vendedor_id')
            .merge(df_population, on='ISO_3166_2')
)
columns=['total','precio','sku']
df_final.drop(columns=columns,inplace=True)
df_final['ingresos_netos'] = df_final['valor_total'] - df_final['costo_envio']
df_final.drop_duplicates(inplace=True)
df_final.dropna(inplace=True)
df_final['valor_total'].sum()
df_final.head(3)



df_ventas = pd.read_csv('https://raw.githubusercontent.com/civvic1/Sales_dashboard_streamlit/main/base_ventas.csv')
df_ventas['valor_total'] = (df_ventas.price * df_ventas.cantidad_itens) + (df_ventas.freight_value * df_ventas.cantidad_itens)
df_ventas['order_purchase_timestamp'] = pd.to_datetime(df_ventas['order_purchase_timestamp'])
df_ventas['tipo_producto'] = df_ventas['product_category_name'].str.split('_').str[0]



#Configuramos los filtros
st.sidebar.image('logo.png')
st.sidebar.title('Filtros')



estados = sorted(list(df_ventas['geolocation_state'].unique()))
ciudades = st.sidebar.multiselect('Estados', estados)

productos = sorted(list(df_ventas['tipo_producto'].dropna().unique()))
productos.insert(0, 'Todos')
producto = st.sidebar.selectbox('Productos', productos)

años = st.sidebar.checkbox('Todo el periodo', value=True)
if not años:
	año = st.sidebar.slider('Año', df_ventas['order_purchase_timestamp'].dt.year.min(), df_ventas['order_purchase_timestamp'].dt.year.max())

#Filtrando los datos
if ciudades:
	df_ventas = df_ventas[df_ventas['geolocation_state'].isin(ciudades)]

if producto!='Todos':
	df_ventas = df_ventas[df_ventas['tipo_producto'] == producto]

if not años:
	df_ventas = df_ventas[df_ventas['order_purchase_timestamp'].dt.year == año]

#Llamar a los gráficos
graf_mapa = graf1.crear_grafico(df_ventas)
graf_lineas = graf2.crear_grafico(df_ventas)
graf_barras = graf3.crear_grafico(df_ventas)
graf_pizza = graf4.crear_grafico(df_ventas)

col1, col2 = st.columns(2)
with col1:
	st.metric('**Total de Revenues**', formata_numero(df_ventas['valor_total'].sum(), '$'))
	st.plotly_chart(graf_mapa, use_container_width=True)
	st.plotly_chart(graf_barras, use_container_width=True)
with col2:
	st.metric('**Total de Ventas**', formata_numero(df_ventas['cantidad_itens'].sum()))
	st.plotly_chart(graf_lineas, use_container_width=True)
	st.plotly_chart(graf_pizza, use_container_width=True)

