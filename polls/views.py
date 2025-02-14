from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import Usuario, Receta, Ingrediente, RecetaIngrediente, UsuarioReceta, Comentario
from .forms import RegistroForm, LoginForm, RecetaForm, IngredienteForm, ComentarioForm
from django.db.models import Avg
from django.views.generic.edit import FormView  
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages  
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Receta, Ingrediente, ListaDeCompras
from .forms import SeleccionarRecetasForm



class RegistroView(FormView):
    template_name = 'polls/registro.html'  # La plantilla donde se mostrará el formulario
    form_class = RegistroForm  # El formulario que se utilizará para registrar al usuario

    def form_valid(self, form):
        # Guardar el usuario con la contraseña encriptada
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])  # Asegurarse de que la contraseña esté encriptada
        user.save()  # Asegurarse de guardar el usuario correctamente

        # Iniciar sesión automáticamente al crear la cuenta
        login(self.request, user)

        # Redirigir a la página de lista de recetas
        return redirect('lista_recetas')

    def form_invalid(self, form):
        # Verificar si las contraseñas no coinciden
        if form.cleaned_data.get('password1') != form.cleaned_data.get('password2'):
            form.add_error('password2', 'Las contraseñas no coinciden.')  # Error personalizado
        
        # Verificar si el correo es válido
        if not form.cleaned_data.get('email'):
            form.add_error('email', 'Por favor, ingresa un correo electrónico válido.')  # Error si el email no es válido

        # Mostrar mensaje de error en la plantilla
        messages.error(self.request, 'Por favor corrige los errores abajo.')
        
        # Mostrar los errores de campo
        return super().form_invalid(form)

# Cierre de sesión
class SalirView(View):
    def get(self, request):
        logout(request)
        return redirect('registro')

# Inicio de sesión
class InicioSesionView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'polls/inicio_sesion.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_recetas_usuario')
            form.add_error(None, 'Credenciales inválidas.')
        return render(request, 'polls/inicio_sesion.html', {'form': form})


# Listado de recetas
class ListaRecetasView(ListView): #ListView: esta view mostrara una lista de objetos de un modelo
    model = Receta #establece cual va a ser el modelo de donde sacar los datos
    template_name = 'polls/lista_recetas.html' #establece a donde va a redireccionar los datos
    context_object_name = 'recetas_con_ingredientes' #se define el nombre con que se pasaran los datos que retornen de esta vista, a la template_name (lista_recetas.html)
    
    def get_queryset(self): #se procede a sobreescribir el metodo get_queryset, con los datos que siguen, definiendo como se obtienen los datos de la tabla a mostrar en la pagina html
        query = self.request.GET.get('q', '').strip()#Se obtiene el parámetro de búsqueda ingresado por el usuario en el template. Si no se proporciona, se usa una cadena vacía. es decir, levanta todas las recetas, sin filtrarlas
        recetas = Receta.objects.all()#se obtienen todos los objetos del modelo "receta"
        
        # Si hay un término de búsqueda, filtra las recetas
        if query:
            recetas = recetas.filter(
                        Q(titulo__icontains=query) | #filtra por titulo comparado con q
                        Q(categoria__icontains=query) |#idema para bajo, esta vez por la categoria..
                        Q(dificultad__icontains=query) |
                        Q(ingredientes__nombre__icontains=query)
            ).distinct() #evita que aparezcan duplicados. ej: si el titulo y la categoria tienen la palabra, sin el distinct, apareceria dos veces
        
        # Prefetch de los ingredientes para cada receta
        recetas = recetas.prefetch_related('ingredientes') #carga los ingredientes de la receta
        
        return recetas


from django.views.generic import ListView
from django.db.models import Q
from .models import Receta

from django.shortcuts import render
from .models import HistorialCocinado


