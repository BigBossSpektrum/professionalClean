from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('servicio/<int:servicio_id>/', views.servicio_detalle, name='servicio_detalle'),
    path('usuario/', views.usuario, name='usuario'),
    path('admin-servicio/', views.administrador, name='administrador'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-servicio/editar/<int:servicio_id>/', views.editar_servicio, name='editar_servicio'),
    path('admin-servicio/eliminar/<int:servicio_id>/', views.eliminar_servicio, name='eliminar_servicio'),
    path('admin-servicio/eliminar-imagen/<int:imagen_id>/', views.eliminar_imagen, name='eliminar_imagen'),
    path('contacto-email/', views.contacto_email, name='contacto_email'),
    path('admin-servicio/subir-archivos/<int:servicio_id>/', views.subir_archivos_servicio, name='subir_archivos_servicio'),
]
