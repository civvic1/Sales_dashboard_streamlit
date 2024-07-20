import plotly.express as px
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
#from matplotlib.patches import FancyBboxPatch
#from matplotlib.offsetbox import OffsetImage, AnnotationBbox
#import matplotlib.dates as mdates
#from matplotlib.ticker import FuncFormatter
#import matplotlib.ticker as ticker
import requests
from io import BytesIO


def generar_dataframe():

    import pandas as pd
    import os

    # Ruta del archivo CSV
    file_path = os.path.join(os.getcwd(), 'bbdd', 'pedidos.csv')

    # Imprimir la ruta absoluta del archivo para verificar
    print(f"Ruta absoluta del archivo: {file_path}")

    # Verificar si el archivo existe
    if os.path.exists(file_path):
        try:
            # Leer el archivo CSV
            df_pedidos = pd.read_csv(file_path)
            print("Archivo leído correctamente.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
    else:
        print("El archivo no existe en la ruta especificada.")









    global df_items_pedidos, df_pedidos, df_productos, df_vendedores, df_final

    #df_items_pedidos = pd.read_csv('https://raw.githubusercontent.com/ElProfeAlejo/Bootcamp_Databases/main/itens_pedidos.csv')
    df_items_pedidos = pd.read_csv('/bbdd/itens_pedidos.csv')
    df_items_pedidos.rename(columns={'ciudad': 'ISO_3166_2'},inplace=True)
    #df_pedidos = pd.read_csv('https://raw.githubusercontent.com/ElProfeAlejo/Bootcamp_Databases/main/pedidos.csv')
    df_pedidos = pd.read_csv('bbdd/pedidos.csv')
    #df_productos = pd.read_csv('https://raw.githubusercontent.com/ElProfeAlejo/Bootcamp_Databases/main/productos.csv')
    df_productos = pd.read_csv('bbdd/productos.csv')
    #df_vendedores = pd.read_csv('https://raw.githubusercontent.com/ElProfeAlejo/Bootcamp_Databases/main/vendedores.csv')
    df_vendedores = pd.read_csv('bbdd/vendedores.csv')

    dfs = [df_items_pedidos, df_pedidos, df_productos, df_vendedores]

    def preprocesamiento():
        global df_items_pedidos, df_pedidos, df_productos, df_vendedores

        # Eliminar registros con valores nulos en columnas primary o foreign key
        df_items_pedidos.dropna(subset=['pedido_id', 'producto_id'], inplace=True)
        df_pedidos.dropna(subset=['pedido_id', 'producto_id', 'vendedor_id'], inplace=True)
        df_productos.dropna(subset=['producto_id','producto'], inplace=True)### Elimino también los NaN de producto
        df_vendedores.dropna(subset=['vendedor_id'], inplace=True)

        #eliminar la fila con Vendedor='Unknown':
        df_vendedores = df_vendedores[df_vendedores['nombre_vendedor'] != 'Unknown']

        # Eliminar registros duplicados
        df_items_pedidos.drop_duplicates(inplace=True)
        df_pedidos.drop_duplicates(inplace=True)
        df_productos.drop_duplicates(inplace=True)
        df_vendedores.drop_duplicates(inplace=True)

        # Asegurar tipos de datos correctos:
        df_items_pedidos['id_recibo'] = df_items_pedidos['id_recibo'].astype(int)
        df_items_pedidos['producto_id'] = df_items_pedidos['producto_id'].astype(int)
        df_items_pedidos['pedido_id'] = df_items_pedidos['pedido_id'].astype(int)
        df_items_pedidos['ISO_3166_2'] = df_items_pedidos['ISO_3166_2'].astype(str)
        df_items_pedidos['costo_envio'] = df_items_pedidos['costo_envio'].astype(float)

        df_pedidos['pedido_id'] = df_pedidos['pedido_id'].astype(int)
        df_pedidos['producto_id'] = df_pedidos['producto_id'].astype(int)
        df_pedidos['vendedor_id'] = df_pedidos['vendedor_id'].astype(int)
        df_pedidos['fecha_compra'] = pd.to_datetime(df_pedidos['fecha_compra'])

        df_productos['producto_id'] = df_productos['producto_id'].astype(int)
        df_productos['precio'] = df_productos['precio'].astype(float)
        df_productos['sku'] = df_productos['sku'].astype(str)

        df_vendedores['vendedor_id'] = df_vendedores['vendedor_id'].astype(int)
        df_vendedores['nombre_vendedor'] = df_vendedores['nombre_vendedor'].astype(str)

        return df_items_pedidos, df_pedidos, df_productos, df_vendedores

    df_items_pedidos, df_pedidos, df_productos, df_vendedores = preprocesamiento()

    # https://drive.google.com/file/d/1HDZH0m1OMJplUg2JZrJ4slzIpuVGTxM8/view?usp=sharing
    #file_id = '1HDZH0m1OMJplUg2JZrJ4slzIpuVGTxM8'
    #url = f'https://drive.google.com/uc?export=download&id={file_id}'
    df_population = pd.read_csv('population_data.csv')
    df_population

    df_final = (
        df_items_pedidos.merge(df_pedidos, on='pedido_id')
                .drop(columns=['producto_id_y'])
                .rename(columns={'producto_id_x': 'producto_id'})
                .merge(df_productos, on='producto_id')
                .merge(df_vendedores, on='vendedor_id')
                .merge(df_population, on='ISO_3166_2')
    )
    columns=['total','precio','sku']
    df_final.drop(columns=columns,inplace=True)
    df_final['ingresos_netos'] = df_final['valor_total'] - df_final['costo_envio']
    df_final['tipo_producto'] = df_final['producto'].str.split().str[0]
    #df_final.sample(5)
    #eliminar duplicates y nan:
    df_final.drop_duplicates(inplace=True)
    df_final.dropna(inplace=True)
    df_final.valor_total.sum()
    return df_final