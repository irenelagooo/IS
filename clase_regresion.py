from dataclasses import dataclass
import pickle
from regresion import formula_recta

@dataclass
class Regresion:
    '''
    Clase que representa un modelo de regresion lineal

    Attributes
    ---------
    m: list
        lista de pendientes de la recta de regresion
    n: float
        ordenada en el origen de la recta de regresion
    texto: str
        descripcion del modelo de regresión
    bondad_del_ajuste: float
        valor que indica la bondad del ajuste del modelo
    x: list
        lista con los nombres de las variables independientes
    y: str
        nombre de la variable dependiente
    Methods
    -------
    __repr__: devuelve una representación de cadena del objeto Regresion
    '''
    
    m:list
    n:float
    texto:str
    bondad_del_ajuste:float
    x:list
    y:str

    def __repr__(self) -> str:
        '''
        Devuelve una representación de cadena del objeto Regresion

        Returns
        -------
        str: cadena que representa el objeto Regresion
        '''
        return f"\nrecta: {formula_recta(self.m,self.n,self.x,self.y)}\nbondad_del_ajuste: {self.bondad_del_ajuste}\nDescripción: {self.texto}"
        

if __name__=='__main__':

    regresionPrueba = Regresion([1,3,90],'asd', 7, 0.9)
   
    # serializar
    with open('C:/Users/alexe/OneDrive/Escritorio/IS/guardar.txt', 'ab') as f:
        pickle.dump(regresionPrueba, f)

    # deserializar
    with open('C:/Users/alexe/OneDrive/Escritorio/IS/guardar.txt', 'rb') as f:
        try:
            regresion = pickle.load(f)
            print(regresion)    
        except EOFError:
            print("Objeto no encontrado en el archivo.")