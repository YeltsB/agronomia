from django.db import models

# Create your models here.
class Enfermedad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Enfermedad"
        verbose_name_plural = "Enfermedades"
        
    def __str__(self):
        return "{}--{}".format(self.pk,self.nombre)
    
    
class Planta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250)
    class Meta:
        verbose_name = "Planta"
        verbose_name_plural = "Plantas"
        
    def __str__(self):
        return "{}--{}".format(self.pk,self.nombre)

  
class PlantaEnfermedad(models.Model):
    id_planta = models.ForeignKey(Planta, verbose_name='Planta', on_delete=models.CASCADE)
    id_enfermedad = models.ForeignKey(Enfermedad, verbose_name='Enfermedad', on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Plan Enfermedad"
        verbose_name_plural = "Plantas Efermedades"
        
    def __str__(self):
        return "{}--{}--{}".format(self.pk,self.id_enfermedad,self.id_enfermedad.nombre)

    
class CargaEntrenamiento(models.Model):
    id_planta = models.ForeignKey(Planta, verbose_name='Planta', on_delete=models.CASCADE)
    id_enfermedad = models.ForeignKey(Enfermedad, null=True, verbose_name='Enfermedad', on_delete=models.CASCADE)
    esta_sana = models.BooleanField()

    def __str__(self):
        return "{}--{}".format(self.pk,self.esta_sana)

    
class DetalleEntrenamiento(models.Model):
    id_carga_entrenamiento = models.ForeignKey(CargaEntrenamiento, verbose_name='Carga Entrenamiento', on_delete=models.CASCADE)
    url = models.CharField(max_length=250)
        
    def __str__(self):
        return "{}--{}--{}".format(self.pk,self.id_carga_entrenamiento,self.url)

        