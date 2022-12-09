from django.urls import path #Libreria para utilizar path manejo de urls
from app_agronomia.views import *
app_name = 'app_agronomia' #El nombre de nuestra aplicacio

urlpatterns = [
    path("", inicio, name="inicio"),
    path("identificar_enfermedad", identificar_enfermedad, name="identificar_enfermedad"),
    path("entrenamiento", entrenamiento, name="entrenamiento"),
    path("asignacion_enfermedad", asignacion_enfermedad, name="asignacion_enfermedad"),
    path("post_planta", post_planta, name="post_planta"),
    path("post_enfermedad", post_enfermedad, name="post_enfermedad"),
    path("post_asignacion", post_asignacion, name="post_asignacion"),
    path("post_cbo_enfermedades", post_cbo_enfermedades, name="post_cbo_enfermedades")
]