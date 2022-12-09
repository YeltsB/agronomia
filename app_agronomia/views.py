import base64
from django.http import JsonResponse
from django.shortcuts import redirect, render
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from app_agronomia.models import *

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
        enfermedad = ''
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
                model = load_model('C:/Users/yeltsinbaquedano82/Desktop/agronomia-desarrollo/app_agronomia/IA/my_h5_model.h5')
                
                img_array = tf.keras.utils.img_to_array(img)
                img_array = tf.expand_dims(img_array, 0) # Create a batch

                predictions = model.predict(img_array)
                score = tf.nn.softmax(predictions[0])
                text = class_names[np.argmax(score)]
                
                
                carga = CargaEntrenamiento.objects.get(pk=int(text.split("_")[0]))
                detalle = DetalleEntrenamiento.objects.filter(id_carga_entrenamiento=carga.pk).values()[:1]
                
                planta = Planta.objects.get(pk=carga.id_planta.pk)
                
                if "hoja_sana" in text:
                        msg = "hoja_sana"
                        detalle = DetalleEntrenamiento.objects.filter(id_carga_entrenamiento=carga.pk).values()[:1]
                else:
                        msg = "hoja_enferma"
                        enfermedad = Enfermedad.objects.get(pk=carga.id_enfermedad.pk)
                        
                        
                        
                with open(detalle[0]['url'], "rb") as image_file:
                        img64 = base64.b64encode(image_file.read())        
                        img64 = img64.decode('utf-8')
                        
                msg = msg
                
        except Exception as e:
                msg = 'Error: ' + str(e)
                print(msg)

        return {'tipo_hoja': planta.nombre, 'estado_hoja': msg,'planta':planta,
                'enfermedad':enfermedad, 'img64': img64 }



def obtener_sub_carpetas():
        try:                
                carpeta = 'C:/Users/yeltsinbaquedano82/Desktop/agronomia-desarrollo/app_agronomia/IA/Cultivo'               
                sub_carpetas = [name for name in os.listdir(carpeta) if os.path.isdir(os.path.join(carpeta, name))]
        except Exception as e:
                sub_carpetas = 'Error al obtener las carpetas'
                
        return sub_carpetas



def entrenamiento(request):
        msg = ""
        planta = ""
        enfermedad = ""
        estado_hoja = ""
        cadena = ""
        lista_planta = Planta.objects.all()
        
        ret_data = {}
        query_entrenamiento = {}
        
        
        if request.method == 'POST':
                
                if len(request.FILES.getlist('imagenes')) == 0:
                        ret_data['validacion_archivo'] = 'Debe cargar el conjunto de datos de su planta'
                else:
                        imagenes = request.FILES.getlist('imagenes')
                        
                        
                planta = Planta.objects.get(pk=request.POST.get("planta_select"))
                query_entrenamiento['id_planta']  = planta
                     
                if request.POST.get("salud") == '1':
                        estado_hoja = "hoja_sana"
                        query_entrenamiento['id_enfermedad'] = None
                        query_entrenamiento['esta_sana'] = True
                else:
                        estado_hoja = "hoja_enferma"
                        if request.POST.get("enfermedad_select") == None:
                                ret_data['validacion_enfermedad'] = 'Debe selecionar una enfermedad'
                        else:
                                enfermedad = Enfermedad.objects.get(pk=request.POST.get("enfermedad_select"))
                                query_entrenamiento['id_enfermedad'] = enfermedad
                                query_entrenamiento['esta_sana'] = False
                                
                                

                        
                     
                                
                if 'validacion_archivo' not in ret_data  and 'validacion_enfermedad' not in ret_data:
                        carga = CargaEntrenamiento(**query_entrenamiento)
                        carga.save()
                        cadena = str(carga.pk) + '_' + planta.nombre.lower() + '_' + estado_hoja   
                        ret_data['status'] = entranamiento_tensorflow(cadena,imagenes,carga)

           
        data = {'data':ret_data, 'lista_planta': lista_planta}
        return render(request, 'entrenamiento.html',data)



