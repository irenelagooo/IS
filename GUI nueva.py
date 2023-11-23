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
import pickle
from carga_guardado import cargar_regresion
def crear_interfaz():
    global ruta_label, cargar_archivo_btn, cargar_modelo_btn, resultado_label, ancho_root, altura_root, calcular_predicciones_btn

    
    ancho_pantalla = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()
    
    ancho_root = ancho_pantalla // 2
    altura_root = altura_pantalla - 100
    
    x_pos = ancho_pantalla // 4
    y_pos = 0
    
    root.geometry(f"{ancho_root}x{altura_root}+{x_pos}+{y_pos}")
    
    ruta_label = tk.Label(root, text="Ruta: ")
    ruta_label.pack(padx=10, pady=10)
    resultado_label = ttk.Label(root, text="", style="Boton.TLabel")
    resultado_label.place(x=450, y=400)
    cerrar_btn = tk.Button(root, text="Salir", command=cerrar_programa, bg="red", fg="white", font=("Arial", 12))
    cerrar_btn.place(x=900, y=0)
    calcular_predicciones_btn = tk.Button(root, text="Calcular Predicciones", command=calcular_predicciones_click)
    calcular_predicciones_btn.place_forget()
    cargar_archivo_btn = tk.Button(root, text="Cargar Archivo", command=cargar_archivo)
    cargar_archivo_btn.place(x=500,y=7)
    def cargar_modelo():
        limpiar_interfaz()
        crear_interfaz()
        archivo = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if archivo:
            with open(archivo, 'rb') as archivo:
                try:
                    
                    regresion = pickle.load(archivo)
                    mostrar_modelo(regresion)
                except EOFError:
                    resultado_label.config(text="Objeto no encontrado en el archivo.")
    cargar_modelo_btn = tk.Button(root, text="Cargar Modelo", command=cargar_modelo)
    cargar_modelo_btn.place(x=600,y=7)
def eliminar_frame_blanco():
    global frame_blanco
    
    if 'frame_blanco' in globals():
        frame_blanco.destroy()

def crear_frame_blanco():
    global frame_blanco
    
    frame_blanco = tk.Frame(root, bg='white')
    frame_blanco.place(x=0, y=840, width=10000, height=30)
def calcular_predicciones_click():
    global cuadros_texto
    global root 
    global x_seleccionadas  
    
    if 'cuadros_texto' in globals():
        for entry in cuadros_texto:
            entry.destroy()
    
    cuadros_texto = [] 
    
    canvas_cuadros_texto = tk.Canvas(root, bd=0, highlightthickness=0)
    canvas_cuadros_texto.place(x=20, y=850, width=1000)
    
    frame_cuadros_texto = tk.Frame(canvas_cuadros_texto)
    canvas_cuadros_texto.create_window((0, 0), window=frame_cuadros_texto, anchor='nw')
    
    scrollbar_horizontal = ttk.Scrollbar(root, orient="horizontal", command=canvas_cuadros_texto.xview)
    scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)
    canvas_cuadros_texto.configure(xscrollcommand=scrollbar_horizontal.set)
    
    frame_cuadros_texto.bind("<Configure>", lambda e: canvas_cuadros_texto.configure(scrollregion=canvas_cuadros_texto.bbox("all")))
    
    for var in x_seleccionadas:
        frame_variable = tk.Frame(frame_cuadros_texto)
        frame_variable.pack(side=tk.LEFT, padx=5)  
        
        label_variable = tk.Label(frame_variable, text=f"Variable '{var}':")
        label_variable.pack(side=tk.LEFT, padx=5)
        
        entry_variable = tk.Entry(frame_variable)
        entry_variable.pack(side=tk.LEFT, padx=5)
        
        cuadros_texto.append(entry_variable) 

    canvas_cuadros_texto.bind("<Configure>", lambda e: canvas_cuadros_texto.configure(scrollregion=canvas_cuadros_texto.bbox("all")))
    eliminar_frame_blanco()

