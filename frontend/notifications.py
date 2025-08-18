import requests
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

def enviar_email_solicitud(solicitud):
    """
    Envía un email al administrador cuando se recibe una nueva solicitud
    """
    try:
        asunto = f'Nueva Solicitud de Servicio - {solicitud.servicio.nombre}'
        
        # Preparar el contexto para el template
        contexto = {
            'solicitud': solicitud,
            'servicio': solicitud.servicio,
        }
        
        # Crear el mensaje HTML
        mensaje_html = f"""
        <h2 style="color: #00c3ff;">Nueva Solicitud de Servicio</h2>
        
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #333;">Información del Cliente</h3>
            <p><strong>Nombre:</strong> {solicitud.nombre}</p>
            <p><strong>Email:</strong> {solicitud.email}</p>
            <p><strong>Teléfono:</strong> {solicitud.telefono}</p>
            <p><strong>Dirección:</strong> {solicitud.direccion}</p>
        </div>
        
        <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #333;">Detalles del Servicio</h3>
            <p><strong>Servicio:</strong> {solicitud.servicio.nombre}</p>
            <p><strong>Fecha Preferida:</strong> {solicitud.fecha_preferida}</p>
            <p><strong>Hora Preferida:</strong> {solicitud.hora_preferida}</p>
        </div>
        
        {f'<div style="background: #fff3e0; padding: 20px; border-radius: 8px; margin: 20px 0;"><h3 style="color: #333;">Detalles Adicionales</h3><p>{solicitud.detalles}</p></div>' if solicitud.detalles else ''}
        
        <div style="margin: 30px 0; text-align: center;">
            <p style="color: #666;">Solicitud recibida el {solicitud.fecha_creacion.strftime('%d/%m/%Y a las %H:%M')}</p>
        </div>
        
        <hr>
        <p style="color: #999; font-size: 12px;">
            Este email fue enviado automáticamente desde Professional Clean.<br>
            Por favor, contacta al cliente lo antes posible para confirmar la cita.
        </p>
        """
        
        # Crear versión de texto plano
        mensaje_texto = f"""
Nueva Solicitud de Servicio - {solicitud.servicio.nombre}

INFORMACIÓN DEL CLIENTE:
Nombre: {solicitud.nombre}
Email: {solicitud.email}
Teléfono: {solicitud.telefono}
Dirección: {solicitud.direccion}

DETALLES DEL SERVICIO:
Servicio: {solicitud.servicio.nombre}
Fecha Preferida: {solicitud.fecha_preferida}
Hora Preferida: {solicitud.hora_preferida}

{"DETALLES ADICIONALES: " + solicitud.detalles if solicitud.detalles else ""}

Solicitud recibida el {solicitud.fecha_creacion.strftime('%d/%m/%Y a las %H:%M')}

---
Este email fue enviado automáticamente desde Professional Clean.
Por favor, contacta al cliente lo antes posible para confirmar la cita.
        """
        
        # Enviar el email
        send_mail(
            subject=asunto,
            message=mensaje_texto,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=mensaje_html,
            fail_silently=False,
        )
        
        logger.info(f"Email enviado correctamente para solicitud {solicitud.id}")
        return True
        
    except Exception as e:
        logger.error(f"Error enviando email para solicitud {solicitud.id}: {str(e)}")
        return False

def enviar_whatsapp_notificacion(solicitud):
    """
    Envía una notificación por WhatsApp al administrador
    """
    try:
        # Crear el mensaje para WhatsApp
        mensaje = f"""🔔 *NUEVA SOLICITUD DE SERVICIO*

👤 *Cliente:* {solicitud.nombre}
📞 *Teléfono:* {solicitud.telefono}
📧 *Email:* {solicitud.email}
📍 *Dirección:* {solicitud.direccion}

🧹 *Servicio:* {solicitud.servicio.nombre}
📅 *Fecha:* {solicitud.fecha_preferida.strftime('%d/%m/%Y')}
🕐 *Hora:* {solicitud.hora_preferida}

{f'📝 *Detalles:* {solicitud.detalles}' if solicitud.detalles else ''}

⏰ Solicitud recibida: {solicitud.fecha_creacion.strftime('%d/%m/%Y %H:%M')}

*¡Contacta al cliente pronto para confirmar!*"""
        
        # Configurar la URL de WhatsApp Web/API
        whatsapp_url = f"https://api.whatsapp.com/send?phone={settings.WHATSAPP_NUMBER.replace('+', '')}&text={requests.utils.quote(mensaje)}"
        
        # Si tienes una API de WhatsApp Business configurada, puedes usar esto:
        if settings.WHATSAPP_API_TOKEN and settings.WHATSAPP_API_URL:
            headers = {
                'Authorization': f'Bearer {settings.WHATSAPP_API_TOKEN}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'messaging_product': 'whatsapp',
                'to': settings.WHATSAPP_NUMBER.replace('+', ''),
                'type': 'text',
                'text': {
                    'body': mensaje
                }
            }
            
            response = requests.post(settings.WHATSAPP_API_URL, json=data, headers=headers)
            
            if response.status_code == 200:
                logger.info(f"WhatsApp enviado correctamente para solicitud {solicitud.id}")
                return True
            else:
                logger.error(f"Error enviando WhatsApp para solicitud {solicitud.id}: {response.text}")
                return False
        else:
            # Log para indicar que se debe configurar la API de WhatsApp
            logger.info(f"WhatsApp URL generada para solicitud {solicitud.id}: {whatsapp_url}")
            return True
            
    except Exception as e:
        logger.error(f"Error enviando WhatsApp para solicitud {solicitud.id}: {str(e)}")
        return False

