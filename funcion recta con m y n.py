def calcular_recta_regresion(m, n, x_values):
    """
    Calcula la recta de regresión lineal dados los parámetros m y n.

    Parámetros:
    - m: Pendiente de la recta de regresión.
    - n: Ordenada al origen de la recta de regresión.
    - x_values: Valores de la variable X para los cuales se calculará la recta.

    Devuelve:
    - y_values: Valores de la variable Y correspondientes a la recta de regresión.
    """
    y_values = [m * x + n for x in x_values]
    return y_values