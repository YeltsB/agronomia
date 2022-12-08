from django.shortcuts import render
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

import os
import patoolib
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
        text = ''
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
                #print(text)

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
                
                if request.FILES.getlist('imagenes') == None:
                        ret_data['validacion_archivo'] = 'Debe cargar el conjunto de datos de su planta'
                else:
                        imagenes = request.FILES.getlist('imagenes')
                        
                if request.POST.get("nombre") == '':
                        ret_data['validacion_nombre'] = 'Debe ingresar el nombre de la planta'
                else:
                        nombre = request.POST.get("nombre").lower()
                        
                        
                if request.POST.get("salud") == '1':
                        estado_hoja = "hoja_sana"
                else:
                        estado_hoja = "hoja_enferma"

                                
                cadena = nombre + '_' + estado_hoja   
                

                if 'validacion_archivo' not in ret_data  and 'validacion_nombre' not in ret_data:
                        ret_data['status'] = entranamiento_tensorflow(cadena,imagenes)

                
        data = {'data':ret_data}
        return render(request, 'entrenamiento.html',data)



def entranamiento_tensorflow(cadena,imagenes):
        status = True
        try:
                directorio = "C:/Users/Yeltsin/Desktop/Proyecto Agronomia/agronomia/app_agronomia/IA/Cultivo/"+cadena
                os.mkdir(directorio)
                
                for img in imagenes:
                        with open(directorio +'/'+ str(img), 'wb') as dest:
                                for chunk in img.chunks():
                                        dest.write(chunk)
                                        
                                        
                                        
                if os.path.exists("C:/Users/Yeltsin/Desktop/Proyecto Agronomia/agronomia/app_agronomia/IA/my_h5_model.h5"):
                        os.remove('C:/Users/Yeltsin/Desktop/Proyecto Agronomia/agronomia/app_agronomia/IA/my_h5_model.h5') 
                        
                                             
                train_ds = tf.keras.utils.image_dataset_from_directory(
                        "app_agronomia/IA/Cultivo",
                        validation_split=0.2,
                        subset="training",
                        seed=123,
                        image_size=(180, 180),
                        batch_size=32)
                                       
                class_names = train_ds.class_names
                
                normalization_layer = layers.Rescaling(1./255)
                normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
                image_batch, labels_batch = next(iter(normalized_ds))
                first_image = image_batch[0]
                
                #Creacion del modelo
                num_classes = len(class_names)

                model = Sequential([
                layers.Rescaling(1./255, input_shape=(180, 180, 3)),
                layers.Conv2D(16, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(),
                layers.Conv2D(32, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(),
                layers.Conv2D(64, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(),
                layers.Flatten(),
                layers.Dense(128, activation='relu'),
                layers.Dense(num_classes)
                ])

                #Complicacion y optimizacion del modelo
                model.compile(optimizer='adam',
                        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                        metrics=['accuracy'])

                model.summary()

                #Entranamiento del modelo y numero de ciclos
                epochs=30
                history = model.fit(
                train_ds,
                epochs=epochs
                )

                model.save("C:/Users/Yeltsin/Desktop/Proyecto Agronomia/agronomia/app_agronomia/IA/my_h5_model.h5")
                
                
                status = True
        except Exception as e:
                status = False

        return status
        
        
def asignacion_enfermedad(request):
        ret_data = {}
        validacion = ''
        
        if request.method == 'POST':
                pass
                        
        data = {'resultado':"ret_data"}
        return render(request, 'asignacion_enfermedad.html',data)  
        
 #==============================POST==================================================# 
 
 
       