class ListaMisRecetasView(ListView):
    model = Receta
    template_name = 'polls/lista_recetas_propias.html'
    context_object_name = 'recetas'  
    
    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        recetas = Receta.objects.filter(usuario=self.request.user).prefetch_related('ingredientes')
        
        if query:
            recetas = recetas.filter(
                Q(titulo__icontains=query) |
                Q(categoria__icontains=query) |
                Q(dificultad__icontains=query) |
                Q(ingredientes__nombre__icontains=query)
            ).distinct() #evita que aparezcan duplicados. ej: si el titulo y la categoria tienen la palabra, sin el distinct, apareceria dos veces
        
        return recetas  # Esto ahora devuelve un queryset válido
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Construir el diccionario de recetas con ingredientes
        recetas_con_ingredientes = {}
        for receta in context['recetas']:
            recetas_con_ingredientes[receta] = {
                'ingredientes': receta.ingredientes.all(),
                'detalles': receta
            }
        
        # Agregar al contexto
        context['recetas_con_ingredientes'] = recetas_con_ingredientes
           
        return context


# Creación de recetas
import json
from django.shortcuts import redirect

import json
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Receta, Ingrediente, RecetaIngrediente
from .forms import RecetaForm

class IngresarRecetaView(LoginRequiredMixin, CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'polls/ingresar_receta.html'
    success_url = '/lista_recetas/'

    def form_valid(self, form):
        # Guardar la receta sin confirmarla en la base de datos.
        receta = form.save(commit=False)
        # Asignar el usuario autenticado a la receta.
        receta.usuario = self.request.user
        receta.save()
        # Asignar la receta a self.object para que get_success_url() funcione.
        self.object = receta
        print(f"Receta guardada: {receta}")

        # Obtener ingredientes desde el campo oculto 'ingredientes_json'
        ingredientes_json = self.request.POST.get('ingredientes_json')
        if ingredientes_json:
            try:
                # Convertir JSON a lista de diccionarios.
                ingredientes = json.loads(ingredientes_json)
                for ingrediente_data in ingredientes:
                    nombre = ingrediente_data['nombre']
                    cantidad = ingrediente_data['cantidad']
                    unidad = ingrediente_data['unidad']
                    
                    # Buscar si el ingrediente ya existe, o crearlo con valores por defecto
                    ingrediente, created = Ingrediente.objects.get_or_create(
                        nombre=nombre,
                        defaults={'cantidad': cantidad, 'unidad': unidad}
                    )
                    
                    # Crear la relación en RecetaIngrediente para asociar el ingrediente a la receta
                    RecetaIngrediente.objects.create(
                        receta=receta,
                        ingrediente=ingrediente,
                        cantidad=cantidad,
                        unidad=unidad
                    )
            except Exception as e:
                print("Error al procesar ingredientes JSON:", e)
        else:
            print("No se envió JSON de ingredientes.")
        
        # Redirigir a la URL de éxito.
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print("Formulario no válido:", form.errors)
        return super().form_invalid(form)



# Edición de recetas
class EditarRecetaView(LoginRequiredMixin, UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'polls/editar_receta.html'
    success_url = '/lista_recetas/'

# Asociación de receta a usuario
class AsociarRecetaAUsuarioView(LoginRequiredMixin, View):
    def post(self, request, receta_id):
        receta = get_object_or_404(Receta, id=receta_id)
        if not UsuarioReceta.objects.filter(usuario=request.user, receta=receta).exists():
            UsuarioReceta.objects.create(usuario=request.user, receta=receta)
        return redirect('lista_recetas')

# Comentarios y calificaciones
from django.shortcuts import get_object_or_404, redirect  # Importa funciones de Django para obtener objetos o redirigir
from django.http import HttpResponseForbidden  # Permite devolver una respuesta con error 403 (prohibido)
from .models import Receta, Comentario  # Importa los modelos de Receta y Comentario que se utilizarán

# Definición de la clase basada en vista para agregar un comentario

class AgregarComentarioView(View):
    
    # Método GET: Mostrar el formulario para agregar comentario
    def get(self, request, receta_id):
        receta = get_object_or_404(Receta, id=receta_id)
        form = ComentarioForm()  # Crear un formulario vacío
        comentarios = Comentario.objects.filter(receta=receta)  # Obtener los comentarios de la receta
        return render(request, 'polls/comentarios_calificaciones.html', {'form': form, 'receta': receta, 'comentarios': comentarios})

    # Método POST: Procesar el formulario con informacion recibido
    def post(self, request, receta_id):
        receta = get_object_or_404(Receta, id=receta_id)
        form = ComentarioForm(request.POST)  # Recibir los datos del formulario enviado
        
        if form.is_valid():  # Verificar si los datos son válidos
            comentario = form.save(commit=False)
            comentario.usuario = request.user  # Asignar al usuario autenticado
            comentario.receta = receta  # Asociar la receta
            comentario.save()  # Guardar el comentario en la base de datos
            
            return redirect('comentarios_calificaciones', receta_id=receta.id)
        
        # Si el formulario no es válido, devolver un mensaje de error
        return JsonResponse({'error': 'Formulario no válido'}, status=400)
    

class UsuarioListaView(ListView):
    model = Usuario
    template_name = 'polls/usuario_lista.html'
    context_object_name = 'usuarios'



#lista de compras
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Receta, Ingrediente, ListaDeCompras
from .forms import SeleccionarRecetasForm

# Vista para seleccionar recetas
class SeleccionarRecetasView(LoginRequiredMixin, FormView):
    template_name = 'polls/seleccionar_recetas.html'
    form_class = SeleccionarRecetasForm
    success_url = '/lista_compras/'

    def form_valid(self, form):
        return self.generar_lista_compras(form.cleaned_data['recetas'])

    def generar_lista_compras(self, recetas_seleccionadas):
        lista_compras = []

        for receta in recetas_seleccionadas:
            for ingrediente in receta.ingredientes.all():
                lista_compras.append(
                    ListaDeCompras(
                        usuario=self.request.user,
                        receta=receta,
                        ingrediente=ingrediente,
                        cantidad=ingrediente.cantidad,
                        unidad=ingrediente.unidad
                    )
                )

        ListaDeCompras.objects.bulk_create(lista_compras)
        return redirect('ver_lista_compras')

# Vista para mostrar la lista de compras
from django.http import JsonResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import ListaDeCompras

class ListaComprasView(LoginRequiredMixin, ListView):
    model = ListaDeCompras
    template_name = 'polls/lista_compras.html'
    context_object_name = 'lista_compras'

    def get_queryset(self):
        return ListaDeCompras.objects.filter(usuario=self.request.user)

    def post(self, request, *args, **kwargs):
        """ Maneja la eliminación de un ingrediente de la lista de compras vía AJAX. """
        item_id = request.POST.get("item_id")
        item = get_object_or_404(ListaDeCompras, id=item_id, usuario=request.user)
        item.delete()
        
        return JsonResponse({"success": True, "item_id": item_id})
# views.py
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Receta
from django.contrib.auth.decorators import login_required
from django.views import View

@method_decorator(login_required, name='dispatch')
class MarcarFavoritoView(View):
    def post(self, request, pk):
        # Obtener la receta por su ID
        receta = get_object_or_404(Receta, pk=pk)
        
        # Comprobar si la receta ya está en los favoritos
        if receta in request.user.favoritos.all():
            request.user.favoritos.remove(receta)  # Eliminar de favoritos
            new_state = False
            mensaje = "Receta eliminada de favoritos"
        else:
            request.user.favoritos.add(receta)  # Añadir a favoritos
            new_state = True
            mensaje = "Receta añadida a favoritos"

        # Devolver un JSON con el estado de la receta y el mensaje
        return JsonResponse({'mensaje': mensaje, 'nuevo_estado': new_state}, status=200)



class ListaFavoritasView(ListView):
    model = Receta
    template_name = 'polls/recetas_favoritas.html'
    context_object_name = 'recetas_favoritas'
    
    def get_queryset(self):
        # Obtiene las recetas favoritas del usuario logueado
        return self.request.user.favoritos.all()

#historial recetas cocinadas

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Receta, HistorialCocinado
from django.http import JsonResponse

class RegistrarCocinadoView(LoginRequiredMixin, View):
    def post(self, request, receta_id):
        receta = get_object_or_404(Receta, id=receta_id)
        HistorialCocinado.objects.create(usuario=request.user, receta=receta)
        return JsonResponse({'mensaje': 'Registro actualizado'}, status=200)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import HistorialCocinado

class HistorialCocinadoView(LoginRequiredMixin, ListView):
    model = HistorialCocinado
    template_name = 'polls/historial_cocinados.html'
    context_object_name = 'historial'
    ordering = ['-fecha_cocinado']

    def get_queryset(self):
        return HistorialCocinado.objects.filter(usuario=self.request.user).order_by('-fecha_cocinado')


#estadisticas y reportes 

from django.shortcuts import render
from django.views import View
from django.db.models import Count
from .models import HistorialCocinado, Receta


class ReporteEstadisticasView(View):
    def get(self, request):
        # Lógica para obtener estadísticas
        recetas_cocinadas = HistorialCocinado.objects.values('receta__titulo').annotate(total_cocinados=Count('receta')).order_by('-total_cocinados')
        categorias_populares = Receta.objects.values('categoria').annotate(cantidad=Count('categoria')).order_by('-cantidad')
        recetas_usuario = HistorialCocinado.objects.filter(usuario=request.user).values('receta__titulo').annotate(total_cocinados=Count('receta')).order_by('-total_cocinados')
        total_recetas_cocinadas = HistorialCocinado.objects.filter(usuario=request.user).count()

        # Pasar los datos al contexto
        context = {
            'recetas_cocinadas': recetas_cocinadas,
            'categorias_populares': categorias_populares,
            'recetas_usuario': recetas_usuario,
            'total_recetas_cocinadas': total_recetas_cocinadas
        }
        return render(request, 'polls/reporte_estadisticas.html', context)


import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.db.models import Count
from .models import HistorialCocinado, Receta

class ExportarEstadisticasCSVView(View):
    def get(self, request):
        # Lógica para obtener las estadísticas
        recetas_cocinadas = HistorialCocinado.objects.values('receta__titulo').annotate(total_cocinados=Count('receta')).order_by('-total_cocinados')
        categorias_populares = Receta.objects.values('categoria').annotate(cantidad=Count('categoria')).order_by('-cantidad')
        recetas_usuario = HistorialCocinado.objects.filter(usuario=request.user).values('receta__titulo').annotate(total_cocinados=Count('receta')).order_by('-total_cocinados')
        total_recetas_cocinadas = HistorialCocinado.objects.filter(usuario=request.user).count()

        # Crear una respuesta CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="estadisticas_recetas.csv"'

        writer = csv.writer(response)
        
        # Escribir los encabezados
        writer.writerow(['Estadísticas de Recetas'])
        
        # Recetas más cocinadas
        writer.writerow(['Receta', 'Total Cocinados'])
        for receta in recetas_cocinadas:
            writer.writerow([receta['receta__titulo'], receta['total_cocinados']])
        
        writer.writerow([])  # Salto de línea
        
        # Categorías más populares
        writer.writerow(['Categoría', 'Cantidad de Recetas'])
        for categoria in categorias_populares:
            writer.writerow([categoria['categoria'], categoria['cantidad']])
        
        writer.writerow([])  # Salto de línea
        
        # Recetas cocinadas por el usuario
        writer.writerow(['Mis Recetas Cocinadas'])
        writer.writerow(['Receta', 'Total Cocinados'])
        for receta in recetas_usuario:
            writer.writerow([receta['receta__titulo'], receta['total_cocinados']])

        writer.writerow([])  # Salto de línea
        
        # Total de recetas cocinadas
        writer.writerow(['Total Recetas Cocinadas por el Usuario', total_recetas_cocinadas])

        return response

#comentario


# polls/views.py
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Comentario, Receta
from .forms import ComentarioForm
from django.urls import reverse_lazy




#notificaciones
from django.shortcuts import render
from django.views.generic import ListView


class NotificacionesView(LoginRequiredMixin, ListView):
    model = Comentario #el tipo de objeto que esta pasando
    template_name = "polls/notificaciones.html"
    context_object_name = "notificaciones" #es el nombre del objeto que se usara en el contexto(en la plantilla html)

    def get_queryset(self):
        return Comentario.objects.filter(receta__usuario=self.request.user).order_by('-fecha_creacion')


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View


class MarcarNotificacionLeidaView(LoginRequiredMixin, View):
    def post(self, request, comentario_id):
        comentario = get_object_or_404(Comentario, id=comentario_id, receta__usuario=request.user)
        comentario.leida = True
        comentario.save()
        return JsonResponse({'mensaje': 'Notificación marcada como leída'})
