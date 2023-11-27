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
def crear_interfaz(root):
    global resultado_label
    ancho_root = root.winfo_screenwidth()
    altura_pantalla = root.winfo_screenheight()
    
    altura_root = altura_pantalla - 100
    
    x_pos = ancho_root // 1000
    y_pos = 0
    
    root.geometry(f"{ancho_root}x{altura_root}+{x_pos}+{y_pos}")
    
    resultado_label = ttk.Label(root, text="", style="Boton.TLabel")
    resultado_label.place(x=450, y=400)

    cerrar_btn = tk.Button(root, text="Salir", command=cerrar_programa, bg="red", fg="white", font=("Arial", 12))
    cerrar_btn.place(x=1000, y=5)

    cargar_archivo_btn = tk.Button(root, text="Cargar Archivo", command=lambda: cargar_archivo(root))
    cargar_archivo_btn.place(x=800,y=7)

    regresion=None

    cargar_modelo_btn = tk.Button(root, text="Cargar Modelo", command= lambda: cargar_regresion(resultado_label,regresion))
    cargar_modelo_btn.place(x=900,y=7)
    
def boton_predicciones(root,x_seleccionadas):
    calcular_predicciones_btn = tk.Button(root, text="Calcular Predicciones", command= lambda: calcular_predicciones_click(root,x_seleccionadas))
    calcular_predicciones_btn.place(x=20, y=800)
    

def calcular_predicciones_click(root,x_seleccionadas):
    '''for entry in cuadros_texto:
        entry.destroy()'''
    
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

def ruta_archivo(root,archivo):
    ruta_label = tk.Label(root, text=f"Ruta: {archivo}")
    ruta_label.pack(padx=10, pady=10)
    return ruta_label

def crear_tabla(root,mis_datos):
    
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

    
    variables_x = {col: tk.BooleanVar(value=False) for col in columnas_numericas}

    for col in columnas_numericas:
        checkbutton_x = ttk.Checkbutton(variables_frame_x, text=col, variable=variables_x[col])
        checkbutton_x.pack(side=tk.LEFT)
    return variables_x

def seleccionar_y(root,columnas_numericas):
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

    variable_y_seleccionada_radio = tk.StringVar()
    for col in columnas_numericas:

        radio_y = ttk.Radiobutton(variables_frame_y, text=col, variable=variable_y_seleccionada_radio, value=col)
    
        radio_y.pack(side=tk.LEFT)
    return variable_y_seleccionada_radio

def cargar_datos(root,archivo):

    mis_datos = leer_archivos(archivo)

    ruta_archivo(root,archivo)

    crear_tabla(root,mis_datos)

    columnas_numericas = mis_datos.select_dtypes(include='number').columns.tolist()
    
    variables_x=seleccionar_x(root,columnas_numericas)
    variable_y_seleccionada_radio=seleccionar_y(root,columnas_numericas)
    boton_calculo = tk.Button(root, text="Calcular Regresión", command= lambda: calcular_regresion_click(root,mis_datos,variables_x,variable_y_seleccionada_radio))
    boton_calculo.place(x=700, y=325)

def calcular_regresion_click(root,mis_datos,variables_x,variable_y_seleccionada_radio):
    plt.close('all') 

    x,y,m,n,R=regresion_gui(mis_datos,variables_x,variable_y_seleccionada_radio)
    x_seleccionadas=x.columns.tolist()
    boton_predicciones(root,x_seleccionadas)
    #calcular_predicciones_btn.place(x=20, y=800)
    root.update()
    
    imprimir_graficas(x,y)

    boton_descargar(root,m,n,R)

def imprimir_graficas(x,y):
    fig=imprimir_datos(x, y)
    frame_graficas = tk.Frame(root)
    frame_graficas.place(x=50, y=450) 
    canvas_graficas = tk.Canvas(frame_graficas, bg='white', width=root.winfo_screenwidth(), height=400)
    canvas_graficas.pack(side='top', fill='both', expand=True)

    frame_interior = tk.Frame(canvas_graficas)
    canvas_graficas.create_window((0, 0), window=frame_interior, anchor='nw')

    scrollbar_x_graficas = ttk.Scrollbar(frame_graficas, orient='horizontal', command=canvas_graficas.xview)
    scrollbar_x_graficas.pack(side='bottom', fill='x')
    canvas_graficas.configure(xscrollcommand=scrollbar_x_graficas.set)

    frame_interior.bind('<Configure>', lambda e: canvas_graficas.configure(scrollregion=canvas_graficas.bbox('all')))

    canvas_graficas.create_window((0, 0), window=frame_interior, anchor='nw')
    canvas_fig = FigureCanvasTkAgg(fig, master=frame_interior)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().pack(side='left', fill='both', expand=True)



def regresion_gui(mis_datos,variables_x,variable_y_seleccionada_radio):
    width_of_label=400
    x_seleccionadas = [col for col, var in variables_x.items() if var.get()]

    y_seleccionada = variable_y_seleccionada_radio.get()

    if not x_seleccionadas or not y_seleccionada:
        resultado_label.config(text="Error: Debes seleccionar al menos una variable X e Y")
        x_coordinate = (width_of_label) / 2 
        resultado_label.place_configure(x=x_coordinate)
        resultado_label.lift()

    x = mis_datos[x_seleccionadas]
    y = mis_datos[y_seleccionada]
    l = datos_regresion(x, y)
    n = l[-1]
    m = l[:-1]
    R = bondad_ajuste(x, y)
    r = formula_recta(m, n)
    resultado_label.config(text=f"Recta regresión: {r}, Bondad del ajuste: {R:.3f}")
    x_coordinate = (width_of_label) / 2  
    resultado_label.place_configure(x=x_coordinate)
    resultado_label.lift()
    return x,y,m,n,R

def boton_descargar(root,m,n,R):
    descargar_modelo_button = tk.Button(root, text="Descargar Modelo", command=lambda: guardar_regresion(m,n,R))
    descargar_modelo_button.place(x=130,y=395)


   
       
    

'''    for i in range(n):
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

        '''


def cargar_archivo(root):
    limpiar_interfaz()
    crear_interfaz(root)
    archivo = filedialog.askopenfilename(filetypes=[("CSV Files", ".csv"), ("Excel Files", ".xlsx"),("DataBase Files", ".db")])
    if archivo:
        cargar_datos(root,archivo)
        

def cerrar_programa():
    root.destroy()
    
def destruir_widgets():
    for widget in root.winfo_children():
        widget.destroy()

def limpiar_interfaz():
    for widget in root.winfo_children():
        widget.destroy()

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
    cerrar_btn = tk.Button(frame_modelo, text="Cerrar", command=lambda: [frame_modelo.destroy()])
    cerrar_btn.pack()
    
def crear_ventana():
    root = tk.Tk()
    root.title("Regresion")
    return root

if __name__=='__main__':
    root=crear_ventana()
    crear_interfaz(root)
    root.mainloop()
