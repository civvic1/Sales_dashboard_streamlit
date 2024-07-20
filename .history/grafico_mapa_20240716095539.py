#import pandas as pd
#import plotly.express as px
#
#def crear_grafico(df):
#    # Agrupar los datos por ciudad y sumar los valores totales
#    df_mapa = df.groupby('ciudad').agg({
#        'valor_total' : 'sum'
#    }).reset_index().sort_values(by='valor_total', ascending=False)
#
#    # Crear un gráfico de barras con los ingresos por ciudad
#    graf_mapa = px.bar(df_mapa,
#                       x='ciudad',
#                       y='valor_total',
#                       title='Ingresos por ciudad',
#                       labels={'ciudad': 'Ciudad', 'valor_total': 'Ingresos Totales'},
#                       template='seaborn')
#
#    return graf_mapa

import pandas as pd
import plotly.express as px

def crear_grafico_mapa(df):
    # Agrupar los datos por estado y sumar los valores totales
    df_mapa = df.groupby('ciudad').agg({
        'valor_total' : 'sum'
    }).reset_index().sort_values(by='valor_total', ascending=False)

    # Crear un gráfico de coropletas con los ingresos por estado
    graf_mapa = px.choropleth(df_mapa,
                              geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
                              locations="ciudad",
                              featureidkey="properties.sigla",
                              color="valor_total",
                              hover_name="ciudad",
                              hover_data={"ciudad": False, "valor_total": True},
                              title="Ingresos por Estado ($)",
                              color_continuous_scale="Blues",
                              scope="south america")

    graf_mapa.update_geos(fitbounds="locations", visible=False)

    return graf_mapa

# Ejemplo de uso con el dataframe final
# df_final debería ser el resultado del merge realizado anteriormente
grafico = crear_grafico_mapa(df_final)
grafico.show()

