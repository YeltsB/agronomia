from django.urls import path #Libreria para utilizar path manejo de urls
from app_agronomia.views import *
app_name = 'app_agronomia' #El nombre de nuestra aplicacio

urlpatterns = [
    path("", inicio, name="inicio"),
    path("identificar_enfermedad", identificar_enfermedad, name="identificar_enfermedad"),
    path("entrenamiento", entrenamiento, name="entrenamiento"),
    path("asignacion_enfermedad", asignacion_enfermedad, name="asignacion_enfermedad")

]