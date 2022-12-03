from django.shortcuts import render
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
# Create your views here.


def inicio(request):
        
        ret_data = {}
        validacion = ''
        
        if request.method == 'POST':
                
                if request.FILES.get('imagen') == None:
                        validacion = 'Debe cargar la imagen'
                else:
                        ret_data['identificacion'] = identificar_enfermedad(request.FILES.get("imagen"))
                        
                        

        data = {'resultado':ret_data, 'validacion': validacion,
                'sub_carpetas': obtener_sub_carpetas(),}
        return render(request, 'inicio.html',data)






def identificar_enfermedad(photo):
        msg = ''
        try:
                myfile = photo.read()
                image = cv2.imdecode(np.frombuffer(myfile, np.uint8), cv2.IMREAD_UNCHANGED)
                img = cv2.resize(image, (180,180))
                img = img[...,::-1]
                
                train_ds = tf.keras.utils.image_dataset_from_directory(
                        "app_agronomia/IA/Cultivo",
                        validation_split=0.2,
                        subset="training",
                        seed=123,
                        image_size=(180, 180),
                        batch_size=32)
                
                
                #Obtenemos las clases del conjuto de datos
                class_names = train_ds.class_names
                print(class_names)
                model = load_model('C:/Users/Yeltsin/Desktop/Proyecto Agronomia/agronomia/app_agronomia/IA/my_h5_model.h5')
                
                img_array = tf.keras.utils.img_to_array(img)
                img_array = tf.expand_dims(img_array, 0) # Create a batch

                predictions = model.predict(img_array)
                score = tf.nn.softmax(predictions[0])
                text = class_names[np.argmax(score)]
                
                if "hoja_sana" in text:
                        msg = "hoja_sana"
                else:
                        msg = "hoja_enferma"
        

                msg = msg
                
        except Exception as e:
                msg = 'Error: ' + str(e)
                

        return {'tipo_hoja': text.split("_")[0].capitalize(), 'estado_hoja': msg}



def obtener_sub_carpetas():
        try:                
                carpeta = 'C:/Users/Yeltsin/Desktop/Proyecto Agronomia/agronomia/app_agronomia/IA/Cultivo'               
                sub_carpetas = [name for name in os.listdir(carpeta) if os.path.isdir(os.path.join(carpeta, name))]
        except Exception as e:
                sub_carpetas = 'Error al obtener las carpetas'
                
        return sub_carpetas



def entrenamiento(request):
        msg = ""
        nombre = ""
        estado_hoja = ""
        cadena = ""
        
        ret_data = {}
        if request.method == 'POST':
                
                if request.FILES.get('archivo') == None:
                        ret_data['validacion_archivo'] = 'Debe cargar el conjunto de datos de su planta'
                else:
                        ret_data['identificacion'] = identificar_enfermedad(request.FILES.get("imagen"))
                        
                if request.POST.get("nombre") == '':
                        ret_data['validacion_nombre'] = 'Debe ingresar el nombre de la planta'
                else:
                        nombre = request.POST.get("nombre").lower()
                        
                        
                if request.POST.get("salud") == '1':
                        estado_hoja = "hoja_sana"
                else:
                        estado_hoja = "hoja_enferma"

                                
                cadena = nombre + '_' + estado_hoja   

                
        data = {'data':ret_data}
        return render(request, 'entrenamiento.html',data)