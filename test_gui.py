import pytest
from carga_guardado import leer_archivos 
from tkinter import ttk, Scrollbar, filedialog, simpledialog, messagebox

# Prueba unitaria para la función leer_archivos
def test_leer_archivos():
    archivo_prueba = "C:\\Users\Raúl\\Desktop\\IA\\3 cuatri\\Enx Software\\P1\\housing.csv"


    datos = leer_archivos(archivo_prueba)

    # vrificar que los datos no sean None y que la longitud sea mayor a cer
    
    assert datos is not None
    assert len(datos) > 0
pytest.mark.parametrize
