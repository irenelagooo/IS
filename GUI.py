import tkinter as tk
from tkinter import ttk
from tkinter import filedialog 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from regresionsimplemultiple import *

def guardar_regresion(X,Y):
    pass
        
def borrar_grafica():
    # Verifica si hay un lienzo y lo destruye
    if hasattr(window, 'canvas'):
        window.canvas.get_tk_widget().destroy()

def calcular_regresion_click():
    borrar_grafica()
    plt.clf()
    # Obtiene los nombres de las variables seleccionadas
    x_seleccionadas = [col for col, var in variables_x.items() if var.get()]
    y_seleccionadas = [col for col, var in variables_y.items() if var.get()]

    if not x_seleccionadas or not y_seleccionadas:
        resultado_label.config(text="Error: Debes seleccionar al menos una variable X e Y")
        return

    x=pd.DataFrame()
    #seleccion_x = x_seleccionadas[0]
    seleccion_y = y_seleccionadas[0]
    for i in range(len(x_seleccionadas)):
        nombre_variable=x_seleccionadas[i]
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
    n=round(l[-1],3)
    m=[round(i,3) for i in l[:-1]]

    R=round(bondad_ajuste(x,y),3)
    resultado_label.config(text=f"Pendiente: {m}, Ordenada en el origen: {n}, Bondad del ajuste: {R}")

    imprimir_datos(x,y,x_seleccionadas,seleccion_y)

    canvas = FigureCanvasTkAgg(plt.gcf(), master=canvas_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, columnspan=2, sticky="nsew") 
    window.canvas = canvas 
    descargar_modelo_button = ttk.Button(window, text="Descargar Modelo", command=guardar_regresion)
    descargar_modelo_button.grid(row=4, column=2, sticky="nsew") 

    # Ajusta las columnas y filas para expandirse
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(3, weight=1)
    window.grid_rowconfigure(5, weight=1)
    
    entrada_prediccion = ttk.Entry(window)
    entrada_prediccion.grid(row=2, column=2, sticky="nsew")
    etiqueta_prediccion = ttk.Label(window, text="Ingrese el valor de X para la predicción:")
    etiqueta_prediccion.grid(row=1, column=2, sticky="nsew")

def obtener_datos(path):
    extension = path.split('.')[-1]
    if extension == 'csv':
        df = pd.read_csv(path, delimiter=';') 
    elif extension == 'xlsx':
        df = pd.read_excel(path)
    return df

def cargar_archivo():
    borrar_grafica()

    archivo = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
    if archivo:
        ruta_label.config(text=f"Ruta del archivo: {archivo}")
        cargar_datos(archivo)

def cargar_datos(archivo):
    global mis_datos, variable_y_seleccionada, variables_x, variables_y
    mis_datos = obtener_datos(archivo)

    columnas_numericas = mis_datos.select_dtypes(include='number').columns.tolist()

    variables_x = {col: tk.BooleanVar(value=False) for col in columnas_numericas}
    variables_y = {col: tk.BooleanVar(value=False) for col in columnas_numericas}
    variable_y_seleccionada = None  # Variable para almacenar la variable Y seleccionada

    for i, col in enumerate(columnas_numericas):
        checkbutton_x = ttk.Checkbutton(variables_frame_x, text=col, variable=variables_x[col])
        checkbutton_x.grid(row=i, column=0, sticky="w")

        checkbutton_y = ttk.Checkbutton(variables_frame_y, text=col, variable=variables_y[col], command=lambda col=col: seleccionar_variable_y(col))
        checkbutton_y.grid(row=i, column=0, sticky="w")

    columnas_no_numericas = mis_datos.select_dtypes(exclude='number').columns.tolist()

    # Solo agregar casillas de verificación para columnas numéricas
    for i, col in enumerate(columnas_no_numericas):
        if col in variables_x:
            checkbutton_x = ttk.Checkbutton(variables_frame_x, text=col, variable=variables_x[col], state='disabled')
            checkbutton_x.grid(row=i+len(columnas_numericas), column=0, sticky="w")

        if col in variables_y:
            checkbutton_y = ttk.Checkbutton(variables_frame_y, text=col, variable=variables_y[col], state='disabled')
            checkbutton_y.grid(row=i+len(columnas_numericas), column=0, sticky="w")

def seleccionar_variable_y(col):
    global variable_y_seleccionada
    # Desmarca otras variables Y y almacena la variable Y seleccionada
    for var_col in variables_y:
        variables_y[var_col].set(False)
    variable_y_seleccionada = col
    variables_y[col].set(True)


window = tk.Tk()
window.title("Calculadora de Regresión")
mis_datos = None  

# Ajustes para centrar y cambiar el tamaño de la ventana
window_width = 800
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Contenedores para las variables
variables_frame_x = ttk.Frame(window)
variables_frame_x.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=10)  # Agregado padx para espacio vertical

variables_frame_y = ttk.Frame(window)
variables_frame_y.grid(row=0, column=1, rowspan=5, sticky="nsew", padx=10)  # Agregado padx para espacio vertical

variable_x_label = ttk.Label(variables_frame_x, text="Selecciona Variable(s) X:")
variable_x_label.grid(row=0, column=0, sticky="w")

variable_y_label = ttk.Label(variables_frame_y, text="Selecciona Variable Y:")
variable_y_label.grid(row=0, column=0, sticky="w")

resultado_label = ttk.Label(window, text="")
resultado_label.grid(row=3, columnspan=2, sticky="nsew")  # sticky para expandir en todas las direcciones

ruta_label = ttk.Label(window, text="Ruta del archivo: ")
ruta_label.grid(row=6, columnspan=2, sticky="nsew")  # sticky para expandir en todas las direcciones

cargar_archivo_button = ttk.Button(window, text="Cargar Archivo", command=cargar_archivo)
cargar_archivo_button.grid(row=5, columnspan=2, sticky="nsew")  # sticky para expandir en todas las direcciones

calcular_button = ttk.Button(window, text="Calcular Regresión", command=calcular_regresion_click)
calcular_button.grid(row=2, columnspan=2, sticky="nsew")  # sticky para expandir en todas las direcciones

# Marco para el gráfico
canvas_frame = ttk.Frame(window)
canvas_frame.grid(row=4, columnspan=2, sticky="nsew")  # sticky para expandir en todas las direcciones

# Ajusta las columnas y filas para expandirse
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(3, weight=1)
window.grid_rowconfigure(5, weight=1)

window.mainloop()