def enviar_confirmacion_cliente(solicitud):
    """
    Envía un email de confirmación al cliente
    """
    try:
        asunto = f'Confirmación de Solicitud - Professional Clean'
        
        mensaje_html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #00c3ff, #0080ff); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">Professional Clean</h1>
                <p style="color: white; margin: 10px 0 0 0; font-size: 16px;">Servicios de Limpieza Profesional</p>
            </div>
            
            <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h2 style="color: #00c3ff; margin-bottom: 20px;">¡Hola {solicitud.nombre}!</h2>
                
                <p style="color: #333; line-height: 1.6; margin-bottom: 20px;">
                    Hemos recibido tu solicitud de servicio y queremos confirmarte que está siendo procesada. 
                    Nos pondremos en contacto contigo pronto para coordinar los detalles.
                </p>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #00c3ff;">
                    <h3 style="color: #333; margin-top: 0;">Resumen de tu solicitud:</h3>
                    <p style="margin: 5px 0;"><strong>Servicio:</strong> {solicitud.servicio.nombre}</p>
                    <p style="margin: 5px 0;"><strong>Fecha preferida:</strong> {solicitud.fecha_preferida.strftime('%d/%m/%Y')}</p>
                    <p style="margin: 5px 0;"><strong>Hora preferida:</strong> {solicitud.hora_preferida}</p>
                    <p style="margin: 5px 0;"><strong>Dirección:</strong> {solicitud.direccion}</p>
                </div>
                
                <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #333; margin-top: 0;">¿Tienes alguna pregunta?</h3>
                    <p style="margin: 10px 0;">Puedes contactarnos directamente:</p>
                    <p style="margin: 5px 0;">📞 WhatsApp: <a href="https://wa.me/573142729812" style="color: #00c3ff;">{settings.WHATSAPP_NUMBER}</a></p>
                    <p style="margin: 5px 0;">📧 Email: <a href="mailto:{settings.ADMIN_EMAIL}" style="color: #00c3ff;">{settings.ADMIN_EMAIL}</a></p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://wa.me/573142729812" style="background: #25D366; color: white; padding: 12px 25px; text-decoration: none; border-radius: 25px; display: inline-block; font-weight: bold;">
                        💬 Contactar por WhatsApp
                    </a>
                </div>
                
                <p style="color: #666; font-size: 14px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                    Gracias por confiar en Professional Clean.<br>
                    <em>Tu satisfacción es nuestra prioridad.</em>
                </p>
            </div>
        </div>
        """
        
        mensaje_texto = f"""
¡Hola {solicitud.nombre}!

Hemos recibido tu solicitud de servicio y queremos confirmarte que está siendo procesada.
Nos pondremos en contacto contigo pronto para coordinar los detalles.

RESUMEN DE TU SOLICITUD:
Servicio: {solicitud.servicio.nombre}
Fecha preferida: {solicitud.fecha_preferida.strftime('%d/%m/%Y')}
Hora preferida: {solicitud.hora_preferida}
Dirección: {solicitud.direccion}

¿TIENES ALGUNA PREGUNTA?
Puedes contactarnos directamente:
WhatsApp: {settings.WHATSAPP_NUMBER}
Email: {settings.ADMIN_EMAIL}

Gracias por confiar en Professional Clean.
Tu satisfacción es nuestra prioridad.
        """
        
        send_mail(
            subject=asunto,
            message=mensaje_texto,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[solicitud.email],
            html_message=mensaje_html,
            fail_silently=False,
        )
        
        logger.info(f"Email de confirmación enviado al cliente {solicitud.email}")
        return True
        
    except Exception as e:
        logger.error(f"Error enviando confirmación al cliente {solicitud.email}: {str(e)}")
        return False