def entranamiento_tensorflow(cadena,imagenes,carga):
        status = True
        try:
                directorio = "C:/Users/yeltsinbaquedano82/Desktop/agronomia-desarrollo/app_agronomia/IA/Cultivo/"+cadena
                os.mkdir(directorio)
                
                for img in imagenes:
                        with open(directorio +'/'+ str(img), 'wb') as dest:
                                for chunk in img.chunks():
                                        dest.write(chunk)
                                        
                        detalle = DetalleEntrenamiento(id_carga_entrenamiento=carga, url=directorio + '/' +  str(img))
                        detalle.save()             

                                        
                                        
                                        
                                        
                if os.path.exists("C:/Users/yeltsinbaquedano82/Desktop/agronomia-desarrollo/app_agronomia/IA/my_h5_model.h5"):
                        os.remove('C:/Users/yeltsinbaquedano82/Desktop/agronomia-desarrollo/app_agronomia/IA/my_h5_model.h5') 
                        
                                             
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

                model.save("C:/Users/yeltsinbaquedano82/Desktop/agronomia-desarrollo/app_agronomia/IA/my_h5_model.h5")

                
                status = True
        except Exception as e:
                status = False
                print(e)

        return status
        
        
def asignacion_enfermedad(request):
        lista_planta = Planta.objects.all()
        lista_enfermedad = Enfermedad.objects.all()
        lista_asigancion = PlantaEnfermedad.objects.select_related('id_planta', 'id_enfermedad')
        lista_entrenamiento = CargaEntrenamiento.objects.all()
        
        
        
        try:
                if request.session.get('estado_request') == None:
                        status = False
                else:
                        status = request.session.get('estado_request')  
        except Exception as e:
                status = False
                
                        
        data = {'lista_planta':lista_planta, 'lista_enfermedad':lista_enfermedad,
                'lista_asigancion':lista_asigancion, 'lista_entrenamiento':lista_entrenamiento,
                'estatus':status}
        
        request.session['estado_request'] = None 
        return render(request, 'asignacion_enfermedad.html',data)  
        
 #==============================POST==================================================# 
 
def post_planta(request):
        query_planta = {}
        request.session['estado_request'] = False 

                
        if request.method == 'POST':
                query_planta['nombre'] = request.POST.get("nombre_planta")
                query_planta['descripcion'] = request.POST.get("descripcion_planta")
                planta = Planta(**query_planta)
                planta.save()
                request.session['estado_request'] = True 

                        
        #data = {'estatus':estado_request}
        return redirect('/asignacion_enfermedad')



def post_enfermedad(request):
        query_enfermedad = {}
        request.session['estado_request'] = False 

                
        if request.method == 'POST':
                query_enfermedad['nombre'] = request.POST.get("nombre_enfermedad")
                query_enfermedad['descripcion'] = request.POST.get("descripcion_enfermedad")
                enfermedad = Enfermedad(**query_enfermedad)
                enfermedad.save()
                request.session['estado_request'] = True 

                        
        #data = {'estatus':estado_request}
        return redirect('/asignacion_enfermedad')




def post_asignacion(request):
        query_asignacion = {}
        request.session['estado_request'] = False 
               
        if request.method == 'POST':
                query_asignacion['id_planta'] = Planta.objects.get(pk=request.POST.get("planta_select"))
                query_asignacion['id_enfermedad'] = Enfermedad.objects.get(pk=request.POST.get("enfermedad_select"))
       
                #if request.POST.get("estado_select") == "2":


                asignacion = PlantaEnfermedad(**query_asignacion)
                asignacion.save()
                request.session['estado_request'] = True
                
                
        #data = {'estatus':estado_request}
        return redirect('/asignacion_enfermedad')


def post_cbo_enfermedades(request):
        list_enfermedades = []
        
        if request.is_ajax():
                try:
                        id_planta = request.POST.get('id_planta')
                        enfermedades =  PlantaEnfermedad.objects.filter(id_planta=id_planta).values()

                        for enfermedad in enfermedades:
                                enfer = Enfermedad.objects.get(pk=enfermedad['id'])
                                list_enfermedades.append(
                                        {
                                        'id': enfer.pk,
                                        'text': enfer.nombre      
                                        }
                                )
                                #print(str(enfer.pk) + enfer.nombre)
                except Exception as e:
                        list_enfermedades = []
        
        data = {'resp':list_enfermedades}           
        return JsonResponse(data,safe=False)
  