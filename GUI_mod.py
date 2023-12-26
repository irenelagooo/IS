import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import tkinter as tk
from tkinter import ttk, Scrollbar, filedialog, simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from regresionsimplemultiple import *
from claseRegresion import Regresion
from carga_guardado import cargar_regresion,guardar_regresion,leer_archivos
from regresionsimplemultiple import imprimir_datos
import sys

def crear_interfaz(root):
    '''
    Crea los botones y ajustes que apareceran al iniciar la interfaz
 
    Parameters
    ----------
    root: tk.Tk
        ventana principal de la interfaz gráfica
 
    Returns
    -------
    None
    '''

    ancho_root = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()
    
    altura_root = altura_pantalla - 100
    
    x_pos = ancho_root // 1000
    y_pos = 0
    
    root.geometry(f"{ancho_root}x{altura_root}+{x_pos}+{y_pos}")
    
    resultado_label = ttk.Label(root, text="", style="Boton.TLabel")
    resultado_label.place(x=500, y=415)

    frame_botones = tk.Frame(root)
    frame_botones.pack(pady=10)

    cargar_archivo_btn = tk.Button(frame_botones, text="Cargar Archivo", command=lambda: cargar_archivo(root))
    cargar_archivo_btn.pack(side=tk.LEFT, padx=10)

    cargar_modelo_btn = tk.Button(frame_botones, text="Cargar Modelo", command=lambda: cargar_modelo_click(root))
    cargar_modelo_btn.pack(side=tk.LEFT, padx=10)
    
def cargar_modelo_click(root):
    '''
    Carga un modelo de regresión almacenado desde un archivo, lo muestra y agrega
    un botón en la interfazpara realizar predicciones utilizando el modelo cargado

    Parameters
    ----------
    root: tk.Tk
        ventana principal de la interfaz gráfica

    Returns
    -------
    None
    '''
    limpiar_interfaz()
    crear_interfaz(root)
    label = ttk.Label(root, text="", style="Boton.TLabel")
    label.place(x=500, y=400)
    resultado_carga = cargar_regresion(label)
    m, n, x_seleccionadas=resultado_carga.m, resultado_carga.n, resultado_carga.x
    boton_predicciones(root, x_seleccionadas,m,n)

    
def boton_predicciones(root,x_seleccionadas,m,n):
    '''
    Crea el botón para calcular las predicciones
 
    Parameters
    ----------
    root: tk.Tk
        ventana principal de la interfaz gráfica
    x_seleccionadas: list
        lista con los nombres de las variables independientes
    Returns
    -------
    None
    '''

    valores_x=calcular_predicciones_cuadros(root,x_seleccionadas)
    #x=[i.get() for i in valores_x]
    calcular_predicciones_btn = tk.Button(root, text="Calcular Predicciones", command= lambda: calcular_predicciones_click(m,n,valores_x))
    calcular_predicciones_btn.place(x=20, y=675)
    
def calcular_predicciones_click(m,n,valores_x):
    '''
    Crea tantos cuadros de texto como variables x haya para introducir las predicciones
 
    Parameters
    ----------
    m: list
        lista con las pendientes de la regresión
    n: float
        ordenada en el origen
    valores_x: list
        lista de cuadros de texto creados para ingresar valores
    Returns
    -------
    None
    '''

    x=[int(i.get()) for i in valores_x]
    prediccion=predicciones(m,n,x)
    prediccion_label = ttk.Label(root, text=f"Valor: {prediccion}", style="Boton.TLabel")
    prediccion_label.place(x=200, y=675)

