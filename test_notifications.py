#!/usr/bin/env python
"""
Utilidad de prueba para el sistema de notificaciones de Professional Clean
===========================================================================

Este script te permite probar las notificaciones de email y WhatsApp
sin necesidad de enviar el formulario completo.

Uso:
    python test_notifications.py

"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'profesionalClean.settings')
django.setup()

from frontend.models import Servicio, Solicitud
from frontend.notifications import enviar_email_solicitud, enviar_whatsapp_notificacion, enviar_confirmacion_cliente
from datetime import date, datetime

def crear_solicitud_prueba():
    """Crea una solicitud de prueba para testear las notificaciones"""
    
    # Obtener o crear un servicio de prueba
    servicio, created = Servicio.objects.get_or_create(
        nombre="Limpieza de Prueba",
        defaults={'descripcion': 'Servicio de prueba para testear notificaciones'}
    )
    
    # Crear solicitud de prueba
    solicitud = Solicitud.objects.create(
        nombre="Cliente de Prueba",
        email="cliente.prueba@email.com",
        telefono="+57300123456",
        direccion="Calle Falsa 123, Bogotá",
        servicio=servicio,
        fecha_preferida=date.today(),
        hora_preferida="10:00",
        detalles="Esta es una solicitud de prueba para verificar que las notificaciones funcionan correctamente."
    )
    
    return solicitud

def test_notificaciones():
    """Prueba el sistema completo de notificaciones"""
    
    print("🔧 Probando Sistema de Notificaciones - Professional Clean")
    print("=" * 60)
    
    # Crear solicitud de prueba
    print("📝 Creando solicitud de prueba...")
    solicitud = crear_solicitud_prueba()
    print(f"✅ Solicitud creada con ID: {solicitud.id}")
    
    # Probar email al administrador
    print("\n📧 Probando email al administrador...")
    try:
        resultado_email = enviar_email_solicitud(solicitud)
        if resultado_email:
            print("✅ Email al administrador enviado correctamente")
        else:
            print("❌ Error enviando email al administrador")
    except Exception as e:
        print(f"❌ Error en email al administrador: {e}")
    
    # Probar notificación WhatsApp
    print("\n📱 Probando notificación WhatsApp...")
    try:
        resultado_whatsapp = enviar_whatsapp_notificacion(solicitud)
        if resultado_whatsapp:
            print("✅ Notificación WhatsApp procesada correctamente")
        else:
            print("❌ Error en notificación WhatsApp")
    except Exception as e:
        print(f"❌ Error en WhatsApp: {e}")
    
    # Probar confirmación al cliente
    print("\n📬 Probando confirmación al cliente...")
    try:
        resultado_confirmacion = enviar_confirmacion_cliente(solicitud)
        if resultado_confirmacion:
            print("✅ Confirmación al cliente enviada correctamente")
        else:
            print("❌ Error enviando confirmación al cliente")
    except Exception as e:
        print(f"❌ Error en confirmación al cliente: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Prueba completada!")
    print("\n💡 Notas importantes:")
    print("   - Si ves errores, verifica las configuraciones en settings.py")
    print("   - Para emails: configura EMAIL_HOST_USER y EMAIL_HOST_PASSWORD")
    print("   - Para WhatsApp: configura WHATSAPP_NUMBER")
    print("   - Revisa la consola del servidor para más detalles")
    
    # Limpiar solicitud de prueba
    print(f"\n🧹 Eliminando solicitud de prueba (ID: {solicitud.id})")
    solicitud.delete()
    print("✅ Limpieza completada")

if __name__ == "__main__":
    test_notificaciones()
