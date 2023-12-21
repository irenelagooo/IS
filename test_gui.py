import pytest
import pandas as pd
from carga_guardado import leer_archivos 
from tkinter import ttk, Scrollbar, filedialog, simpledialog, messagebox
from GUI_mod import regresion_gui
from regresionsimplemultiple import bondad_ajuste, predicciones


# Prueba unitaria para la función leer_archivos
def test_leer_archivos():
    archivo_prueba = "C:\\Users\Raúl\\Desktop\\IA\\3 cuatri\\Enx Software\\P1\\housing.csv"


    datos = leer_archivos(archivo_prueba)

    # vrificar que los datos no sean None y que la longitud sea mayor a cer
    
    assert datos is not None
    assert len(datos) > 0
def test_regresion_gui():
    x_seleccionada = [1, 2, 3, 4, 5]
    y_seleccionada = [2, 4, 6, 8, 10]

    resultado = regresion_gui(x_seleccionada, y_seleccionada)

    assert resultado is not None

    assert x_seleccionada is not None
    assert y_seleccionada is not None

def recta_regresion(X, Y):
    return [0] * len(Y)

def test_bondad_ajuste():
    X = [1, 2, 3, 4, 5]
    Y = [2, 4, 6, 8, 10]

    resultado = bondad_ajuste(X, Y)
    assert resultado >= 0
    assert resultado <= 1
def test_predicciones():
    m = [1, 2, 3]
    n = 4
    x = pd.DataFrame({
        'feature1': [1.0, 2.0, 3.0],
        'feature2': [4.0, 5.0, 6.0],
        'feature3': [7.0, 8.0, 9.0]
    })

    resultado = predicciones(m, n, x)
    assert isinstance(resultado, pd.Series)
    m_string = ['a', 'b', 'c']
    with pytest.raises(TypeError):
        predicciones(m_string, n, x)

    n_string = 'not_a_float'
    with pytest.raises(TypeError):
        predicciones(m, n_string, x)

    x_not_dataframe = [1, 2, 3]
    with pytest.raises(AttributeError):
        predicciones(m, n, x_not_dataframe)