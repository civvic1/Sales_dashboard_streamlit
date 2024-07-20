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

import streamlit as st
import pandas as pd
import grafico_mapa_1 as graf1
import grafico_lineas_1 as graf2
import grafico_barras_1 as graf3
import grafico_pizza_1 as graf4

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

df_itens_pedidos = pd.read_csv('https://raw.githubusercontent.com/ElProfeAlejo/Bootcamp_Databases/main/itens_pedidos.csv')
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

df_final.head(3)

#eliminar duplicates y nan:
df_final.drop_duplicates(inplace=True)
df_final.dropna(inplace=True)
df_final.info()

preprocesamiento()



#Configuramos los filtros
st.sidebar.image('logo.png')
st.sidebar.title('Filtros')


estados = sorted(list(df_final['ciudad'].unique()))
ciudades = st.sidebar.multiselect('Estados', estados)


productos = sorted(list(df_final['producto'].dropna().unique()))
productos.insert(0, 'Todos')
producto = st.sidebar.selectbox('Productos', productos)

años = st.sidebar.checkbox('Todo el periodo', value=True)
if not años:
	año = st.sidebar.slider('Año', df_final['fecha_compra'].dt.year.min(), df_final['fecha_compra'].dt.year.max())

#Filtrando los datos
if ciudades:
	df_ventas = df_final[df_final['ciudad'].isin(ciudades)]

if producto!='Todos':
	df_final = df_final[df_final['producto'] == producto]

if not años:
	df_final = df_final[df_final['fecha_compra'].dt.year == año]

#Llamar a los gráficos
#graf_mapa = graf1.crear_grafico(df_final)
#graf_lineas = graf2.crear_grafico(df_final)
graf_barras = graf3.crear_grafico(df_final)
#graf_pizza = graf4.crear_grafico(df_final)

col1, col2 = st.columns(2)
with col1:
	st.metric('**Total de Revenues**', formata_numero(df_final['valor_total'].sum(), '$'))
	st.plotly_chart(graf_mapa, use_container_width=True)
	st.plotly_chart(graf_barras, use_container_width=True)
with col2:
	st.metric('**Total de Ventas**', formata_numero(df_final['cantidad'].sum()))
	st.plotly_chart(graf_lineas, use_container_width=True)
	st.plotly_chart(graf_pizza, use_container_width=True)
