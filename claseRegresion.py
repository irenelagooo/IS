from dataclasses import dataclass
import pickle

@dataclass
class Regresion:
    nombre:str
    m:list
    n:float
    texto:str
    bondad_del_ajuste:float

    def __repr__(self) -> str:
        x=0
        xd=str(self.n)
        for i in self.m:
            x+=1
            xd+='+'+str(i)+'x'+str(x)
        return f"\nrecta: y={xd}, bondad_del_ajuste: {self.bondad_del_ajuste}"
        #serializar objeto (guardar y recuperar)

if __name__=='__main__':

    # Objeto # a serializar
    regresion1 = Regresion('reg1',[3], 5,'', 0.95)
    regresion2 = Regresion('reg2',[1,3,90],'asd', 7, 0.9)
    regresion3 = Regresion('reg3',[5],0,'ihdafbc', 0.925)
   
    # serializar
    with open('C:/Users/alexe/OneDrive/Escritorio/IS/guardar.txt', 'ab') as f:
        pickle.dump(regresion1, f)
        pickle.dump(regresion2, f)
        pickle.dump(regresion3, f)
    
    buscar='reg3'

    # deserializar
    with open('C:/Users/alexe/OneDrive/Escritorio/IS/guardar.txt', 'rb') as f:
        try:
            while True:
                regresion = pickle.load(f)
                if regresion.nombre == buscar:
                    print((regresion, type(regresion)))
                    break
        except EOFError:
            print("Objeto no encontrado en el archivo.")