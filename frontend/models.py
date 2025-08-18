from django.db import models
from django.contrib.auth.models import AbstractUser


class Servicio(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()

	def __str__(self):
		return self.nombre

class ServicioImagen(models.Model):
	servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='imagenes')
	imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)
	video = models.FileField(upload_to='servicios/videos/', blank=True, null=True)

	def __str__(self):
		return f"Imagen de {self.servicio.nombre}"

	def get_imagen_url(self):
		"""Devuelve la URL de la imagen o una imagen por defecto si no existe o fue borrada."""
		from django.conf import settings
		import os
		if self.imagen and self.imagen.name and self.imagen.storage.exists(self.imagen.name):
			return self.imagen.url
		return settings.STATIC_URL + 'images/default.png'

	def get_video_url(self):
		"""Devuelve la URL del video si existe y el archivo está presente."""
		import os
		if self.video and self.video.name and self.video.storage.exists(self.video.name):
			return self.video.url
		return None

	def has_content(self):
		"""Retorna True si tiene imagen o video válido."""
		return (self.imagen and self.imagen.name and self.imagen.storage.exists(self.imagen.name)) or \
			   (self.video and self.video.name and self.video.storage.exists(self.video.name))

	def get_file_type(self):
		"""Retorna el tipo de archivo: 'image', 'video' o 'both'."""
		has_image = self.imagen and self.imagen.name and self.imagen.storage.exists(self.imagen.name)
		has_video = self.video and self.video.name and self.video.storage.exists(self.video.name)
		
		if has_image and has_video:
			return 'both'
		elif has_image:
			return 'image'
		elif has_video:
			return 'video'
		return 'none'

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
