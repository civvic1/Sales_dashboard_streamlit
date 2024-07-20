import streamlit as st
import pandas as pd
import grafico_mapa as graf1
import grafico_lineas as graf2
import grafico_barras as graf3
import grafico_pizza as graf4

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
url = 'https://raw.githubusercontent.com/alanwillms/geoinfo/master/latitude-longitude-cidades.csv'
df_location = pd.read_csv(url, sep=';')

# Quitar el prefijo "BR-" de los registros de la columna 'ciudad' en df_itens_pedidos
df_itens_pedidos['ciudad'] = df_itens_pedidos['ciudad'].str.replace('^BR-', '', regex=True)

# Renombrar la columna 'uf' a 'ciudad' en df_location
df_location.rename(columns={'uf': 'ciudad'}, inplace=True)




def preprocesamiento():
  global df_itens_pedidos, df_pedidos, df_productos, df_vendedores, df_final, df_location
  df_itens_pedidos=pd.DataFrame(df_itens_pedidos)
  df_pedidos=pd.DataFrame(df_pedidos)
  df_productos=pd.DataFrame(df_productos)
  df_vendedores=pd.DataFrame(df_vendedores)

  # Eliminar registros con valores nulos
  df_itens_pedidos = df_itens_pedidos.dropna(subset=['id_recibo', 'producto_id','pedido_id']).reset_index(drop=True)
  df_pedidos = df_pedidos.dropna(subset=['pedido_id', 'producto_id','vendedor_id']).reset_index(drop=True)
  df_productos = df_productos.dropna(subset=['producto_id']).reset_index(drop=True)
  df_vendedores = df_vendedores.dropna(subset=['vendedor_id']).reset_index(drop=True)
  
  
  # Eliminar filas duplicadas
  df_itens_pedidos = df_itens_pedidos.drop_duplicates().reset_index(drop=True)
  df_pedidos = df_pedidos.drop_duplicates().reset_index(drop=True)
  df_productos = df_productos.drop_duplicates().reset_index(drop=True)
  df_vendedores = df_vendedores.drop_duplicates().reset_index(drop=True)

  # Convert 'fecha_compra' column to datetime
  df_pedidos['fecha_compra'] = pd.to_datetime(df_pedidos['fecha_compra'])

  # Crear un diccionario con los nombres de los estados correspondientes a las siglas
  estado_diccionario = {
      'AC': 'Acre',
      'AL': 'Alagoas',
      'AP': 'Amapá',
      'AM': 'Amazonas',
      'BA': 'Bahia',
      'CE': 'Ceará',
      'DF': 'Distrito Federal',
      'ES': 'Espírito Santo',
      'GO': 'Goiás',
      'MA': 'Maranhão',
      'MT': 'Mato Grosso',
      'MS': 'Mato Grosso do Sul',
      'MG': 'Minas Gerais',
      'PA': 'Pará',
      'PB': 'Paraíba',
      'PR': 'Paraná',
      'PE': 'Pernambuco',
      'PI': 'Piauí',
      'RJ': 'Rio de Janeiro',
      'RN': 'Rio Grande do Norte',
      'RS': 'Rio Grande do Sul',
      'RO': 'Rondônia',
      'RR': 'Roraima',
      'SC': 'Santa Catarina',
      'SP': 'São Paulo',
      'SE': 'Sergipe',
      'TO': 'Tocantins'
  }

  # Añadir la nueva columna 'state_name' utilizando el diccionario y el método map
  df_itens_pedidos['state_name'] = df_itens_pedidos['ciudad'].map(estado_diccionario)

  # Crear una nueva columna 'tipo_producto' extrayendo la primera palabra de la columna 'producto'
  df_productos['tipo_producto'] = df_productos['producto'].str.split().str[0]



  # Realizar los merges
  merged1 = pd.merge(df_itens_pedidos, df_pedidos, on=['producto_id', 'pedido_id'])
  merged2 = pd.merge(merged1, df_productos, on='producto_id')
  merged3 = pd.merge(merged2, df_location[['ciudad', 'longitude', 'latitude']], on='ciudad', how='left')
  df_final = pd.merge(merged3, df_vendedores, on='vendedor_id', how='left')




preprocesamiento()

#print(df_final.head(5))
#print("-----------")
print(df_location.head(5))

#Configuramos los filtros
st.sidebar.image('logo.png')
st.sidebar.title('Filtros')


estados = sorted(list(df_final['state_name'].unique()))
ciudades = st.sidebar.multiselect('Estados', estados)


productos = sorted(list(df_final['tipo_producto'].dropna().unique()))
productos.insert(0, 'Todos')
producto = st.sidebar.selectbox('Productos', productos)

años = st.sidebar.checkbox('Todo el periodo', value=True)
if not años:
	año = st.sidebar.slider('Año', df_final['fecha_compra'].dt.year.min(), df_final['fecha_compra'].dt.year.max())

#Filtrando los datos
if ciudades:
	df_ventas = df_final[df_final['state_name'].isin(ciudades)]

if producto!='Todos':
	df_final = df_final[df_final['tipo_producto'] == producto]

if not años:
	df_final = df_final[df_final['fecha_compra'].dt.year == año]

#Llamar a los gráficos
graf_mapa = graf1.crear_grafico(df_final)
graf_lineas = graf2.crear_grafico(df_final)
graf_barras = graf3.crear_grafico(df_final)
graf_pizza = graf4.crear_grafico(df_final)

col1, col2 = st.columns(2)
with col1:
	st.metric('**Total de Revenues**', formata_numero(df_final['valor_total'].sum(), '$'))
	st.plotly_chart(graf_mapa, use_container_width=True)
	st.plotly_chart(graf_barras, use_container_width=True)
with col2:
	st.metric('**Total de Ventas**', formata_numero(df_final['cantidad'].sum()))
	st.plotly_chart(graf_lineas, use_container_width=True)
	st.plotly_chart(graf_pizza, use_container_width=True)
