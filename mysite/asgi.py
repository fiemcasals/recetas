"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

# Importa el módulo 'os' para interactuar con el sistema operativo
import os

# Importa la función get_asgi_application de Django, que devuelve la aplicación ASGI para el proyecto
from django.core.asgi import get_asgi_application

# Establece la variable de entorno 'DJANGO_SETTINGS_MODULE' si no está ya definida,
# especificando el archivo de configuración de Django a utilizar ('mysite.settings').
# Esta configuración es crucial para que Django sepa qué ajustes cargar.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Asigna la instancia de la aplicación ASGI obtenida de get_asgi_application()
# a la variable 'application', que es utilizada por el servidor ASGI para manejar las solicitudes.
application = get_asgi_application()