def calcular_predicciones_cuadros(root, x_seleccionadas):
    '''
    Crea y muestra cuadros de texto para ingresar valores de variables independientes en la interfaz

    Parameters
    ----------
    root: tk.Tk
        ventana principal de la interfaz gráfica.
    x_seleccionadas: list
        lista de nombres de variables independientes seleccionadas

    Returns
    -------
    cuadros_texto: list
        lista de cuadros de texto creados para ingresar valores
    '''

    borrar_predicciones_canvas(root)

    ancho_root = root.winfo_screenwidth()

    cuadros_texto = []

    canvas_cuadros_texto = tk.Canvas(root, bd=0, highlightthickness=0)
    canvas_cuadros_texto.place(x=20, y=715, width=ancho_root - 50)

    frame_cuadros_texto = tk.Frame(canvas_cuadros_texto)
    canvas_cuadros_texto.create_window((0, 0), window=frame_cuadros_texto, anchor='nw')

    scrollbar_horizontal = ttk.Scrollbar(root, orient="horizontal", command=canvas_cuadros_texto.xview)
    scrollbar_horizontal.place(x=20, y=738, width=ancho_root - 50)
    canvas_cuadros_texto.configure(xscrollcommand=scrollbar_horizontal.set)

    frame_cuadros_texto.bind("<Configure>", lambda e: canvas_cuadros_texto.configure(scrollregion=canvas_cuadros_texto.bbox("all")))

    for var in x_seleccionadas:
        frame_variable = tk.Frame(frame_cuadros_texto)
        frame_variable.pack(side=tk.LEFT, padx=5)

        label_variable = tk.Label(frame_variable, text=f"Variable {var}:")
        label_variable.pack(side=tk.LEFT, padx=5)

        entry_variable = tk.Entry(frame_variable)
        entry_variable.pack(side=tk.LEFT, padx=5)

        cuadros_texto.append(entry_variable)

    frame_cuadros_texto.update_idletasks()
    canvas_cuadros_texto.config(scrollregion=canvas_cuadros_texto.bbox("all"))

    root.canvas_predicciones = canvas_cuadros_texto
    root.scrollbar_predicciones = scrollbar_horizontal

    return cuadros_texto

def borrar_predicciones_canvas(root):
    '''
    Elimina los elementos gráficos relacionados con la entrada de valores para predicciones

    Parameters
    ----------
    root: tk.Tk
        ventana principal de la interfaz gráfica
    
    Returns
    -------
    None
    '''
    # Verificar si existen elementos de predicciones y destruirlos
    if hasattr(root, 'canvas_predicciones'):
        root.canvas_predicciones.destroy()
        root.scrollbar_predicciones.destroy()


def ruta_archivo(root, archivo):
    '''
    Crea una etiqueta que muestra la ruta del archivo
    Parameters
    ----------
    root: tk.Tk
        ventana principal de la interfaz gráfica
    archivo: str
        ruta del archivo seleccionado
       
    Returns
    -------
    ruta_label: Label
        etiqueta con la ruta del archivo
    '''

    ruta_label = tk.Label(root, text=f"Ruta: {archivo}")
    ruta_label.pack(anchor='nw', padx=10, pady=0)  # Ajuste en el anclaje y los márgenes
    return ruta_label


def crear_tabla(root,mis_datos):
    '''
    Crea un marco y configura encabezados para mostrar los datos en una tabla
    Parameters
    ----------
    root: tk.Tk
        ventana principal de la interfaz gráfica
    mis_datos: DataFrame
        dataframe con la información del archivo
       
    Returns
    -------
    None
    '''

    frame_tabla = tk.Frame(root)
    frame_tabla.pack(pady=10, padx=20)

    treeview = ttk.Treeview(frame_tabla)
    treeview["columns"] = tuple(mis_datos.columns)

    for column in mis_datos.columns:
        treeview.heading(column, text=column)

    for i, row in mis_datos.iterrows():
        treeview.insert("", i, values=tuple(row))
    for col in mis_datos.columns:
        treeview.heading(col, text=col, anchor='center')  
        treeview.column(col, anchor='center', width=150)
    
    treeview.heading('#0', text='', anchor='center') 
    treeview.column('#0', width=0, anchor='center')  

    yscroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=treeview.yview)
    yscroll.pack(side="right", fill="y")
    treeview.configure(yscrollcommand=yscroll.set)

    xscroll = ttk.Scrollbar(frame_tabla, orient="horizontal", command=treeview.xview)
    xscroll.pack(side="bottom", fill="x")
    treeview.configure(xscrollcommand=xscroll.set)

    treeview.pack()
    
