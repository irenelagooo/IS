from dataclasses import dataclass
import pickle
from regresionsimplemultiple import formula_recta

@dataclass
class Regresion:
    #nombre:str
    m:list
    n:float
    texto:str
    bondad_del_ajuste:float

    def __repr__(self) -> str:
        
        return f"\nrecta: {formula_recta(self.m,self.n)}, bondad_del_ajuste: {self.bondad_del_ajuste}, Descripción: {self.texto}"
        #serializar objeto (guardar y recuperar)

if __name__=='__main__':

    # Objetos a serializar
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