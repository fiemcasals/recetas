"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""


import os

# Construye rutas dentro del proyecto, como por ejemplo: os.path.join(BASE_DIR, ...)
# 'BASE_DIR' es la ruta base de tu proyecto, normalmente el directorio donde se encuentra el archivo settings.py.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ADVERTENCIA DE SEGURIDAD: ¡mantén la clave secreta utilizada en producción secreta!
SECRET_KEY = 'di0wk-ix&28fpsqdd&tubbd1(%cukzgvfyxgkh%%6c48=z3_6c'

# ADVERTENCIA DE SEGURIDAD: ¡no ejecutes el proyecto con 'DEBUG' activado en producción!
DEBUG = True

# Hosts permitidos. Especifica los dominios que pueden acceder a tu aplicación.
# Si está vacío, se permiten todas las direcciones.
ALLOWED_HOSTS = []

# Definición de las aplicaciones de la web

INSTALLED_APPS = [
    # Aplicaciones de Django que están preinstaladas
    'django.contrib.admin',  # Para el panel de administración de Django
    'django.contrib.auth',   # Para la gestión de usuarios
    'django.contrib.contenttypes',  # Para el manejo de tipos de contenido
    'django.contrib.sessions',  # Para gestionar sesiones
    'django.contrib.messages',  # Para manejar mensajes a los usuarios
    'django.contrib.staticfiles',  # Para gestionar archivos estáticos como CSS y JS
    'polls.apps.PollsConfig',  # La aplicación 'polls' (en este caso es una app personalizada)
    'recetas',
    
    
]

# Middleware
# El middleware son componentes que procesan las solicitudes y respuestas
# que pasan a través del servidor de Django.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Middleware de seguridad
    'django.contrib.sessions.middleware.SessionMiddleware',  # Maneja las sesiones
    'django.middleware.common.CommonMiddleware',  # Middleware general
    'django.middleware.csrf.CsrfViewMiddleware',  # Protege contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Maneja la autenticación de usuarios
    'django.contrib.messages.middleware.MessageMiddleware',  # Maneja los mensajes flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protege contra ataques de clickjacking
    
]


# Configuración de las URL raíz de la aplicación
ROOT_URLCONF = 'mysite.urls'

# Configuración de las plantillas HTML (temas o vistas)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Motor de plantillas de Django
        'DIRS': [],  # Se especifican los directorios donde Django buscará las plantillas, si están disponibles
        'APP_DIRS': True,  # Si se deben buscar plantillas dentro de las aplicaciones instaladas
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Procesador de contexto para el modo de depuración
                'django.template.context_processors.request',  # Procesador para manejar objetos request
                'django.contrib.auth.context_processors.auth',  # Procesador para manejar datos de autenticación
                'django.contrib.messages.context_processors.messages',  # Procesador para manejar los mensajes de usuarios
            ],
        },
    },
]

# Aplicación WSGI para el proyecto
WSGI_APPLICATION = 'mysite.wsgi.application'

# Configuración de la base de datos
# Django utiliza bases de datos para almacenar información
# Aquí se especifica que se usará SQLite como base de datos
# Y se guarda el archivo de base de datos en la misma carpeta que el archivo settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Motor de base de datos: SQLite
        'NAME': os.path.join(BASE_DIR, 'database.sqlite3'),  # Ruta al archivo de base de datos
    }
}


# Validación de contraseñas
# Esto ayuda a aplicar políticas de contraseñas seguras
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Valida que el usuario no use atributos similares a su nombre
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Valida que la contraseña tenga una longitud mínima
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Valida que la contraseña no sea común
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Valida que la contraseña no sea solo numérica
    },
]


# Internacionalización
# Configura el idioma y la zona horaria del proyecto
LANGUAGE_CODE = 'en-us'  # Establece el idioma de la aplicación (inglés de Estados Unidos)

TIME_ZONE = 'UTC'  # Establece la zona horaria del proyecto (UTC)

USE_I18N = True  # Activa la internacionalización (i18n) para traducir la aplicación

USE_L10N = True  # Activa la localización (l10n) para el formato de datos (fechas, números, etc.)

USE_TZ = True  # Activa el uso de zonas horarias en el proyecto

# Archivos estáticos (CSS, JavaScript, Imágenes)
# Aquí se configura la ruta a los archivos estáticos (archivos que no cambian como CSS y JS)
STATIC_URL = '/static/'  # Ruta en la URL donde se pueden encontrar los archivos estáticos

# Configuración para campos automáticos en modelos (por defecto, usa un campo AutoField para los IDs)
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Directorios donde buscar archivos estáticos adicionales (fuera de las aplicaciones Django)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'polls/static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



AUTH_USER_MODEL = 'polls.Usuario'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Backend de autenticación predeterminado
]

LOGIN_URL = '/home/mauri/Documentos/FIE/4to/SegundoCuatrimestre/PP5/django-original/ejemplo-django/polls/templates/polls/registro.html'  # Cambia esta ruta según tu configuración

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False  # Cambia esto a True si estás usando HTTPS
