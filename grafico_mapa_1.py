import json
import pandas as pd
import plotly.express as px

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
        color_continuous_scale='viridis',
        featureidkey='properties.sigla',
        title='Ventas Totales por Estado',
        range_color=[df_ingresos_ciudad['ingresos_netos'].min(), df_ingresos_ciudad['ingresos_netos'].max()],
        hover_data={'abbrev_state': False, 'Estado': True}
    )

    # Actualizar propiedades del mapa
    fig_mapa.update_geos(
        visible=False,
        scope="south america",
        center={"lat": -14.2350, "lon": -51.9253},
        projection_scale=1.7,
        showland=False,
        showcountries=False,
        showcoastlines=False,
        showframe=False,
        showsubunits=False
    )
    fig_mapa.update_layout(
        height=850,
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

# Ejemplo de uso con un DataFrame de ejemplo
data = {
    'abbrev_state': ['SP', 'RJ', 'MG', 'BA', 'PR'],
    'Estado': ['São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Bahia', 'Paraná'],
    'ingresos_netos': [10000, 8000, 5000, 3000, 2000]
}
df = pd.DataFrame(data)

grafico = crear_grafico(df)
grafico.show()



