# Professional Clean - Sistema de Notificaciones 🧹✨

Sistema completo de gestión de solicitudes de servicios de limpieza con notificaciones automáticas por email y WhatsApp.

## 🚀 Características Implementadas

### ✅ Formulario de Solicitud Completo
- Información del cliente (nombre, email, teléfono, dirección)
- Selección de servicio de limpieza
- Programación de fecha y hora
- Detalles adicionales
- Validación completa frontend y backend

### ✅ Sistema de Notificaciones Automáticas
- **📧 Email al administrador** con todos los detalles de la solicitud
- **📱 Notificación WhatsApp** al administrador
- **📬 Email de confirmación** al cliente
- Templates HTML profesionales con branding

### ✅ Galería de Imágenes 360°
- Auto-scroll horizontal de derecha a izquierda
- Lightbox para vista ampliada
- Soporte para imágenes y videos
- Efectos visuales y animaciones

### ✅ Panel de Administración
- Gestión completa de solicitudes
- Estados de seguimiento (Pendiente, Confirmado, Realizado, Cancelado)
- Filtros y búsquedas
- Vista detallada de clientes

## 🛠️ Configuración Rápida

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Email (Gmail)
```bash
# Copia el archivo de configuración
cp config.env.template .env

# Edita .env con tus credenciales:
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicacion
ADMIN_EMAIL=donde-recibes-solicitudes@gmail.com
```

**Importante para Gmail:**
1. Activa la verificación en 2 pasos
2. Genera una "Contraseña de aplicación"
3. Usa esa contraseña (NO tu contraseña normal)

### 3. Configurar WhatsApp
```bash
# En tu archivo .env:
WHATSAPP_NUMBER=+57123456789
```

### 4. Aplicar Migraciones
```bash
python manage.py migrate
```

### 5. Ejecutar Servidor
```bash
python manage.py runserver
```

## 🧪 Probar el Sistema

### Prueba Automática
```bash
python test_notifications.py
```

### Prueba Manual
1. Ve a http://localhost:8000/usuario/
2. Completa el formulario
3. Verifica que recibas:
   - Email en tu bandeja de administrador
   - Notificación WhatsApp
   - Cliente recibe confirmación

## 📱 URLs Principales

- **🏠 Página Principal**: `/`
- **📝 Solicitar Servicio**: `/usuario/`
- **🔧 Panel Admin**: `/admin/`
- **📊 Administrador**: `/administrador/`

## 🔧 Archivos Principales

### Backend
- `frontend/models.py` - Modelos de datos
- `frontend/views.py` - Lógica de negocio
- `frontend/notifications.py` - Sistema de notificaciones
- `frontend/admin.py` - Panel de administración

### Frontend
- `templates/frontend/usuario.html` - Formulario de solicitud
- `templates/frontend/home.html` - Página principal con galería
- `templates/frontend/administrador.html` - Panel de administrador
- `static/styles.css` - Estilos personalizados

### Configuración
- `profesionalClean/settings.py` - Configuración Django
- `requirements.txt` - Dependencias Python
- `config.env.template` - Plantilla de configuración

## 📧 Templates de Email

### Email al Administrador
- Información completa del cliente
- Detalles del servicio solicitado
- Formato HTML profesional
- Todos los datos de contacto

### Email al Cliente
- Confirmación de solicitud recibida
- Resumen del servicio
- Información de contacto directo
- Branding Professional Clean

## 📱 Integración WhatsApp

### Notificación Automática
- Mensaje estructurado con emojis
- Todos los datos del cliente
- Información del servicio
- Timestamp de la solicitud

### Opciones de Integración
1. **WhatsApp Web** (Por defecto) - Enlaces directos
2. **WhatsApp Business API** - Envío automático real

## 🛡️ Seguridad

- ✅ Protección CSRF en formularios
- ✅ Validación de datos backend
- ✅ Sanitización de inputs
- ✅ Variables de entorno para credenciales

## 🚀 Deploy en Producción

### Variables de Entorno Requeridas
```bash
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-aplicacion
ADMIN_EMAIL=admin@professionalclean.com
WHATSAPP_NUMBER=+573142729812
DATABASE_URL=postgresql://... (para producción)
```

### Render.com
- El proyecto está configurado para Render
- `render.yaml` incluido
- PostgreSQL configurado
- WhiteNoise para archivos estáticos

## 📞 Soporte

Si tienes alguna pregunta o necesitas ayuda:

1. **📧 Email**: Revisa la configuración de Gmail
2. **📱 WhatsApp**: Verifica el número en settings.py
3. **🐛 Errores**: Revisa los logs del servidor
4. **🧪 Testing**: Usa `test_notifications.py`

## 🎨 Personalización

### Cambiar Colores
Edita `static/styles.css` y busca `#00c3ff` para cambiar el color principal.

### Modificar Templates
Los emails se generan en `frontend/notifications.py` - edita las variables `mensaje_html`.

### Agregar Campos
1. Actualiza el modelo en `frontend/models.py`
2. Crea migración: `python manage.py makemigrations`
3. Aplica: `python manage.py migrate`
4. Actualiza el formulario en `templates/frontend/usuario.html`

---

**Professional Clean** - Tu sistema de gestión de servicios de limpieza 🏆
