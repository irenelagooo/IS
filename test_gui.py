import pytest
import tkinter as tk
from GUI_mod import crear_ventana
import pandas as pd
from carga_guardado import leer_archivos 
from GUI_mod import regresion_gui
from regresionsimplemultiple import predicciones

@pytest.mark.parametrize("archivo", [(""),
    (r"C:\Users\Raúl\Desktop\IA\3 cuatri\Enx Software\P1\housing.db"),
    (r"C:\Users\irene\Downloads\housing.csv"),
    (r"C:\Users\alexe\OneDrive\Escritorio\IS\housing.xlsx")
])

def test_leer_archivos(archivo):
    assert len(archivo)>0
    datos = leer_archivos(archivo)
    
    assert datos is not None, 'Hay que seleccionar un archivo'
    assert len(datos) > 0, 'Archivo no puede estar vacío'

@pytest.mark.parametrize("root, variables_x, y_seleccionada",
                         [(tk.Tk(), {'longitud':True, 'latitud': True, 'habitantes': False}, tk.StringVar(value='longitud')),
                           (tk.Tk(), {'longitud':False, 'latitud': False, 'habitantes': False}, tk.StringVar(value='habitantes')), 
                           (tk.Tk(), {'longitud':True, 'latitud': False, 'habitantes': False}, tk.StringVar())])

def test_regresion_gui(root,variables_x, y_seleccionada):
    mis_datos = pd.DataFrame({'longitud': [1, 2, 223, 4616, 5],'latitud':[3,4,5,6,1],'habitantes':[100,30,40,1,0]})

    resultado_label=tk.Label(root)
    assert y_seleccionada.get() != '', 'Selecciona al menos una variable Y'
    assert any(variables_x.values()), 'Selecciona al menos una variable X'
    regresion_gui(mis_datos,variables_x, y_seleccionada,resultado_label)

    

@pytest.mark.parametrize("m, n, x", [([1.3, 2.0, 3.0], 4.0, [4.8,5.0,4.0]),
    ([2.0, 3.0, 4.0, 7.0], 4.0, ['str',3.1,6.0,9.9]),
    ([1.2, 2.3], 6.1, [3.0,'*'])])

def test_predicciones(m, n, x):
    
    for i in x:
        assert isinstance(i, float), 'Las predicciones deben ser valores numéricos'
    resultado = predicciones(m, n, x)
    assert isinstance(resultado, float), 'El resultado de las predicciones debe ser numérico'