def seleccionar_x(root,columnas_numericas):
    '''
    Muestra las variables X y crea checkbuttons para poder seleccionarlas
    Parameters
    ----------
    root: tk.Tk
        ventana principal de la interfaz gráfica
    columnas_numericas: DataFrame
        dataframe donde todas las columnas son numericas
       
    Returns
    -------
    variables_x: DataFrame
        dataframe con booleanos que indican si se seleccionó o no cada variable
 
    '''

    ancho_root = root.winfo_screenwidth()

    seleccionar_var_x_label = tk.Label(root, text="Selecciona variable(s) X:")
    seleccionar_var_x_label.place(x=10, y=330)

    canvas_x = tk.Canvas(root, bd=0, highlightthickness=0)
    canvas_x.place(x=seleccionar_var_x_label.winfo_reqwidth() + 10, y=330, width=ancho_root-310)

    variables_frame_x = tk.Frame(canvas_x)
    scrollbar_x = ttk.Scrollbar(root, orient="horizontal", command=canvas_x.xview)
    scrollbar_x.place(x=seleccionar_var_x_label.winfo_reqwidth() + 10, y=357, width=ancho_root-310)
    canvas_x.configure(xscrollcommand=scrollbar_x.set)

    variables_frame_x.bind("<Configure>", lambda e: canvas_x.configure(scrollregion=canvas_x.bbox("all")))

    canvas_x.create_window((0, 0), window=variables_frame_x, anchor="nw")

    
    variables_x = {col: tk.BooleanVar(value=False) for col in columnas_numericas}

    for col in columnas_numericas:
        checkbutton_x = ttk.Checkbutton(variables_frame_x, text=col, variable=variables_x[col])
        checkbutton_x.pack(side=tk.LEFT)
    return variables_x

def seleccionar_y(root,columnas_numericas):
    '''
    Muestra las variables Y y crea radio buttons para seleccionar una
 
    Parameters
    ----------
    root: Tk
        ventana principal de la interfaz gráfica
    columnas_numericas: list
        dataFrame donde todas las columnas son numéricas
 
    Returns
    -------
    variable_y_seleccionada_radio: tk.StringVar
        variable Y seleccionada
    '''

    ancho_root = root.winfo_screenwidth()

    seleccionar_var_y_label = tk.Label(root, text="Selecciona variable Y:")
    seleccionar_var_y_label.place(x=10, y=370)

    canvas_y = tk.Canvas(root, bd=0, highlightthickness=0)
    canvas_y.place(x=seleccionar_var_y_label.winfo_reqwidth() + 23, y=370, width=ancho_root-310)

    variables_frame_y = tk.Frame(canvas_y)
    scrollbar_y = ttk.Scrollbar(root, orient="horizontal", command=canvas_y.xview)
    scrollbar_y.place(x=seleccionar_var_y_label.winfo_reqwidth() + 23, y=397, width=ancho_root-310)
    canvas_y.configure(xscrollcommand=scrollbar_y.set)

    variables_frame_y.bind("<Configure>", lambda e: canvas_y.configure(scrollregion=canvas_y.bbox("all")))

    canvas_y.create_window((0, 0), window=variables_frame_y, anchor="nw")

    variable_y_seleccionada_radio = tk.StringVar()
    for col in columnas_numericas:

        radio_y = ttk.Radiobutton(variables_frame_y, text=col, variable=variable_y_seleccionada_radio, value=col)
    
        radio_y.pack(side=tk.LEFT)
    return variable_y_seleccionada_radio

def cargar_datos(root,archivo):
    '''
    Carga datos desde un archivo y llama a otras funciones para mostrar y seleccionar variables X y la variable Y y mostrar un botón para calcular la regresión
 
    Parameters
    ----------
    root: tk.Tk
        ventana principal de la interfaz gráfica
    archivo: str
        ruta del archivo seleccionado
 
    Returns
    -------
    None
    '''

    mis_datos = leer_archivos(archivo)

    ruta_archivo(root,archivo)

    crear_tabla(root,mis_datos)

    columnas_numericas = mis_datos.select_dtypes(include='number').columns.tolist()
    
    variables_x=seleccionar_x(root,columnas_numericas)
    variable_y_seleccionada_radio=seleccionar_y(root,columnas_numericas)
    boton_calculo = tk.Button(root, text="Calcular Regresión", command= lambda: calcular_regresion_click(root,mis_datos,variables_x,variable_y_seleccionada_radio))
    boton_calculo.place(x=100, y=415)