def cargar_datos(archivo):
    
    global mis_datos

    mis_datos = obtener_datos(archivo)
    if not mis_datos.index.name:  
        mis_datos.index.name = 'Índice'
        mis_datos.reset_index(inplace=True)

    ruta_label.config(text=f"Ruta: {archivo}")

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

    if 'Índice' in mis_datos.columns:
        treeview.heading('Índice', text='Índice', anchor='center')
        treeview.column('Índice', anchor='center', width=50)
        
    
    treeview.heading('#0', text='', anchor='center') 
    treeview.column('#0', width=0, anchor='center')  

    yscroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=treeview.yview)
    yscroll.pack(side="right", fill="y")
    treeview.configure(yscrollcommand=yscroll.set)

    xscroll = ttk.Scrollbar(frame_tabla, orient="horizontal", command=treeview.xview)
    xscroll.pack(side="bottom", fill="x")
    treeview.configure(xscrollcommand=xscroll.set)

    treeview.pack()

    width_of_label = 400 


    
    def calcular_regresion_click():
        crear_frame_blanco()

        global l, R, x_seleccionadas
        plt.close('all') 
    
        x_seleccionadas = [col for col, var in variables_x.items() if var.get()]

        y_seleccionada = variable_y_seleccionada_radio.get()
    
        if not x_seleccionadas or not y_seleccionada:
            resultado_label.config(text="Error: Debes seleccionar al menos una variable X e Y")
            x_coordinate = (ancho_root - width_of_label) / 2 
            resultado_label.place_configure(x=x_coordinate)
            resultado_label.lift()
            calcular_predicciones_btn.place_forget()

            return
    
        x = mis_datos[x_seleccionadas]
        y = mis_datos[y_seleccionada]
    
        l = datos_regresion(x, y)
        n = l[-1]
        m = l[:-1]
    
        R = bondad_ajuste(x, y)
        r = formula_recta(m, n)
        resultado_label.config(text=f"Recta regresión: {r}, Bondad del ajuste: {R:.3f}")
        x_coordinate = (ancho_root - width_of_label) / 2  
        resultado_label.place_configure(x=x_coordinate)
        resultado_label.lift()
        resultado_label.lift()
        calcular_predicciones_btn.place(x=20, y=800)
        root.update()
        
        imprimir_datos(x, y)
        
        descargar_modelo_button = tk.Button(root, text="Descargar Modelo", command=guardar_regresion)
        descargar_modelo_button.place(x=130,y=395)
        
    

    boton_calculo = tk.Button(root, text="Calcular Regresión", command=calcular_regresion_click)
    boton_calculo.place(x=700, y=325)
    

    seleccionar_var_x_label = tk.Label(root, text="Selecciona variable(s) X")
    seleccionar_var_x_label.place(x=100, y=300)

 
    canvas_x = tk.Canvas(root, bd=0, highlightthickness=0)
    canvas_x.place(x=300, y=300)

    variables_frame_x = tk.Frame(canvas_x)
    scrollbar_x = ttk.Scrollbar(root, orient="horizontal", command=canvas_x.xview)
    scrollbar_x.place(x=300, y=317, width=400)
    canvas_x.configure(xscrollcommand=scrollbar_x.set)

    variables_frame_x.bind("<Configure>", lambda e: canvas_x.configure(scrollregion=canvas_x.bbox("all")))

    canvas_x.create_window((0, 0), window=variables_frame_x, anchor="nw")

    columnas_numericas = mis_datos.select_dtypes(include='number').columns.tolist()
    global variables_x
    variables_x = {col: tk.BooleanVar(value=False) for col in columnas_numericas}

    for col in columnas_numericas:
        if col != 'Índice':
            checkbutton_x = ttk.Checkbutton(variables_frame_x, text=col, variable=variables_x[col])
            checkbutton_x.pack(side=tk.LEFT)
    
    seleccionar_var_y_label = tk.Label(root, text="Selecciona variable Y:")
    seleccionar_var_y_label.place(x=100, y=350)

    canvas_y = tk.Canvas(root, bd=0, highlightthickness=0)
    canvas_y.place(x=300, y=350)

    variables_frame_y = tk.Frame(canvas_y)
    scrollbar_y = ttk.Scrollbar(root, orient="horizontal", command=canvas_y.xview)
    scrollbar_y.place(x=300, y=367, width=400)
    canvas_y.configure(xscrollcommand=scrollbar_y.set)

    variables_frame_y.bind("<Configure>", lambda e: canvas_y.configure(scrollregion=canvas_y.bbox("all")))

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


def guardar_regresion():
    
    texto = simpledialog.askstring("Descripción", "Ingrese un texto que desee guardar con los datos de la regresión:")
    
    m=l[:-1]
    n=l[-1]
    
    regresion=Regresion(m,n,texto,R)
    archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    
    if archivo:
        with open(archivo,'wb') as archivo:
            pickle.dump(regresion,archivo)

