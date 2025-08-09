from django.db import models

class Servicio(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()
	imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)

	def __str__(self):
		return self.nombre

class Solicitud(models.Model):
	nombre = models.CharField(max_length=100)
	email = models.EmailField()
	servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
	detalles = models.TextField(blank=True)
	fecha = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.nombre} - {self.servicio.nombre}"