def calcular_regresion_click(root, mis_datos, variables_x, variable_y_seleccionada_radio):
    '''
    Calcula la regresión e imprime los resultados
 
    Parameters
    ----------
    root: tk.Tk
        ventana principal de la interfaz gráfica
    mis_datos: pd.DataFrame
        dataFrame con la información del archivo
    variables_x: dict
        diccionario con booleanos que indican si se seleccionó o no cada variable X
    variable_y_seleccionada_radio: tk.StringVar
        variable Y seleccionada
 
    Returns
    -------
    None
    '''

    plt.close('all') 

    resultado_label = next((child for child in root.winfo_children() if isinstance(child, ttk.Label)), None)

    x, y, m, n, R = regresion_gui(mis_datos, variables_x, variable_y_seleccionada_radio, resultado_label)
    x_seleccionadas = x.columns.tolist()
    boton_predicciones(root, x_seleccionadas, m, n)
    root.update()

    # Actualiza el texto de la etiqueta con el resultado
    resultado_label.config(text=f"Recta regresión: {formula_recta(m, n)}, Bondad del ajuste: {R:.3f}")
    resultado_label.lift()

    imprimir_graficas(x, y, root)
    boton_descargar(root, m, n, R, x_seleccionadas)

def regresion_gui(mis_datos, variables_x, variable_y_seleccionada_radio, resultado_label):
    '''
    Obtiene las variables x e y, la(s) pendiente(s), ordenada en el origen y bondad del ajuste
 
    Parameters
    ----------
    mis_datos: pd.DataFrame
        dataFrame con la información del archivo
    variables_x: dict
        diccionario con booleanos que indican si se seleccionó o no cada variable X
    variable_y_seleccionada_radio: tk.StringVar
        variable Y seleccionada
    resultado_label: ttk.Label
        etiqueta para mostrar resultados
 
    Returns
    -------
    x: pd.Dataframe
        dataframe con las variables X seleccionadas
    y: panda.series
        variable y seleccionada
    m: list
        lista con las pendientes de la regresión
    n: float
        ordenada en el origen
    R: float
        bondad del ajuste
    '''

    width_of_label = 400
    x_seleccionadas = [col for col, var in variables_x.items() if var.get()]

    y_seleccionada = variable_y_seleccionada_radio.get()

    if not x_seleccionadas or not y_seleccionada:
        resultado_label.config(text="Error: Debes seleccionar al menos una variable X e Y")
        resultado_label.lift()

    x = mis_datos[x_seleccionadas]
    y = mis_datos[y_seleccionada]
    m, n = datos_regresion(x, y)
    R = bondad_ajuste(x, y)
    r = formula_recta(m, n)
    resultado_label.config(text=f"Recta regresión: {r}, Bondad del ajuste: {R:.3f}")
    resultado_label.lift()
    return x, y, m, n, R

def borrar_canvas_grafica(root):
    '''
    Borra los elementos gráficos asociados a la visualización de gráficas en la interfaz

    Parameters
    ----------
    root: tk.Tk
        ventana principal de la interfaz gráfica.

    Returns
    -------
    None
    '''

    if hasattr(root, 'canvas_fig'):
        root.canvas_fig.get_tk_widget().destroy()
        root.frame_graficas.destroy()


