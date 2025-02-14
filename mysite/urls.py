"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# registrar y gestionar los modelos a través de la interfaz de administración de Django.
from django.contrib import admin

# Se importa 'path' y 'include' desde 'django.urls'. 'path' se usa para definir rutas en la URL,
# y 'include' se usa para incluir otras configuraciones de URLs desde otros archivos de aplicaciones.
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# Aquí se define la lista de patrones de URL del proyecto, conocida como 'urlpatterns'.
urlpatterns = [
    # Esta línea indica que cuando la URL raíz ('') es visitada, Django debe incluir los patrones
    # de URL definidos en el archivo 'urls.py' de la aplicación 'polls'. Esto se logra con 'include'.
    path('', include('polls.urls')),

    # Esta línea define un patrón de URL para acceder a la interfaz de administración de Django.
    # Cuando el usuario visite '/admin/', se redirigirá al sistema de administración proporcionado
    # por Django para gestionar modelos y otros aspectos del sitio.
    path('admin/', admin.site.urls),

    # Tus otras URL patterns aquí
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

