import tkinter as tk
from tkinter import ttk, Scrollbar, filedialog, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from regresionsimplemultiple import *
#from claseRegresion import Regresion
import pickle
from carga_guardado import *

def calcular_regresion_click():
    # Obtiene los nombres de las variables seleccionadas
    x_seleccionadas = [col for col, var in variables_x.items() if var.get()]
    y_seleccionadas = [col for col, var in variables_y.items() if var.get()]

    if not x_seleccionadas or not y_seleccionadas:
        resultado_label.config(text="Error: Debes seleccionar al menos una variable X e Y")

    x=pd.DataFrame()
    
    #seleccion_x = x_seleccionadas[0]
    seleccion_y = y_seleccionadas[0]
    for i in x_seleccionadas:
        nombre_variable=i
        x[nombre_variable]=mis_datos[nombre_variable]
    #x = mis_datos[seleccion_x]
    y = mis_datos[seleccion_y]

    variables_no_numericas = []
    for i in range(x.shape[1]):
        if not pd.to_numeric(x.iloc[:,i], errors='coerce').notna().all():
            variables_no_numericas.append(x_seleccionadas[i])
    if not pd.to_numeric(y, errors='coerce').notna().all():
          variables_no_numericas.append(seleccion_y)

    l = datos_regresion(x, y)
    n=l[-1]
    m=l[:-1]

    R=bondad_ajuste(x,y)
    r=formula_recta(m,n)
    resultado_label.config(text=f"Recta regresión: {r}, Bondad del ajuste: {R:.3f}")
    imprimir_datos(x,y)


    canvas = FigureCanvasTkAgg(plt.gcf(), master=canvas_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, columnspan=2, sticky="nsew") 
    window.canvas = canvas 
    '''descargar_modelo_button = ttk.Button(window, text="Descargar Modelo", command=guardar_regresion)
    descargar_modelo_button.grid(row=4, column=2, sticky="nsew")''' 

    # Ajusta las columnas y filas para expandirse
    '''window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(3, weight=1)
    window.grid_rowconfigure(5, weight=1)'''
    
    entrada_prediccion = ttk.Entry(window)
    entrada_prediccion.grid(row=2, column=2, sticky="nsew")
    etiqueta_prediccion = ttk.Label(window, text="Ingrese el valor de X para la predicción:")
    etiqueta_prediccion.grid(row=1, column=2, sticky="nsew")

    '''def llamar_guardar_regresion():
        if 'x' in locals() and 'y' in locals():
            guardar_regresion(x, y)
        else:
            resultado_label.config(text="Error: Debes calcular la regresión primero")'''

    descargar_modelo_button = ttk.Button(window, text="Descargar Modelo", command=lambda: guardar_regresion(x,y))
    descargar_modelo_button.grid(row=4, column=2, sticky="nsew")

'''def obtener_datos(path):
    extension = path.split('.')[-1]
    if extension == 'csv':
        df = pd.read_csv(path, delimiter=',') 
    elif extension == 'xlsx':
        df = pd.read_excel(path)
    return df'''

'''def cargar_archivo(ruta_label):
    archivo = filedialog.askopenfilename(filetypes=[("CSV Files", ".csv"), ("Excel Files", ".xlsx"),("DataBase Files",".db")])
    if archivo:
        ruta_label.config(text=f"Ruta del archivo: {archivo}")
        cargar_datos(archivo,variables_frame_x,variables_frame_y)'''

def cargar_datos(variables_frame_x,variables_frame_y,ruta_label):
    global mis_datos, variable_y_seleccionada, variables_x, variables_y
    
    archivo = filedialog.askopenfilename(filetypes=[("CSV Files", ".csv"), ("Excel Files", ".xlsx"),("DataBase Files",".db")])
    if archivo:
        ruta_label.config(text=f"Ruta del archivo: {archivo}")

    mis_datos = leer_archivos(archivo)

    columnas_numericas = mis_datos.select_dtypes(include='number').columns.tolist()

    variables_x = {col: tk.BooleanVar(value=False) for col in columnas_numericas}
    variables_y = {col: tk.BooleanVar(value=False) for col in columnas_numericas}
    #variable_y_seleccionada = None  # Variable para almacenar la variable Y seleccionada

    for i, col in enumerate(columnas_numericas):
        checkbutton_x = ttk.Checkbutton(variables_frame_x, text=col, variable=variables_x[col])
        checkbutton_x.grid(row=i, column=0, sticky="w")

        checkbutton_y = ttk.Checkbutton(variables_frame_y, text=col, variable=variables_y[col], command=lambda col=col: seleccionar_variable_y(col))
        checkbutton_y.grid(row=i, column=0, sticky="w")
    
