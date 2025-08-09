from django.shortcuts import render, redirect, get_object_or_404
from .models import Servicio, Solicitud

def home(request):
	servicios = Servicio.objects.all()
	return render(request, 'frontend/home.html', {'servicios': servicios})

def servicio_detalle(request, servicio_id):
	servicio = get_object_or_404(Servicio, pk=servicio_id)
	return render(request, 'frontend/servicio_detalle.html', {'servicio': servicio})

def usuario(request):
	servicios = Servicio.objects.all()
	if request.method == 'POST':
		nombre = request.POST.get('nombre')
		email = request.POST.get('email')
		servicio_id = request.POST.get('servicio')
		detalles = request.POST.get('detalles')
		servicio = Servicio.objects.get(pk=servicio_id)
		Solicitud.objects.create(nombre=nombre, email=email, servicio=servicio, detalles=detalles)
		return redirect('home')
	return render(request, 'frontend/usuario.html', {'servicios': servicios})

def administrador(request):
	if request.method == 'POST':
		nombre = request.POST.get('nombre')
		descripcion = request.POST.get('descripcion')
		imagen = request.FILES.get('imagen')
		Servicio.objects.create(nombre=nombre, descripcion=descripcion, imagen=imagen)
		return redirect('home')
	return render(request, 'frontend/administrador.html')
