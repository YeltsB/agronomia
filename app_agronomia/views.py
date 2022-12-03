from django.shortcuts import render
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Create your views here.


def inicio(request):
        
        msg = 'Imagen no cargada'
        validacion = ''
        
        if request.method == 'POST':
                
                if request.FILES.get('imagen') == None:
                        validacion = 'Debe cargar la imagen'
                else:
                        msg = identificar_enfermedad(request.FILES.get("imagen"))
                
        data = {'resultado':msg, 'validacion': validacion}
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
                
                if  text == "hoja_sana":
                        msg = "La hoja que ha ingresado esta sana"
                else:
                        msg = "La hoja que ha ingresado esta enferma"
        

                msg = msg
                
        except Exception as e:
                msg = 'Error: ' + str(e)

        return msg
