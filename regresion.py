import pandas as pd
import matplotlib.pyplot as plt

def datos_regresion(X, Y):
    '''
    Calcula la(s) pendiente(s) y ordenada en el origen de la regresion
 
    Parameters
    ----------
    x: pd.DataFrame
        DataFrame con las variables X
    y: pd.series
        columna de un DataFrame con la variable Y
 
    Returns
    -------
    b: list
        lista con la(s) pendiente(s)
    b0: float
        ordenada en el origen de la regresion
    '''

    n = X.shape[1]
    y_media = Y.mean()
    b = []
    b0 = y_media
   
    for i in range(n):
        numerador = ((X.iloc[:, i] - X.iloc[:, i].mean()) * (Y - y_media)).sum()
        denominador = ((X.iloc[:, i] - X.iloc[:, i].mean())**2).sum()
        k = numerador / denominador
        b.append(k)
        b0 -= k * X.iloc[:, i].mean()
    
    return b, b0

def bondad_ajuste(X, Y):
    '''
    Calcula la bondad del ajuste de la regresion
 
    Parameters
    ----------
    X: pd.DataFrame
        DataFrame con las variables X
    Y: pd.series
        columna de un DataFrame con la variable Y
 
    Returns
    -------
    R_cuadrado: float
        bondad del ajuste de la regresion
    '''

    m, n = datos_regresion(X, Y)
    pred=valor_regresion(X, m, n)
    num = ((Y - pred)**2).sum()
    den = ((Y - Y.mean())**2).sum()
    R_cuadrado = 1 - (num / den)
    
    return R_cuadrado
 
def valor_regresion(X, m, n):
    '''
    Devuelve los valores de la regresion
 
    Parameters
    ----------
    X: pd.DataFrame
        DataFrame con las variables X
    m: float
        pendiente
    n: float
        ordenada en el origen
 
    Returns
    -------
    y: pd.series
        panda series con los valores de la regresion
    '''

    y = n
    
    for i in range(X.shape[1]):
        y += X.iloc[:, i] * m[i]
    
    return y

def formula_recta(m, n, x, y):
    '''
    Devuelve un string con la formula de la recta
 
    Parameters
    ----------
    m: float
        pendiente
    n: float
        ordenada en el origen
 
    Returns
    -------
    r: str
        formula de la recta
    '''

    ctn = 0
    r = f'{n:.3f}'
    
    for i in m:
        s = '+' if i >= 0 else ''
        r += f'{s}{i:.3f}x{x[ctn]}'
        ctn += 1
    
    return f"{y}={r}"

def predicciones(m, n, x):
    '''
    Devuelve el valor de las predicciones
 
    Parameters
    ----------
    m: float
        pendiente
    n: float
        ordenada en el origen
    x: list
        lista con el valor de cada variable x
    
    Returns
    -------
    y: float
        valor de la prediccion
    '''

    resultado = n # ordenada en el origen
    l = len(x)
    
    for i in range(l):
        resultado += m[i] * x[i] 
    
    return resultado

def hacer_recta(m, n, x):
    '''
    Devuelve el valor de la variable dependiente dadas
    la variable independiente, la pendiente y la ordenada
 
    Parameters
    ----------
    m: float
        pendiente
    n: float
        ordenada en el origen
    x: pd.series
        columna de un DataFrame con la variable X
    
    Returns
    -------
    y: pd.series
        columna de un DataFrame con la variable Y
    '''

    y = m * x + n
    return y

def imprimir_datos(X, Y):
    '''
    Crea las graficas de dispersion para representar la regresion
 
    Parameters
    ----------
    x: pd.DataFrame
        DataFrame con las variables X
    y: pd.series
        columna de un DataFrame con la variable Y
    
    Returns
    -------
    fig: Figure
        ventana en la que se dibujaran los graficos
    '''
    
    n = X.shape[1] 
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 2))
    b, b0 = datos_regresion(X, Y)
    recta = valor_regresion(X, b, b0)
    
    if n == 1: axes = [axes] 
    
    for i in range(n):
        m = b[i]
        recta = hacer_recta(m, b0, X.iloc[:, i])
        axes[i].scatter(X.iloc[:, i], Y, color = 'blue', label = f'Datos de entrenamiento', s = 1)
        axes[i].plot(X.iloc[:, i], recta, color = 'black', label = f'Recta de Regresión', linewidth = 1)
        axes[i].set_xlabel(X.columns[i])
        axes[i].set_ylabel(Y.name)
        axes[i].legend()

    plt.tight_layout()
    return fig