def imprimir_datos(X, Y, x_nuevo=None):
    n = X.shape[1] 

    fig, axes = plt.subplots(1, n, figsize=(8 * n, 6))

    if n == 1:
        axes = [axes] 
        
    for i in range(n):
        x = pd.DataFrame({'X': X.iloc[:, i]})
        recta = recta_regresion(x, Y)
        axes[i].scatter(X.iloc[:, i], Y, color='blue', label=f'Datos de entrenamiento', s=1)
        axes[i].plot(X.iloc[:, i], recta, color='black', label=f'Recta de Regresión', linewidth=1)

        if x_nuevo is not None:
            x_nuevo2 = pd.DataFrame({'X': x_nuevo.iloc[:, i]})
            y_nuevo = recta_regresion(x, Y, x_nuevo2)
            axes[i].scatter(x_nuevo2, y_nuevo, color='red', label=f'Predicciones', s=20)

        axes[i].set_xlabel(X.columns[i])
        axes[i].set_ylabel(Y.name)
        axes[i].legend()

    plt.tight_layout()

    frame_graficas = tk.Frame(root)
    frame_graficas.place(x=50, y=430) 

    canvas_graficas = tk.Canvas(frame_graficas, bg='white', width=ancho_root - 100, height=300)
    canvas_graficas.pack(side='top', fill='both', expand=True)

    frame_interior = tk.Frame(canvas_graficas)
    canvas_graficas.create_window((0, 0), window=frame_interior, anchor='nw')


    scrollbar_x_graficas = ttk.Scrollbar(frame_graficas, orient='horizontal', command=canvas_graficas.xview)
    scrollbar_x_graficas.pack(side='bottom', fill='x')
    canvas_graficas.configure(xscrollcommand=scrollbar_x_graficas.set)

    def configurar_scroll_region(event):
        canvas_graficas.configure(scrollregion=canvas_graficas.bbox('all'))

    frame_interior.bind('<Configure>', configurar_scroll_region)

    canvas_graficas.create_window((0, 0), window=frame_interior, anchor='nw')

    for i in range(n):
        fig_plt = plt.figure(figsize=(6, 4))
        ax = fig_plt.add_subplot(111)
        ax.scatter(X.iloc[:, i], Y, color='blue', label=f'Datos de entrenamiento', s=1)
        ax.plot(X.iloc[:, i], recta, color='black', label=f'Recta de Regresión', linewidth=1)
        if x_nuevo is not None:
            x_nuevo2 = pd.DataFrame({'X': x_nuevo.iloc[:, i]})
            y_nuevo = recta_regresion(x, Y, x_nuevo2)
            ax.scatter(x_nuevo2, y_nuevo, color='red', label=f'Predicciones', s=20)

        ax.set_xlabel(X.columns[i])
        ax.set_ylabel(Y.name)
        ax.legend()

        canvas_fig = FigureCanvasTkAgg(fig_plt, master=frame_interior)
        canvas_fig.draw()
        canvas_fig.get_tk_widget().pack(side='left', fill='both', expand=True)

    plt.close('all')

def archivo_bien():
    limpiar_interfaz()
    crear_interfaz()
    archivo = filedialog.askopenfilename(filetypes=[("CSV Files", ".csv"), ("Excel Files", ".xlsx")])
    if archivo:
        cargar_datos(archivo)
        cargar_archivo_btn.place(x=680,y=7)
        cargar_modelo_btn.place(x=800,y=7)

def cerrar_programa():
    root.destroy()
    
def destruir_widgets():
    for widget in root.winfo_children():
        widget.destroy()
def cargar_archivo():
  
    respuesta = messagebox.askyesno("Cargar otro archivo", "¿Desea cargar un archivo?")
    if respuesta:
        
       archivo_bien()
    


def limpiar_interfaz():
    for widget in root.winfo_children():
        widget.destroy()

def obtener_datos(path):
    extension = path.split('.')[-1]
    if extension == 'csv':
        df = pd.read_csv(path, delimiter=',') 
    elif extension == 'xlsx':
        df = pd.read_excel(path)
    return df
def borrar_grafica():
    if hasattr(root, 'frame_graficas'):
        root.frame_graficas.destroy()

def mostrar_modelo(regresion):
    frame_modelo = tk.Frame(root, bg='light grey', padx=20, pady=20)
    frame_modelo.place(relx=0.5, rely=0.5, anchor='center')
    
    # Mostrar el modelo dentro del Frame
    label_modelo = tk.Label(frame_modelo, text=str(regresion), font=("Arial", 12))
    label_modelo.pack(padx=10, pady=10)
    
    # Botón para cerrar el Frame del modelo y volver a mostrar los botones
    cerrar_btn = tk.Button(frame_modelo, text="Cerrar", command=lambda: [frame_modelo.destroy(), cargar_archivo_btn.place(x=500, y=7), cargar_modelo_btn.place(x=600, y=7)])
    cerrar_btn.pack()
    

root = tk.Tk()
root.title("Regresion")
crear_interfaz()
root.mainloop()