def imprimir_graficas(x, y, root):
    '''
    Imprime la regresión y crea un marco para mostrar las gráfica
 
    Parameters
    ----------
    x: pd.Dataframe
        dataframe con las variables X
    y: panda.series
        variable Y
 
    Returns
    -------
    None
    '''
    # Obtener el color de fondo de la ventana
    color_fondo_ventana = root.cget('bg')

    borrar_canvas_grafica(root)

    fig = imprimir_datos(x, y)
    
    frame_graficas = tk.Frame(root)
    frame_graficas.pack(padx=50, pady=(120, 0)) 
    canvas_graficas = tk.Canvas(frame_graficas, bg=color_fondo_ventana, width=root.winfo_screenwidth(), height=200)  # Ajuste de altura
    canvas_graficas.pack(side='top', fill='both', expand=True)
    canvas_graficas.config(highlightthickness=0)  # Eliminar el borde del canvas

    frame_interior = tk.Frame(canvas_graficas, bg=color_fondo_ventana)  # Ajustar el fondo al color de la ventana
    canvas_graficas.create_window((0, 0), window=frame_interior, anchor='nw')

    scrollbar_x_graficas = ttk.Scrollbar(frame_graficas, orient='horizontal', command=canvas_graficas.xview)
    scrollbar_x_graficas.pack(side='bottom', fill='x')
    canvas_graficas.configure(xscrollcommand=scrollbar_x_graficas.set)

    frame_interior.bind('<Configure>', lambda e: canvas_graficas.configure(scrollregion=canvas_graficas.bbox('all')))

    canvas_graficas.create_window((0, 0), window=frame_interior, anchor='nw')
    canvas_fig = FigureCanvasTkAgg(fig, master=frame_interior)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().pack(side='left', fill='both', expand=True)
    
    # Guardar referencia a las gráficas para su eliminación posterior si es necesario
    root.canvas_fig = canvas_fig
    root.frame_graficas = frame_graficas


def boton_descargar(root,m,n,R,x_seleccionadas):
    '''
    Crea un botón que, al pulsarlo, guardará el modelo en un archivo
 
    Parameters
    ----------
    root: tk.Tk
        ventana principal de la interfaz gráfica
    m: list
        lista con las pendientes de la regresión
    n: float
        ordenada en el origen
    R: float
        bondad del ajuste
 
    Returns
    -------
    None
    '''

    descargar_modelo_button = tk.Button(root, text="Descargar Modelo", command=lambda: guardar_regresion(m,n,R,x_seleccionadas))
    descargar_modelo_button.place(x=300,y=415)


def cargar_archivo(root):
    '''
    Carga un archivo seleccionado por el usuario y carga los datos
    Parameters
    ----------
    root: tk.Tk
        ventana principal de la interfaz gráfica
 
    Returns
    -------
    None
    '''
    limpiar_interfaz()
    crear_interfaz(root)
    archivo = filedialog.askopenfilename(filetypes=[("CSV Files", ".csv"), ("Excel Files", ".xlsx"),("DataBase Files", ".db")])
    if archivo:
        cargar_datos(root,archivo)

def limpiar_interfaz():
    '''
    Elimina todos los widgets secundarios de la ventana principal
 
    Returns
    -------
    None
    '''

    for widget in root.winfo_children():
        widget.destroy()

def borrar_grafica():
    '''
    Si la ventana principal tiene un marco para las gráficas, los destruye
 
    Returns
    -------
    None
    '''

    if hasattr(root, 'frame_graficas'):
        root.frame_graficas.destroy()

def mostrar_modelo(regresion):
    frame_modelo = tk.Frame(root, bg='light grey', padx=20, pady=20)
    frame_modelo.place(relx=0.5, rely=0.5, anchor='center')
    
    # Mostrar el modelo dentro del Frame
    label_modelo = tk.Label(frame_modelo, text=str(regresion), font=("Arial", 12))
    label_modelo.pack(padx=10, pady=10)

def crear_ventana():
    '''
    Crea la ventana de la interfaz gráfica
 
    Returns
    -------
    root: tk.Tk
        ventana principal de la interfaz gráfica
    '''
    
    root = tk.Tk()
    root.title("Regresion")
    root.protocol("WM_DELETE_WINDOW",sys.exit)
    return root

if __name__=='__main__':
    root=crear_ventana()

    crear_interfaz(root)
    
    root.mainloop()
    
