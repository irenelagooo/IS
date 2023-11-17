import pandas as pd
import matplotlib.pyplot as plt

def datos_regresion(X, Y):
    n=X.shape[-1]
    y_media = Y.mean()
    x_media=[]
    for i in range(n):
        x=X.iloc[:, i]
        x_media.append(x.mean())
    b = []
    b0 = y_media
    
    for i in range(n):
        numerador = ((X.iloc[:, i] - x_media[i]) * (Y - y_media)).sum()
        denominador = ((X.iloc[:, i] - x_media[i])**2).sum()
        k = numerador / denominador
        b.append(k)
        b0 -= k * x_media[i]
    b.append(b0)
    return b

def mostrar_regresion(X,Y):
    b=datos_regresion(X,Y)
    n=len(b)
    R_cuadrado=bondad_ajuste(X,Y)
    print(f"\nCoeficiente de determinación o bondad del ajuste (R^2): {R_cuadrado}")
    print(f'\nLos datos de la regresión son:\nb0='+str(b[-1]))
    for i in range(n-1):
        print('b'+str(i+1),f'={b[i]}')
    
def recta_regresion(X,Y,x_nuevo=None):
    regresion=datos_regresion(X,Y)
    resultado=regresion[-1] #ordenada en el origen
    x=x_nuevo if x_nuevo is not None else X
    n=x.shape[1]
    for i in range(n):
        resultado+=regresion[i]*x.iloc[:,i] 
    return resultado

def bondad_ajuste(X, Y):
    recta = recta_regresion(X, Y)
    SST = ((Y - Y.mean())**2).sum()
    SSR = ((recta - Y.mean())**2).sum()
    R_cuadrado = SSR / SST
    return R_cuadrado

def formula_recta(m,n):
    x=0
    r=f'{n:.3f}'
    for i in m:
        s='+' if i>=0 else ''
        x+=1
        r+=f'{s}{i:.3f}x{x}'
    return f"y={r}"

def predicciones_modelo_cargado(m, n, x):
    y=n
    for i in m:
        y+=i*x
    return y

def imprimir_datos(X, Y, x_nuevo=None):
    n=X.shape[1]
    if n==1:
        x = pd.DataFrame({'X': X.iloc[:, 0]})
        recta = recta_regresion(x, Y)
        plt.scatter(X.iloc[:, 0], Y, color='blue', label=f'Datos de entrenamiento', s=1)
        plt.plot(X.iloc[:, 0], recta, color='black', label=f'Recta de Regresión', linewidth=1)

        if x_nuevo is not None:
            x_nuevo2 = pd.DataFrame({'X': x_nuevo.iloc[:, 0]})
            y_nuevo = recta_regresion(x, Y, x_nuevo2)
            plt.scatter(x_nuevo2, y_nuevo, color='red', label=f'Predicciones', s=20) 

        plt.xlabel(X.columns[0])
        plt.ylabel(Y.name)
        plt.legend()
        plt.show()
    else:
        _, axes = plt.subplots(n, 1, figsize=(8, 6 * n))
        
        for i in range(n):
            x = pd.DataFrame({'X': X.iloc[:, i]})  # x tiene que ser un DataFrame, no DataSeries
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
        plt.show()
