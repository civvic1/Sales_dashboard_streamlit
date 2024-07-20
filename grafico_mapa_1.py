

import json
import pandas as pd
import plotly.express as px

# Diccionario con las coordenadas centrales de cada estado de Brasil
coords_estados = {
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

def crear_grafico(df):
    # Leer el archivo JSON localmente
    file_path = 'bbdd/brazil-states.geojson'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            brazil_states_geojson = json.load(f)
        print("Archivo GeoJSON leído correctamente.")
    except Exception as e:
        print(f"Error al leer el archivo GeoJSON: {e}")
        return None

    # Agrupar los ingresos por estado
    df_ingresos_ciudad = df.groupby(['abbrev_state', 'Estado']).agg(
        ingresos_netos=('ingresos_netos', 'sum')
    ).reset_index()

    # Crear el gráfico coroplético
    fig_mapa = px.choropleth(
        df_ingresos_ciudad,
        geojson=brazil_states_geojson,
        locations='abbrev_state',
        color='ingresos_netos',
        color_continuous_scale='Blues',
        featureidkey='properties.sigla',
        title='Ventas Totales por Estado',
        range_color=[df_ingresos_ciudad['ingresos_netos'].min(), df_ingresos_ciudad['ingresos_netos'].max()],
        hover_data={'abbrev_state': False, 'Estado': True}
    )

    # Obtener el estado seleccionado
    estado_seleccionado = df_ingresos_ciudad['abbrev_state'].unique()
    
    if len(estado_seleccionado) == 1:
        # Si solo hay un estado seleccionado, centrar y acercar el mapa a ese estado
        estado = estado_seleccionado[0]
        lat_lon = coords_estados[estado]
        fig_mapa.update_geos(
            visible=False,
            scope="south america",
            center={"lat": lat_lon['lat'], "lon": lat_lon['lon']},
            projection_scale=8,  # Incrementar la escala para acercar más el estado
            showland=False,
            showcountries=False,
            showcoastlines=False,
            showframe=False,
            showsubunits=False
        )
    else:
        # Configuración por defecto para varios estados
        fig_mapa.update_geos(
            visible=False,
            scope="south america",
            center={"lat": -14.2350, "lon": -51.9253},
            projection_scale=1.3,
            showland=False,
            showcountries=False,
            showcoastlines=False,
            showframe=False,
            showsubunits=False
        )

    fig_mapa.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_showscale=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            bgcolor='rgba(0,0,0,0)',
            projection_type='mercator',
        )
    )
    fig_mapa.update_traces(
        marker_line_width=0,
        hovertemplate='<b>%{customdata[1]}</b><br>Ventas Totales: %{z}<extra></extra>'
    )

    return fig_mapa




