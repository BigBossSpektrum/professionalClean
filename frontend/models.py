from django.db import models
from django.contrib.auth.models import AbstractUser

class Servicio(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()
	imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)

	def __str__(self):
		return self.nombre

class Usuario(AbstractUser):
	telefono = models.CharField(max_length=20, blank=True)
	direccion = models.CharField(max_length=255, blank=True)

	def __str__(self):
		return self.username

class Solicitud(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
	nombre = models.CharField(max_length=100)
	email = models.EmailField()
	servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
	detalles = models.TextField(blank=True)
	fecha = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.nombre} - {self.servicio.nombre}"
