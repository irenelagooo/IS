import pandas as pd
from regresion import *
import sqlite3
from clase_regresion import Regresion
import matplotlib.pyplot as plt
import pickle
import tkinter as tk
from tkinter import ttk, Scrollbar, filedialog, simpledialog

def leer_archivos(path):
    '''
    Lee un archivo Excel y lo almacena en un DataFrame

    Parameters
    ----------
    path: str
        archivo con los datos a almacenar

    Returns
    -------
    df: pd.DataFrame
        DataFrame con los datos que se desean estudiar
    '''
    extension = path.split('.')[-1]
    if extension=='csv':
        df = pd.read_csv(path)
    elif extension=='xlsx':
        df = pd.read_excel(path)
    elif extension=='db':
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        df = pd.read_sql_query(f"SELECT * FROM {cursor.fetchall()[0][0]}", conn)
    return df

def guardar_regresion(m,n,R,x_seleccionadas,y_seleccionada):
    '''
    Guarda los datos de una regresión en un archivo

    Parameters
    ----------
    m: list
        lista de pendientes de la recta de regresion
    n: float
        ordenada en el origen de la recta de regresion
    R: float
        bondad del ajuste del modelo
    x_seleccionadas: list
        lista con los nombres de las variables independientes
    y_seleccionada: str
        nombre de la variable dependiente

    Returns
    -------
    None
    '''

    texto = simpledialog.askstring("Descripción", "Ingrese un texto que desee guardar con los datos de la regresión:")
    regresion=Regresion(m,n,texto,R,x_seleccionadas,y_seleccionada)
    archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    
    if archivo:
        with open(archivo,'wb') as archivo:
            pickle.dump(regresion,archivo)

def cargar_regresion(label):
    '''
    Carga los datos de una regresión desde un archivo     

    Parameters
    ----------
    label: ttk.Label
        etiqueta de la interfaz grafica donde se muestra la informacion cargada

    Returns
    -------
    Regresion: class Regresion
        objeto Regresion cargado desde el archivo
    '''

    archivo = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if archivo:
        with open(archivo, 'rb') as archivo:
            try:
                regresion = pickle.load(archivo)
                label.config(text=regresion)
            except EOFError:
                label.config(text = 'Objeto no encontrado en el archivo')
            except pickle.UnpicklingError:
                label.config(text = 'El archivo seleccionado no es correcto')
        return regresion