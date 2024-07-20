import pandas as pd
import plotly.express as px

def crear_grafico(df):
    # Agrupar los datos por ciudad y sumar los valores totales
    df_mapa = df.groupby('ciudad').agg({
        'valor_total' : 'sum',
        'latitude': 'mean',
		'longitude': 'mean'
    }).reset_index().sort_values(by='valor_total', ascending=False)

    # Crear un gráfico de barras con los ingresos por ciudad
    graf_mapa = px.scatter_geo(df_mapa,
                       lat='latitude',
                       lon='longitude',
                       scope='south america',	
                       template='seaborn')

    return graf_mapa






#def crear_grafico(df):
#    # Agrupar los datos por ciudad y sumar los valores totales
#    df_mapa = df.groupby('ciudad').agg({
#        'valor_total': 'sum',
#        'latitude': 'mean',
#        'longitude': 'mean'
#    }).reset_index().sort_values(by='valor_total', ascending=False)
#
#    # Crear un gráfico de barras con los ingresos por ciudad
#    graf_mapa = px.scatter_geo(df_mapa,
#                               lat='latitude',
#                               lon='longitude',
#                               scope='south america',
#                               template='seaborn',
#                               hover_name='ciudad',
#                               size='valor_total',
#                               color='valor_total',
#                               color_continuous_scale=px.colors.sequential.Plasma)
#
#    return graf_mapa
