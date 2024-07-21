import pandas as pd
import plotly.express as px

def crear_grafico(df):
	df_review = df.groupby('nombre_vendedor').agg(
		total_ventas = ('ingresos_netos', 'sum')
	).reset_index()

	colors = ['#0077b6', '#1A4D83', '#063970', '#2f567D', '#4B6A92']
	fig = px.pie(df_review,
		values = 'total_ventas',
		names = 'nombre_vendedor',
		title = 'Total de ventas por vendedor',
		color_discrete_sequence = colors
	)

	fig.update_layout(yaxis_title = 'Calificación', xaxis_title='Ventas', showlegend=False)
	fig.update_traces(textposition = 'inside', textinfo='percent+label', insidetextfont=dict(size=16), insidetextorientation='horizontal')

	return fig
