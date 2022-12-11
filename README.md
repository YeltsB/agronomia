# Proyecto Inteligencia Artificial UTH
Pasos la configuración del proyecto


## Requisitos
Para ejecutar el proyecto Django en la máquina local es necesario descargar las siguientes librerias:
* [Tensorflow](https://www.tensorflow.org/install)
* [CV2](https://pypi.org/project/opencv-python/)
* [Django](https://www.djangoproject.com/)

### Configuración del proyecto
Es necesario crear una carpeta llamada __Cultivo__ en la ruta: __agronomia/app_agronomia/IA/__
en ella se almacenarán las carpetas e imágenes de cada entrenamiento. Esto se debe realizar ya que la carpeta __IA__
esta ignorada.

Una vez realizada el proceso solo es necesario ejecutar py manage.py runserver donde se encuentra el archivo manage.py
* No es necesario configurar base de datos ni realizar migraciones ya que se utiliza SQLite y ya cuenta con el esquema de
base de datos. 
