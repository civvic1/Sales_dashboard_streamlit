
import pandas as pd
import plotly.express as px

# Función para obtener las coordenadas de los estados de Brasil
def obtener_coordenadas_estados():
    coords = {
        'AC': {'lat': -9.974, 'lon': -67.807},
        'AL': {'lat': -9.571, 'lon': -36.646},
        'AP': {'lat': 0.902, 'lon': -52.003},
        'AM': {'lat': -3.416, 'lon': -65.856},
        'BA': {'lat': -12.970, 'lon': -38.512},
        'CE': {'lat': -3.717, 'lon': -38.543},
        'DF': {'lat': -15.793, 'lon': -47.882},
        'ES': {'lat': -19.919, 'lon': -40.367},
        'GO': {'lat': -16.686, 'lon': -49.264},
        'MA': {'lat': -2.538, 'lon': -44.282},
        'MT': {'lat': -12.642, 'lon': -55.424},
        'MS': {'lat': -20.469, 'lon': -54.620},
        'MG': {'lat': -19.815, 'lon': -43.954},
        'PA': {'lat': -1.455, 'lon': -48.502},
        'PB': {'lat': -7.239, 'lon': -35.881},
        'PR': {'lat': -25.428, 'lon': -49.273},
        'PE': {'lat': -8.047, 'lon': -34.878},
        'PI': {'lat': -5.092, 'lon': -42.803},
        'RJ': {'lat': -22.906, 'lon': -43.173},
        'RN': {'lat': -5.794, 'lon': -35.211},
        'RS': {'lat': -30.033, 'lon': -51.230},
        'RO': {'lat': -8.761, 'lon': -63.903},
        'RR': {'lat': 2.823, 'lon': -60.675},
        'SC': {'lat': -27.595, 'lon': -48.548},
        'SP': {'lat': -23.550, 'lon': -46.633},
        'SE': {'lat': -10.947, 'lon': -37.073},
        'TO': {'lat': -10.184, 'lon': -48.333}
    }
    return coords

# Función para crear el gráfico
def crear_grafico(df):
    df_mapa = df.groupby('abbrev_state').agg({'valor_total' : 'sum'}).reset_index().sort_values(by='valor_total', ascending=False)
    
    # Añadir coordenadas
    coords = obtener_coordenadas_estados()
    df_mapa['lat'] = df_mapa['abbrev_state'].apply(lambda x: coords[x]['lat'])
    df_mapa['lon'] = df_mapa['abbrev_state'].apply(lambda x: coords[x]['lon'])
    
    # Crear el gráfico
    graf_mapa = px.scatter_geo(df_mapa,
        lat='lat',
        lon='lon',
        size='valor_total',
        hover_name='Estado',
        hover_data={'abbrev_state': True, 'valor_total': True},
        title='Ingresos por estado en Brasil',
        scope='south america',
        template='seaborn'
    )

    return graf_mapa

# Ejemplo de uso con tu DataFrame
# df_final = ...  # Tu DataFrame con los datos
# grafico = crear_grafico(df_final)
# grafico.show()
