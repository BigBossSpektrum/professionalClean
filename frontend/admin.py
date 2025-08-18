from django.contrib import admin
from .models import Servicio, Solicitud, Usuario, ServicioImagen

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('nombre',)

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'servicio', 'fecha_preferida', 'hora_preferida', 'estado', 'fecha_creacion')
    search_fields = ('nombre', 'email', 'telefono', 'servicio__nombre')
    list_filter = ('servicio', 'estado', 'fecha_preferida', 'fecha_creacion')
    readonly_fields = ('fecha_creacion',)
    list_editable = ('estado',)
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('nombre', 'email', 'telefono', 'direccion')
        }),
        ('Detalles del Servicio', {
            'fields': ('servicio', 'fecha_preferida', 'hora_preferida', 'detalles')
        }),
        ('Estado y Tracking', {
            'fields': ('estado', 'usuario', 'fecha_creacion')
        }),
    )

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
