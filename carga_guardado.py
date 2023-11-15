import pandas as pd
import numpy as np
from regresionsimplemultiple import *
import sqlite3
from claseRegresion import Regresion
import matplotlib.pyplot as plt
import pickle

def leer_archivos(path):
    '''
    Lee un archivo Excel y lo almacena en un DataFrame

    Parameters
    ----------
    path: str
        archivo con los datos a almacenar

    Returns
    -------
    df: DataFrame
        DataFrame con los datos que se desean estudiar
    '''
    extension = path.split('.')[-1]
    if extension=='csv':
        df = pd.read_csv(path)
    elif extension=='xlsx':
        df = pd.read_excel(path)
    elif extension=='db':
        # Conectarse a la base de datos SQLite
        conn = sqlite3.connect(path)

        # Crear un cursor
        cursor = conn.cursor()

        # Obtener el nombre de la tabla en la base de datos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #table_name = cursor.fetchall()[0][0]

        # Leer los datos de la tabla en un DataFrame
        df = pd.read_sql_query(f"SELECT * FROM {cursor.fetchall()[0][0]}", conn)
    return df

def print_columnas_numericas(df):
    '''
    Imprime los nombres de las columnas con datos numericos

    Parameters
    ----------
    df: DataFrame
        DataFrame con los datos que se desean estudiar

    Returns
    -------
    None
    '''
    print('//',end='')
    for columna in df.columns:
        if isinstance(df[columna].iloc[0],np.float64) or isinstance(df[columna].iloc[0],np.int64):
            print(columna,end='//')

def datos_grafica(df):
    '''
    Pide al usuario las columnas de datos con las que quiere realizar el estudio, y los datos de los que desea hacer la predicción.
    Muestra la recta de regresión, los datos de las columnas y las predicciones en una gráfica

    Parameters
    ----------
    df: DataFrame
        DataFrame con los datos que se desean estudiar

    Returns
    -------
    None
    '''
    print('Escoja una de las siguientes columnas para utilizar como variable X escribiendo su nombre por consola:')
    print_columnas_numericas(df)
    nombre_x=str(input('\nX='))
    nombre_y=str(input('Ahora escoja una variable y\nY='))
    X=pd.DataFrame({'X0':df[nombre_x]})
    Y=df[nombre_y]
    print('Desea hacer alguna predicción?')
    respuesta=int(input('Escriba 1 si la respuesta es afirmativa y 0 en caso contrario: '))
    if respuesta==1:
        pred=input('Escriba los valores de los que desea hacer la predicción separados por comas: ').split(',') #mirar espacios
        x_nuevo_df=pd.DataFrame({'X':[float(i) for i in pred]})
        x_nuevo=x_nuevo_df['X']
    else: #elif respuesta==0:???????
        x_nuevo=None

    imprimir_datos(X,Y,nombre_x,nombre_y,x_nuevo)
    plt.show()

    guardar = int(input('Desea guardar los datos de la regresión? Sí=1 No=0\n'))
    if guardar == 1:
        guardar_regresion(X,Y)

    cargar = int(input('Desea cargar una regresión? Sí=1 No=0\n'))
    if cargar == 1:
        regresion=cargar_regresion()
        print(f'La regresión cargada es la siguiente: {regresion}')

def guardar_regresion(X,Y):
    
    texto=str(input('Introduzca un texto que desee que se guarde con los datos de la regresión\n'))
    b=datos_regresion(X,Y)
    m=b[:-1]
    n=b[-1]
    bondad=bondad_ajuste(X,Y)
    regresion=Regresion(m,n,texto,bondad)
    archivo=str(input('Ingrese la ruta completa del archivo en el que desea guardar los datos\n'))
    with open(archivo,'wb') as archivo:
        pickle.dump(regresion,archivo)

#buscar contiene el nombre de la regresió que se desea cargar
def cargar_regresion():
    archivo=str(input('Ingrese la ruta completa del archivo en el que desea cargar los datos\n'))
    with open(archivo, 'rb') as archivo:
        try:
            regresion = pickle.load(archivo)
        except EOFError:
            print("Objeto no encontrado en el archivo.")
    return regresion

if __name__=='__main__':
    df=leer_archivos('C:/Users/alexe/OneDrive/Escritorio/IS/housing.db')
    datos_grafica(df)