from django.contrib import admin
from .models import Servicio, Solicitud, Usuario, ServicioImagen

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('nombre',)

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'servicio', 'detalles', 'fecha')
    search_fields = ('usuario__username', 'servicio__nombre')
    list_filter = ('servicio', 'fecha')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')

@admin.register(ServicioImagen)
class ServicioImagenAdmin(admin.ModelAdmin):
    list_display = ('id', 'servicio', 'imagen')
    search_fields = ('servicio__nombre',)
    list_filter = ('servicio',)
