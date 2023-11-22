import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import tkinter as tk
from tkinter import ttk, Scrollbar, filedialog, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from regresionsimplemultiple import *
from claseRegresion import Regresion
import pickle


# Función para cargar los datos y mostrarlos en una tabla
def cargar_datos(archivo):
    global mis_datos

    mis_datos = obtener_datos(archivo)
    if not mis_datos.index.name:  
        mis_datos.index.name = 'Índice'
        mis_datos.reset_index(inplace=True)

    # Actualizar etiqueta de la ruta
    ruta_label.config(text=f"Ruta: {archivo}")

    # Crear un Frame para la tabla
    frame_tabla = tk.Frame(root)
    frame_tabla.pack(pady=10, padx=20)

    # Crear un Treeview para mostrar la tabla
    treeview = ttk.Treeview(frame_tabla)
    treeview["columns"] = tuple(mis_datos.columns)

    # Configurar encabezados
    for column in mis_datos.columns:
        treeview.heading(column, text=column)

    # Insertar datos
    for i, row in mis_datos.iterrows():
        treeview.insert("", i, values=tuple(row))
    for col in mis_datos.columns:
        treeview.heading(col, text=col, anchor='center')  # Encabezados centrados
        treeview.column(col, anchor='center', width=150)  # Datos centrados en las columnas

    if 'Índice' in mis_datos.columns:
        treeview.heading('Índice', text='Índice', anchor='center')
        treeview.column('Índice', anchor='center', width=50)
        
    
    treeview.heading('#0', text='', anchor='center')  # Encabezado centrado
    treeview.column('#0', width=0, anchor='center')  # Ajusta el ancho según sea necesario

    # Agregar barras de desplazamiento vertical y horizontal dentro del Treeview
    yscroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=treeview.yview)
    yscroll.pack(side="right", fill="y")
    treeview.configure(yscrollcommand=yscroll.set)

    xscroll = ttk.Scrollbar(frame_tabla, orient="horizontal", command=treeview.xview)
    xscroll.pack(side="bottom", fill="x")
    treeview.configure(xscrollcommand=xscroll.set)

    # Centrar la tabla en el Frame
    treeview.pack()

 
    def calcular_regresion():
        pass
    boton_calculo = ttk.Button(root, text="Calcular Regresión", command=calcular_regresion)
    boton_calculo.place(x=700, y=325)
    

    # Etiquetas para seleccionar variables X e Y
    seleccionar_var_x_label = tk.Label(root, text="Selecciona variable(s) X")
    seleccionar_var_x_label.place(x=100, y=300)

 
    # Crear un canvas para las variables X
    canvas_x = tk.Canvas(root, bd=0, highlightthickness=0)
    canvas_x.place(x=300, y=300)

    # Frame para contener las variables X
    variables_frame_x = tk.Frame(canvas_x)
    scrollbar_x = ttk.Scrollbar(root, orient="horizontal", command=canvas_x.xview)
    scrollbar_x.place(x=300, y=325, width=400)
    canvas_x.configure(xscrollcommand=scrollbar_x.set)

    # Establecer el tamaño del canvas
    variables_frame_x.bind("<Configure>", lambda e: canvas_x.configure(scrollregion=canvas_x.bbox("all")))

    # Colocar el frame dentro del canvas
    canvas_x.create_window((0, 0), window=variables_frame_x, anchor="nw")

    columnas_numericas = mis_datos.select_dtypes(include='number').columns.tolist()
    global variables_x
    variables_x = {col: tk.BooleanVar(value=False) for col in columnas_numericas}

    for col in columnas_numericas:
        # Verificar si la columna es el índice
        if col != 'Índice':
            checkbutton_x = ttk.Checkbutton(variables_frame_x, text=col, variable=variables_x[col])
            checkbutton_x.pack(side=tk.LEFT)

    # Etiqueta para seleccionar variable Y
    seleccionar_var_y_label = tk.Label(root, text="Selecciona variable Y:")
    seleccionar_var_y_label.place(x=100, y=350)

    # Crear un canvas para las variables Y
    canvas_y = tk.Canvas(root, bd=0, highlightthickness=0)
    canvas_y.place(x=300, y=350)

    # Frame para contener las variables Y
    variables_frame_y = tk.Frame(canvas_y)
    scrollbar_y = ttk.Scrollbar(root, orient="horizontal", command=canvas_y.xview)
    scrollbar_y.place(x=300, y=375, width=400)
    canvas_y.configure(xscrollcommand=scrollbar_y.set)

    # Establecer el tamaño del canvas
    variables_frame_y.bind("<Configure>", lambda e: canvas_y.configure(scrollregion=canvas_y.bbox("all")))

    # Colocar el frame dentro del canvas
    canvas_y.create_window((0, 0), window=variables_frame_y, anchor="nw")

    columnas_numericas_y = mis_datos.select_dtypes(include='number').columns.tolist()

    def seleccionar_variable_y(variable):
        global variable_y_seleccionada
        variable_y_seleccionada = variable

    variable_y_seleccionada_radio = tk.StringVar()
    for col in columnas_numericas_y:
        if col != 'Índice':
            radio_y = ttk.Radiobutton(variables_frame_y, text=col, variable=variable_y_seleccionada_radio, value=col,
                                      command=lambda col=col: seleccionar_variable_y(col))
            radio_y.pack(side=tk.LEFT)

# Función para cargar un archivo
def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("CSV Files", ".csv"), ("Excel Files", ".xlsx")])
    if archivo:
        cargar_datos(archivo)
        # Mostrar botones después de cargar el archivo
        cargar_archivo_btn.place(x=680,y=7)
        cargar_modelo_btn.place(x=800,y=7)

# Función para obtener los datos del archivo
def obtener_datos(path):
    extension = path.split('.')[-1]
    if extension == 'csv':
        df = pd.read_csv(path, delimiter=',') 
    elif extension == 'xlsx':
        df = pd.read_excel(path)
    return df
'''def borrar_grafica():
    # Verifica si hay un lienzo y lo destruye
    if hasattr(window, 'canvas'):
        window.canvas.get_tk_widget().destroy()'''


# Configuración de la root principal
root = tk.Tk()
root.title("Interfaz de Datos")

# Obtener dimensiones de la pantalla
ancho_pantalla = root.winfo_screenwidth()
altura_pantalla = root.winfo_screenheight()

# Definir tamaño y posición de la root
ancho_root = ancho_pantalla // 2
altura_root = altura_pantalla - 100

x_pos = ancho_pantalla // 4
y_pos = 0

# Establecer geometría de la root
root.geometry(f"{ancho_root}x{altura_root}+{x_pos}+{y_pos}")

# Etiqueta para mostrar la ruta
ruta_label = tk.Label(root, text="Ruta: ")
ruta_label.pack(padx=10, pady=10)

# Botón para cargar archivo
cargar_archivo_btn = tk.Button(root, text="Cargar Archivo", command=cargar_archivo)
cargar_archivo_btn.place(x=500,y=7)
def cargar_modelo():
    pass
cargar_modelo_btn = tk.Button(root, text="Cargar Modelo", command=cargar_modelo)
cargar_modelo_btn.place(x=600,y=7)
root.mainloop()
