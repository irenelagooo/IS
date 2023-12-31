# Manual de usuario
Esta aplicación crea modelos de regresión lineal simple y múltiple a partir de datos almacenados en archivos csv, excel o bases de datos. Permite visualizar la regresión, tras seleccionar las variables independientes y la variable dependiente, y hacer predicciones del modelo. Además, se podrán guardar modelos para no volverlos a calcular y luego cargarlos en la aplicación para hacer predicciones sobre ellos. La aplicación tiene una interfaz gráfica que permite hacer todas las acciones anteriores.

Para utilizar esta aplicación, abra el símbolo de sistema e instale las siguientes librerías, poniendo pip install seguido del nombre de la librería que quiera instalar:
- pandas
- tkinter
- matplotlib
  
Además, si no tiene instalado python en su ordenador, ejecute el comando python3 --version (sustituyendo 'version' por la versión de python que desea instalar).
Para iniciar la aplicación, ejecute el comando python gui.py (siendo gui.py el nombre del fichero principal, si se llama de otra forma poner otro nombre).

Inicie la aplicación y se mostrará la interfaz gráfica de usuario. Si quiere cargar un archivo para calcular la regresión, pulse el botón de cargar archivo y seleccione el archivo de su equipo.
A continuación, se mostrarán las variables X e Y que podrá seleccionar. Escoja una variable Y y tantas variables X como desee y pulse el botón de Calcular regresión. 

Si desea guardar el modelo calculado, pulse el botón Descargar Modelo y escriba una descripción en el campo de texto que se abrirá al pulsar el botón. Escoja el directorio donde prefiera guardar el modelo.

Si desea cargar un modelo guardado, pulse el botón Cargar Regresión y seleccione el documento con la regresión guardada. A continuación, se mostrará la fórmula de la recta de regresión, la bondad del ajuste y el texto descriptivo del modelo. 

Para hacer predicciones, tras cargar un modelo o calcular una regresión aparecerán unos cuadros donde podrá introducir el valor de las variables X de los que desee calcular la Y. Introduzca los valores y, al pulsar el botón Calcular Predicción, aparecerán los resultados en la ventana.
