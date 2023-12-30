import pytest
import tkinter as tk
from GUI_mod import crear_ventana
import pandas as pd
from carga_guardado import leer_archivos 
from GUI_mod import calcular_regresion_click
from regresionsimplemultiple import predicciones, datos_regresion
import os

@pytest.mark.parametrize("archivo", [(""),
    (r"C:\Users\Raúl\Desktop\IA\3 cuatri\Enx Software\P1\housing.db"),
    (r"C:\Users\irene\Downloads\housing.csv"),
    (r"C:\Users\alexe\OneDrive\Escritorio\IS\housing.xlsx"),
    (r"C:\Users\TUF-F15\Desktop\2ºIA1q\ES\Trabajo ES")
])

def test_leer_archivos(archivo):
    '''
    Prueba la función leer_archivos para asegurar que la ruta del archivo o el
    archivo existan o no estén vacíos
    
    Parameters
    ----------
    archivo: str
        ruta del archivo a leer

    Returns
    -------
    None
    '''

    assert len(archivo)>0, 'Ruta del archivo vacía'
    assert os.path.exists(archivo), f'La ruta del archivo no existe: {archivo}'
    datos = leer_archivos(archivo)
    
    assert datos is not None, 'Hay que seleccionar un archivo'
    assert len(datos) > 0, 'Archivo no puede estar vacío'

@pytest.mark.parametrize("root, variables_x, y_seleccionada",
                         [(tk.Tk(), {'longitud':tk.BooleanVar(value=False), 'latitud': tk.BooleanVar(value=True), 'habitantes': tk.BooleanVar(value=True)}, tk.StringVar(value='latitud')),
                           (tk.Tk(), {'longitud':tk.BooleanVar(value=False), 'latitud': tk.BooleanVar(value=False), 'habitantes': tk.BooleanVar(value=False)}, tk.StringVar(value='habitantes')), 
                           (tk.Tk(), {'longitud':tk.BooleanVar(value=True), 'latitud': tk.BooleanVar(value=False), 'habitantes': tk.BooleanVar(value=False)}, tk.StringVar())])

def test_calcular_regresion_click(root,variables_x, y_seleccionada):
    """
    Prueba la función calcular_regresion_click para asegurar que seleccionas al menos una Y y una X

    Parameters
    ----------
    root : tk.Tk
        ventana principal de la interfaz gráfica
    variables_x: dict
        diccionario con tk.BooleanVar que indican si se seleccionó o no cada variable X
    y_seleccionada: tk.StringVar
        variable Y seleccionada

    Returns
    -------
    None
    """

    mis_datos = pd.DataFrame({'longitud': [1, 2, 223, 4616, 5],'latitud':[3,4,5,6,1],'habitantes':[100,30,40,1,0]})
    resultado_label = tk.ttk.Label(root, text="", style="Boton.TLabel")
    assert y_seleccionada.get() != '', 'Selecciona al menos una variable Y'
    assert any(var.get() for var in variables_x.values()), 'Selecciona al menos una variable X'
    calcular_regresion_click(root, mis_datos, variables_x, y_seleccionada)

    

@pytest.mark.parametrize("m, n, x", [([1.3, 2.0, 3.0], 4.0, [4.8,5.0,4.0]),
    ([2.0, 3.0, 4.0, 7.0], 4.0, ['str',3.1,6.0,9.9]),
    ([1.2, 2.3], 6.1, [3.0,'*'])])

def test_predicciones(m, n, x):
    '''
    Prueba la función predicciones para asegurar que los valores sean
    valores númericos o el resultado sea numérico

    Parameters
    ----------
    m: float
        pendiente
    n: float
        ordenada en el origen
    x: pd.series
        columna de un DataFrame con la variable X
    
    Returns
    -------
    None
    '''

    for i in x:
        assert isinstance(i, float), 'Las predicciones deben ser valores numéricos'
    resultado = predicciones(m, n, x)
    assert isinstance(resultado, float), 'El resultado de las predicciones debe ser numérico'

@pytest.mark.parametrize("X, Y", [(pd.DataFrame({'X1': [1, 2, 3], 'X2': [4, 5, 6]}), pd.Series([7, 8, 9])),
                                  (pd.DataFrame({'X1': [4, 5, 6]}), pd.Series([10, 11, 12])),
                                  (pd.DataFrame({'X1': [1, 2], 'X2': [4, 6], 'X3': [7, 9]}), pd.Series([10, 12]))])
def test_datos_regresion(X, Y):
    '''
    Prueba la función datos_regresion para asegurar que el número de pendientes y 
    el números de variables X sea el mismo, y que la ordenada en el origen es un valor numérico
    
    Parameters
    ----------
    X: pd.DataFrame
        DataFrame con las variables X
    Y: pd.series
        columna de un DataFrame con la variable Y

    Returns
    -------
    None
    '''
    
    m, n = datos_regresion(X, Y)

    assert len(m) == X.shape[1], 'Número de pendientes diferente al número de variables X'
    for i in m:
        assert isinstance(i, float), 'Cada pendiente debe ser un valor numérico'
    assert isinstance(n, float), 'Ordenada en el origen debe ser un valor numérico'