from abc import abstractmethod,ABC
import matplotlib.pyplot as plt
import pandas as pd
class CalcularRegresion(ABC):
    def __init__(self,x,y):
        self.x=x
        self.y=y.iloc[:,0]
        self.m=None
        self.n=None
        
    @abstractmethod
    def imprimir(self):
        pass
    @abstractmethod 
    def hacer_regresion(self):
        pass
    
    @abstractmethod 
    def datos_regresion(self):
        pass

    def get_pendiente(self):
        return self.m
    
    def get_ordenada(self):
        return self.n

class RegresionSimple(CalcularRegresion):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.x=x.iloc[:,0]
        self.datos_regresion()
    
    def hacer_regresion(self):
        return self.m*self.x+self.n
    
    def datos_regresion(self):
        y_media = self.y.mean()
        x_media=self.x.mean()
        numerador=((self.x-x_media) * (self.y-y_media)).sum()
        denominador=((self.x-x_media)**2).sum()
        self.m = numerador / denominador
        self.n = y_media - self.m * x_media

    def imprimir(self):
        recta = self.hacer_regresion()
        plt.scatter(self.x, self.y, color='blue', label='Datos de entrenamiento', s=1)
        plt.plot(self.x, recta, color='black', label='Recta regresión', linewidth=1)
  
        plt.xlabel(self.x.name)
        plt.ylabel(self.y.name)
        plt.legend()
        plt.show()

class RegresionMultiple(CalcularRegresion):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.datos_regresion()
    
    def hacer_regresion(self):
        resultado=self.n
        long=self.x.shape[1]
        for i in range(long):
            resultado+=self.m[i]*self.x.iloc[:,i] 
        return resultado
    
    def hacer_recta(self,m,x):
        y=m*x+self.n
        return y
    
    def imprimir(self):
        long = self.x.shape[1] 
        fig, axes = plt.subplots(1, long, figsize=(8 * long, 6))
        recta = self.hacer_regresion()
    
        for i in range(long):
            recta=self.hacer_recta(self.m[i],self.x.iloc[:,i])
            axes[i].scatter(self.x.iloc[:, i], self.y, color='blue', label=f'Datos de entrenamiento', s=1)
            axes[i].plot(self.x.iloc[:, i], recta, color='black', label=f'Recta de Regresión', linewidth=1)
            axes[i].set_xlabel(self.x.columns[i])
            axes[i].set_ylabel(self.y.name)
            axes[i].legend()

        plt.tight_layout()
        plt.show()
        return fig
    
    def datos_regresion(self):
        n=self.x.shape[1]
        y_media = self.y.mean()
        self.m = []
        self.n = y_media
        
        for i in range(n):
            numerador = ((self.x.iloc[:, i] - self.x.iloc[:, i].mean()) * (self.y - y_media)).sum()
            denominador = ((self.x.iloc[:, i] - self.x.iloc[:, i].mean())**2).sum()
            k = numerador / denominador
            self.m.append(k)
            self.n -= k * self.x.iloc[:, i].mean()

if __name__ == '__main__':
    x = pd.DataFrame({'X': [1, 2, 3, 4, 5]})
    y=pd.DataFrame({'Y': [2, 4, 5, 4, 5]})
    x2= pd.DataFrame({'X': [1, 2, 3, 4, 5],'X2': [10, 29, 3, 30, 51]})
    r1=RegresionSimple(x,y)
    r2=RegresionMultiple(x2,y)
    r2.imprimir()
    print(r1.get_pendiente())
    print(r2.get_pendiente())