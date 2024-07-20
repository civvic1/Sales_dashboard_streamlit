import pandas as pd
import plotly.express as px

def crear_grafico(df):
    # Agrupar los datos por ciudad y sumar los valores totales
    df_mapa = df.groupby('ciudad').agg({
        'valor_total' : 'sum'
    }).reset_index().sort_values(by='valor_total', ascending=False)

    # Crear un gráfico de barras con los ingresos por ciudad
    graf_mapa = px.bar(df_mapa,
                       x='ciudad',
                       y='valor_total',
                       title='Ingresos por ciudad',
                       labels={'ciudad': 'Ciudad', 'valor_total': 'Ingresos Totales'},
                       template='seaborn')

    return graf_mapa


