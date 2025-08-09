from django.contrib.auth.decorators import login_required

@login_required(login_url='admin_login')
def editar_servicio(request, servicio_id):
	servicio = get_object_or_404(Servicio, pk=servicio_id)
	if not request.user.is_staff:
		return redirect('admin_login')
	if request.method == 'POST':
		servicio.nombre = request.POST.get('nombre')
		servicio.descripcion = request.POST.get('descripcion')
		servicio.save()
		nuevas_imagenes = request.FILES.getlist('imagenes')
		for img in nuevas_imagenes:
			ServicioImagen.objects.create(servicio=servicio, imagen=img)
		return redirect('administrador')
	return render(request, 'frontend/editar_servicio.html', {'servicio': servicio})

@login_required(login_url='admin_login')
def eliminar_servicio(request, servicio_id):
	servicio = get_object_or_404(Servicio, pk=servicio_id)
	if not request.user.is_staff:
		return redirect('admin_login')
	if request.method == 'POST':
		servicio.delete()
		return redirect('administrador')
	return render(request, 'frontend/eliminar_servicio.html', {'servicio': servicio})

@login_required(login_url='admin_login')
def eliminar_imagen(request, imagen_id):
	imagen = get_object_or_404(ServicioImagen, pk=imagen_id)
	if not request.user.is_staff:
		return redirect('admin_login')
	servicio_id = imagen.servicio.id
	imagen.delete()
	return redirect('editar_servicio', servicio_id=servicio_id)
from django.shortcuts import render, redirect, get_object_or_404
from .models import Servicio, Solicitud, Usuario, ServicioImagen
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

def home(request):
	servicios = Servicio.objects.all()
	return render(request, 'frontend/home.html', {'servicios': servicios})

def servicio_detalle(request, servicio_id):
	servicio = get_object_or_404(Servicio, pk=servicio_id)
	return render(request, 'frontend/servicio_detalle.html', {'servicio': servicio})

def usuario(request):
	servicios = Servicio.objects.all()
	if request.method == 'POST':
		servicio_id = request.POST.get('servicio')
		detalles = request.POST.get('detalles')
		servicio = Servicio.objects.get(pk=servicio_id)
		if request.user.is_authenticated:
			Solicitud.objects.create(
				usuario=request.user,
				nombre=request.user.get_full_name() or request.user.username,
				email=request.user.email,
				servicio=servicio,
				detalles=detalles
			)
		else:
			nombre = request.POST.get('nombre')
			email = request.POST.get('email')
			Solicitud.objects.create(
				nombre=nombre,
				email=email,
				servicio=servicio,
				detalles=detalles
			)
		return redirect('home')
	return render(request, 'frontend/usuario.html', {'servicios': servicios})



from django.middleware.csrf import get_token

def admin_login(request):
	# Configurar el tiempo de expiración de sesión a 10 minutos
	request.session.set_expiry(600)
	csrf_token = get_token(request)
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		try:
			user_obj = Usuario.objects.get(username=username)
		except Usuario.DoesNotExist:
			user_obj = None
		user = authenticate(request, username=username, password=password)
		if user is not None and user_obj is not None and user_obj.is_staff:
			login(request, user)
			return redirect('administrador')
		else:
			messages.error(request, 'Credenciales inválidas o usuario sin permisos de administrador.')
	return render(request, 'frontend/admin_login.html', {'csrf_token': csrf_token})

@login_required(login_url='admin_login')
def admin_logout(request):
	logout(request)
	messages.success(request, 'Sesión cerrada correctamente.')
	return redirect('home')

@login_required(login_url='admin_login')
def administrador(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	if request.method == 'POST':
		nombre = request.POST.get('nombre')
		descripcion = request.POST.get('descripcion')
		imagenes = request.FILES.getlist('imagenes')
		servicio = Servicio.objects.create(nombre=nombre, descripcion=descripcion)
		for img in imagenes:
			ServicioImagen.objects.create(servicio=servicio, imagen=img)
		return redirect('home')
	servicios = Servicio.objects.all()
	return render(request, 'frontend/administrador.html', {'servicios': servicios})