def seleccionar_variable_y(col):
    global variable_y_seleccionada
    # Desmarca otras variables Y y almacena la variable Y seleccionada
    for var_col in variables_y:
        variables_y[var_col].set(False)
    variable_y_seleccionada = col
    variables_y[col].set(True)

'''def cargar_modelo(label):
    #archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    archivo = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if archivo:
        with open(archivo, 'rb') as archivo:
            try:
                
                regresion = pickle.load(archivo)
                label.config(text=regresion)
            except EOFError:
                label.config(text="Objeto no encontrado en el archivo.")
    #return regresion'''

def crear_ventana():
    window = tk.Tk()
    window.title("Calculadora de Regresión")
    # Ajustes para centrar y cambiar el tamaño de la ventana
    window_width = 800
    window_height = 600
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    return window

def variables():
    variables_frame_x = ttk.Frame(window)
    variables_frame_x.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=10,pady=10)  

    variables_frame_y = ttk.Frame(window)
    variables_frame_y.grid(row=0, column=1, rowspan=5, sticky="nsew", padx=10,pady=10)  

    variable_x_label = ttk.Label(variables_frame_x, text="Selecciona Variable(s) X:")
    variable_x_label.grid(row=0, column=0, sticky="w")

    variable_y_label = ttk.Label(variables_frame_y, text="Selecciona Variable Y:")
    variable_y_label.grid(row=0, column=0, sticky="w")
    return variables_frame_x,variables_frame_y

def texto_label_ruta():
    

    ruta_label = ttk.Label(window, text="Ruta del archivo: ")
    ruta_label.grid(row=6, columnspan=2, sticky="nsew")  # sticky para expandir en todas las direcciones
    return ruta_label

def botones(window,variables_frame_x,variables_frame_y):
    cargar_archivo_button = ttk.Button(window, text="Cargar Archivo", command=lambda: cargar_datos(variables_frame_x,variables_frame_y,ruta_label))
    cargar_archivo_button.grid(row=5, column=0, sticky="nsew")  # sticky for expanding in all directions

    cargar_modelo_button = ttk.Button(window, text="Cargar Modelo", command=lambda: cargar_modelo(resultado_label))
    cargar_modelo_button.grid(row=5, column=1, sticky="nsew")  # sticky for expanding in all directions

    calcular_button = ttk.Button(window, text="Calcular Regresión", command=calcular_regresion_click)
    calcular_button.grid(row=2, columnspan=2, sticky="nsew")  # sticky para expandir en todas las direcciones

def espacio_grafica(window):
    # Marco para el gráfico
    canvas_frame = ttk.Frame(window)
    canvas_frame.grid(row=4, columnspan=2, sticky="nsew")  # sticky para expandir en todas las direcciones
    return canvas_frame

def definir_label(window):
    resultado_label = ttk.Label(window, text="")
    resultado_label.grid(row=3, columnspan=2, sticky="nsew")  # sticky para expandir en todas las direcciones
    return resultado_label

def ajusta_ventana(window):
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(3, weight=1)
    window.grid_rowconfigure(5, weight=1)
    window.mainloop()
if __name__=='__main__':


    
    mis_datos = None  
    
    window=crear_ventana()
    # Contenedores para las variables
    variables_frame_x,variables_frame_y=variables()

    resultado_label=definir_label(window)
    '''resultado_label = ttk.Label(window, text="")
    resultado_label.grid(row=3, columnspan=2, sticky="nsew")  # sticky para expandir en todas las direcciones
    '''

    ruta_label=texto_label_ruta()
    botones(window,variables_frame_x,variables_frame_y)

    '''cargar_archivo_button = ttk.Button(window, text="Cargar Archivo", command=lambda: cargar_archivo(ruta_label))
    cargar_archivo_button.grid(row=5, columnspan=2, sticky="nsew")  # sticky para expandir en todas las direcciones'''
    '''cargar_archivo_button = ttk.Button(window, text="Cargar Archivo", command=lambda: cargar_archivo(ruta_label))
    cargar_archivo_button.grid(row=5, column=0, sticky="nsew")  # sticky for expanding in all directions

    cargar_modelo_button = ttk.Button(window, text="Cargar Modelo", command=cargar_modelo)
    cargar_modelo_button.grid(row=5, column=1, sticky="nsew")  # sticky for expanding in all directions

    calcular_button = ttk.Button(window, text="Calcular Regresión", command=calcular_regresion_click)
    calcular_button.grid(row=2, columnspan=2, sticky="nsew")  # sticky para expandir en todas las direcciones'''
    canvas_frame=espacio_grafica(window)

    # Ajusta las columnas y filas para expandirse
    ajusta_ventana(window)