import pandas as pd
import plotly.express as px

def crear_grafico(df):
    # Agrupar los datos por ciudad y sumar los valores totales
    df_mapa = df.groupby('ciudad').agg({
        'valor_total' : 'sum',
        'latitud': 'mean',
		'longitud': 'mean'
    }).reset_index().sort_values(by='valor_total', ascending=False)

    # Crear un gráfico de barras con los ingresos por ciudad
    graf_mapa = px.scatter(df_mapa,
                       lat='latitude',
                       lon='longitude',
                       scope='south america ',
					   size='valor_total'	
                       title='Ingresos por ciudad',
                       labels={'ciudad': 'Ciudad', 'valor_total': 'Ingresos Totales'},
                       template='seaborn')

    return graf_mapa





#import pandas as pd
#import plotly.express as px
#def crear_grafico(df):
#	df_mapa = df.groupby('state_name').agg({
#		'valor_total' : 'sum',
#		'geolocation_lat': 'mean',
#		'geolocation_lng': 'mean'
#	}).reset_index().sort_values(by='valor_total', ascending=False)
#
#	graf_mapa = px.scatter_geo(df_mapa,
#		lat = 'geolocation_lat',
#		lon = 'geolocation_lng',
#		scope = 'south america',
#		template = 'seaborn',
#		size = 'valor_total',
#		hover_name = 'geolocation_state',
#		hover_data = {'geolocation_lat':False, 'geolocation_lng':False},
#		title = 'Ingresos por estado',
#	)
#
#	return graf_mapa