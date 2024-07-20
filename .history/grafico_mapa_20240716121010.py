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
    # Diccionario de abreviaturas de los estados de Brasil
    estado_diccionario = {
        'BR-AC': 'Acre',
        'BR-AL': 'Alagoas',
        'BR-AP': 'Amapá',
        'BR-AM': 'Amazonas',
        'BR-BA': 'Bahia',
        'BR-CE': 'Ceará',
        'BR-DF': 'Distrito Federal',
        'BR-ES': 'Espírito Santo',
        'BR-GO': 'Goiás',
        'BR-MA': 'Maranhão',
        'BR-MT': 'Mato Grosso',
        'BR-MS': 'Mato Grosso do Sul',
        'BR-MG': 'Minas Gerais',
        'BR-PA': 'Pará',
        'BR-PB': 'Paraíba',
        'BR-PR': 'Paraná',
        'BR-PE': 'Pernambuco',
        'BR-PI': 'Piauí',
        'BR-RJ': 'Rio de Janeiro',
        'BR-RN': 'Rio Grande do Norte',
        'BR-RS': 'Rio Grande do Sul',
        'BR-RO': 'Rondônia',
        'BR-RR': 'Roraima',
        'BR-SC': 'Santa Catarina',
        'BR-SP': 'São Paulo',
        'BR-SE': 'Sergipe',
        'BR-TO': 'Tocantins'
    }
    
    # Invertir el diccionario para mapear nombres de estados a abreviaturas
    nombre_estado_diccionario = {v: k for k, v in estado_diccionario.items()}
    
    # Agregar una columna de abreviaturas al dataframe
    df['estado_abreviatura'] = df['state_name'].map(nombre_estado_diccionario)
    
    # Agrupar los datos por estado y sumar los valores totales
    df_mapa = df.groupby('estado_abreviatura').agg({
        'valor_total' : 'sum'
    }).reset_index().sort_values(by='valor_total', ascending=False)

    # Crear un gráfico de coropletas con los ingresos por estado
    graf_mapa = px.choropleth(df_mapa,
                              geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
                              locations="estado_abreviatura",
                              featureidkey="properties.sigla",
                              color="valor_total",
                              hover_name="estado_abreviatura",
                              hover_data={"estado_abreviatura": False, "valor_total": True},
                              title="Ingresos por Estado ($)",
                              color_continuous_scale="Blues",
                              scope="south america")

    graf_mapa.update_geos(fitbounds="locations", visible=False)

    return graf_mapa

# Ejemplo de uso con el dataframe final
# df_final debería ser el resultado del merge realizado anteriormente
#grafico = crear_grafico_mapa(df_final)
#grafico.show()



