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
df_final = pd.read_csv('df_final_limpio.csv')
#df_final['valor_total'] = df_final['valor_total'].sum()
#df_ventas['order_purchase_timestamp'] = pd.to_datetime(df_ventas['order_purchase_timestamp'])
df_final['tipo_producto'] = df_final['producto'].str.split('').str[0]

print(df_final.head(5))

#Configuramos los filtros
st.sidebar.image('logo.png')
st.sidebar.title('Filtros')



estados = sorted(list(df_final['Estado'].unique()))
ciudades = st.sidebar.multiselect('Estados', estados)

productos = sorted(list(df_final['tipo_producto'].dropna().unique()))
productos.insert(0, 'Todos')
producto = st.sidebar.selectbox('Productos', productos)

años = st.sidebar.checkbox('Todo el periodo', value=True)
if not años:
	año = st.sidebar.slider('Año', df_final['fecha_compra'].dt.year.min(), df_final['fecha_compra'].dt.year.max())

#Filtrando los datos
if ciudades:
	df_final = df_final[df_final['Estado'].isin(ciudades)]

if producto!='Todos':
	df_final = df_final[df_final['tipo_producto'] == producto]

if not años:
	df_final = df_final[df_final['fecha_compra'].dt.year == año]

#Llamar a los gráficos
graf_mapa = graf1.crear_grafico(df_final)
#graf_lineas = graf2.crear_grafico(df_ventas)
graf_barras = graf3.crear_grafico(df_final)
#graf_pizza = graf4.crear_grafico(df_ventas)

col1, col2 = st.columns(2)
with col1:
	st.metric('**Total de Revenues**', formata_numero(df_final['valor_total'].sum(), '$'))
	st.plotly_chart(graf_mapa, use_container_width=True)
	st.plotly_chart(graf_barras, use_container_width=True)
with col2:
	st.metric('**Total de Ventas**', formata_numero(df_final['cantidad'].sum()))
	#st.plotly_chart(graf_lineas, use_container_width=True)
	#st.plotly_chart(graf_pizza, use_container_width=True)
