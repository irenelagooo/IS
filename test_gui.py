import pytest
import tkinter as tk
from GUI_mod import crear_ventana
import pandas as pd
from carga_guardado import leer_archivos 
from GUI_mod import regresion_gui
from regresionsimplemultiple import predicciones

@pytest.mark.parametrize("archivo",[("C:\Users\Raúl\Desktop\IA\3 cuatri\Enx Software\P1\housing.csv"),
                                        ("C:\Users\irene\Desktop\IA\ES\IS\housing.db"),
                                        ('C:/Users/alexe/OneDrive/Escritorio/IS/housing.xlsx')])

def test_leer_archivos(archivo):
   
    datos = leer_archivos(archivo)
    
    assert datos is not None
    assert len(datos) > 0

@pytest.mark.parametrize("variables_x, y_seleccionada",
                         [({'longitud':True, 'latitud': True, 'habitantes': False},tk.StringVar(value='latitud')),
                           ({'longitud':False, 'latitud': False, 'habitantes': False},tk.StringVar(value='habitantes')), 
                           ({'longitud':True, 'latitud': False, 'habitantes': False},tk.StringVar())])

def test_regresion_gui(variables_x, y_seleccionada):
    mis_datos = pd.DataFrame({'longitud': [1, 2, 223, 4616, 5],'latitud':[3,4,5,6,1],'habitantes':[100,30,40,1,0]})
    root=crear_ventana()
    variable_y=tk.StringVar()
    resultado_label=tk.Label(root)
    regresion_gui(mis_datos,variables_x, y_seleccionada,resultado_label)

    assert variable_y.get() != ''
    assert any(variables_x.values())

@pytest.mark.parametrize("m, n, x", [([1, 2, 3], 4, [4,5,4]),
    ([2, 3, 4, 7], 4, ['str',3,6,9]),
    ([1, 2], 6, [3,'*'])])

def test_predicciones(m, n, x):
    resultado = predicciones(m, n, x)
    for i in x:
        assert isinstance(i, float)
    assert isinstance(resultado, float)