from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('servicio/<int:servicio_id>/', views.servicio_detalle, name='servicio_detalle'),
    path('usuario/', views.usuario, name='usuario'),
    path('admin-servicio/', views.administrador, name='administrador'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
]
