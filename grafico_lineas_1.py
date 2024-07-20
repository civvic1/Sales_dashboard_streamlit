
import pandas as pd
import plotly.express as px

def crear_grafico(df):
    # Asegurarse de que la columna 'fecha_compra' sea de tipo datetime
    df['fecha_compra'] = pd.to_datetime(df['fecha_compra'])
    
    # Filtrar los datos excluyendo septiembre de 2018
    #df = df[~((df['fecha_compra'].dt.year == 2018) & (df['fecha_compra'].dt.month == 9))]
    
    # Calcular los ingresos mensuales
    revenues_monthly = df.set_index('fecha_compra').groupby(pd.Grouper(freq='M'))['valor_total'].sum().reset_index()
    revenues_monthly['Year'] = revenues_monthly['fecha_compra'].dt.year
    revenues_monthly['Month'] = revenues_monthly['fecha_compra'].dt.month_name()
    
    # Crear un diccionario para mapear los nombres de los meses a su orden
    month_order = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 
        'May': 5, 'June': 6, 'July': 7, 'August': 8, 
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    # Ordenar los datos usando el diccionario
    revenues_monthly['Month'] = pd.Categorical(revenues_monthly['Month'], categories=month_order.keys(), ordered=True)
    revenues_monthly = revenues_monthly.sort_values(by=['Year', 'Month'])
    
    # Crear el gráfico
    fig = px.line(revenues_monthly,
        x='Month',
        y='valor_total',
        markers=True,
        range_y=(0, revenues_monthly['valor_total'].max()),
        color='Year',
        line_dash='Year',
        title='Ingresos mensuales'
    )
    
    fig.update_layout(yaxis_title='Ingresos ($)')
    
    return fig

