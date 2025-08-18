from django.core.mail import send_mail
from django.http import JsonResponse
def contacto_email(request):
	if request.method == 'POST':
		nombre = request.POST.get('nombre')
		email = request.POST.get('email')
		mensaje = request.POST.get('mensaje')
		asunto = f'Nuevo mensaje de contacto de {nombre}'
		cuerpo = f'Nombre: {nombre}\nEmail: {email}\nMensaje:\n{mensaje}'
		send_mail(
			asunto,
			cuerpo,
			email,  # El remitente será el usuario que envía el mensaje
			[settings.DEFAULT_FROM_EMAIL],  # El destinatario es tu correo
			fail_silently=False,
		)
		return JsonResponse({'success': True})
	return JsonResponse({'success': False}, status=400)
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

# Vista para subir imágenes y videos por el admin
from django.shortcuts import render, redirect, get_object_or_404
from .models import Servicio, ServicioImagen
from django.contrib import messages

@login_required(login_url='admin_login')
def subir_archivos_servicio(request, servicio_id):
	servicio = get_object_or_404(Servicio, pk=servicio_id)
	if not request.user.is_staff:
		return redirect('admin_login')
	if request.method == 'POST':
		imagenes = request.FILES.getlist('imagenes')
		videos = request.FILES.getlist('videos')
		archivos_guardados = 0
		errores = []
		# Guardar imágenes
		for img in imagenes:
			if img.content_type.startswith('image/'):
				ServicioImagen.objects.create(servicio=servicio, imagen=img)
				archivos_guardados += 1
			else:
				errores.append(f"Archivo '{img.name}' no es una imagen válida.")
		# Guardar videos
		for vid in videos:
			if vid.content_type.startswith('video/'):
				ServicioImagen.objects.create(servicio=servicio, video=vid)
				archivos_guardados += 1
			else:
				errores.append(f"Archivo '{vid.name}' no es un video válido.")
		if archivos_guardados > 0:
			messages.success(request, f"{archivos_guardados} archivo(s) subido(s) correctamente.")
		if errores:
			for error in errores:
				messages.error(request, error)
		return redirect('administrador')
	return redirect('administrador')

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
	from .notifications import enviar_email_solicitud, enviar_whatsapp_notificacion, enviar_confirmacion_cliente
	servicios = Servicio.objects.all()
	
	if request.method == 'POST':
		try:
			# Obtener todos los datos del formulario
			nombre = request.POST.get('nombre')
			email = request.POST.get('email')
			telefono = request.POST.get('telefono')
			direccion = request.POST.get('direccion')
			servicio_id = request.POST.get('servicio')
			fecha_preferida = request.POST.get('fecha')
			hora_preferida = request.POST.get('hora')
			detalles = request.POST.get('detalles', '')
			
			# Validar que todos los campos requeridos estén presentes
			if not all([nombre, email, telefono, direccion, servicio_id, fecha_preferida, hora_preferida]):
				return JsonResponse({
					'success': False, 
					'error': 'Todos los campos son obligatorios'
				})
			
			# Obtener el servicio
			servicio = Servicio.objects.get(pk=servicio_id)
			
			# Crear la solicitud
			solicitud = Solicitud.objects.create(
				usuario=request.user if request.user.is_authenticated else None,
				nombre=nombre,
				email=email,
				telefono=telefono,
				direccion=direccion,
				servicio=servicio,
				fecha_preferida=fecha_preferida,
				hora_preferida=hora_preferida,
				detalles=detalles
			)
			
			# Enviar notificaciones
			email_enviado = enviar_email_solicitud(solicitud)
			whatsapp_enviado = enviar_whatsapp_notificacion(solicitud)
			confirmacion_enviada = enviar_confirmacion_cliente(solicitud)
			
			return JsonResponse({
				'success': True,
				'message': 'Solicitud enviada correctamente. Te contactaremos pronto.',
				'solicitud_id': solicitud.id,
				'notificaciones': {
					'email_admin': email_enviado,
					'whatsapp': whatsapp_enviado,
					'confirmacion_cliente': confirmacion_enviada
				}
			})
			
		except Servicio.DoesNotExist:
			return JsonResponse({
				'success': False, 
				'error': 'El servicio seleccionado no existe'
			})
		except Exception as e:
			return JsonResponse({
				'success': False, 
				'error': f'Error procesando la solicitud: {str(e)}'
			})
	
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
		videos = request.FILES.getlist('videos')
		
		servicio = Servicio.objects.create(nombre=nombre, descripcion=descripcion)
		archivos_guardados = 0
		errores = []
		
		# Procesar imágenes
		for img in imagenes:
			if img and hasattr(img, 'name') and img.size > 0:
				if img.content_type.startswith('image/'):
					ServicioImagen.objects.create(servicio=servicio, imagen=img)
					archivos_guardados += 1
				else:
					errores.append(f"'{img.name}' no es una imagen válida.")
		
		# Procesar videos
		for vid in videos:
			if vid and hasattr(vid, 'name') and vid.size > 0:
				if vid.content_type.startswith('video/'):
					ServicioImagen.objects.create(servicio=servicio, video=vid)
					archivos_guardados += 1
				else:
					errores.append(f"'{vid.name}' no es un video válido.")
		
		if archivos_guardados > 0:
			messages.success(request, f"Servicio '{nombre}' creado con {archivos_guardados} archivo(s).")
		if errores:
			for error in errores:
				messages.error(request, error)
		
		# Limpieza: eliminar registros huérfanos
		ServicioImagen.objects.filter(imagen='', video='').delete()
		return redirect('administrador')
	
	servicios = Servicio.objects.all()
	return render(request, 'frontend/administrador.html', {'servicios': servicios})
