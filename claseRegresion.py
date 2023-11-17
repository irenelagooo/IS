from dataclasses import dataclass
import pickle

@dataclass
class Regresion:
    #nombre:str
    m:list
    n:float
    texto:str
    bondad_del_ajuste:float

    def __repr__(self) -> str:
        x=0
        xd=f'{self.n:.3f}'
        for i in self.m:
            x+=1
            xd+=f'+{i:.3f}x{x}'
        return f"\nrecta: y={xd}, bondad_del_ajuste: {self.bondad_del_ajuste}"
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