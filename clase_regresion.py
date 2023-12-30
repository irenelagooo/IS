from regresion import formula_recta

class Regresion:
    '''
    Clase que representa un modelo de regresion lineal

    Attributes
    ---------
    _m: list
        lista de pendientes de la recta de regresion
    _n: float
        ordenada en el origen de la recta de regresion
    _texto: str
        descripcion del modelo de regresión
    _bondad_del_ajuste: float
        valor que indica la bondad del ajuste del modelo
    _x: list
        lista con los nombres de las variables independientes
    _y: str
        nombre de la variable dependiente
    Methods
    -------
    __init__: Inicializa una instancia de la clase Regresion
    __repr__: Devuelve una representación de cadena del objeto Regresion
    get_m: Devuelve una lista con las pendientes
    get_n: Devuelve el valor de la ordenada
    get_texto: Devuelve la descripcion de la regresion
    get_bondad_del_ajuste: Devuelve la bondad del ajuste de la regresion
    get_x: Devuelve una lista con las variables independientes
    get_y: Devuelve la variable dependiente
    '''
    def __init__(self, m, n, texto, bondad_del_ajuste, x, y):
        '''
        Inicializa una instancia de la clase Regresion.

        Parameters
        ----------
        m: list
            Lista de pendientes de la recta de regresion
        n: float
            Ordenada en el origen de la recta de regresion
        texto: str
            Descripción del modelo de regresión
        bondad_del_ajuste: float
            Valor que indica la bondad del ajuste del modelo
        x: list
            Lista con los nombres de las variables independientes
        y: str
            Nombre de la variable dependiente
        
        Returns
        -------
        None
        '''
        self._m = m
        self._n = n
        self._texto = texto
        self._bondad_del_ajuste = bondad_del_ajuste
        self._x = x
        self._y = y

    def __repr__(self):
        '''
        Devuelve una representación de cadena del objeto Regresion

        Returns
        -------
        str: cadena que representa el objeto Regresion
        '''
        return f"\nrecta: {formula_recta(self._m,self._n,self._x,self._y)}\nbondad_del_ajuste: {self._bondad_del_ajuste}\nDescripción: {self._texto}"
        
    def get_m(self):
        '''
        Devuelve una lista con las pendientes

        Returns
        -------
        self._m: list
            valor de m
        '''
        return self._m

    def get_n(self):
        '''
        Devuelve el valor de la ordenada

        Returns
        -------
        self._n: float
            valor de n
        '''
        return self._n

    def get_texto(self):
        '''
        Devuelve la descripcion de la regresion

        Returns
        -------
        self._texto: str
            valor de texto
        '''
        return self._texto

    def get_bondad_del_ajuste(self):
        '''
        Devuelve la bondad del ajuste de la regresion

        Returns
        -------
        self._bondad_del_ajuste: float
            valor de bondad_del_ajuste
        '''
        return self._bondad_del_ajuste

    def get_x(self):
        '''
        Devuelve una lista con las variables independientes

        Returns
        -------
        self._x: list
            valor de x
        '''
        return self._x

    def get_y(self):
        '''
        Devuelve la variable dependiente

        Returns
        -------
        self._y: str
            valor de y
        '''
        return self._y