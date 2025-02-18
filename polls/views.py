from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Avg, Count
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import Receta, Ingrediente, RecetaIngrediente, UsuarioReceta, Comentario, ListaDeCompras, HistorialCocinado, Perfil
from .forms import RegistroForm, LoginForm, RecetaForm, IngredienteForm, ComentarioForm, SeleccionarRecetasForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import json
import csv

# Registro de usuario utilizando la clase User
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
class ListaRecetasView(ListView):
    model = Receta
    template_name = 'polls/lista_recetas.html'
    context_object_name = 'recetas_con_ingredientes'
    
    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        recetas = Receta.objects.all()
        
        if query:
            recetas = recetas.filter(
                        Q(titulo__icontains=query) |
                        Q(categoria__icontains=query) |
                        Q(dificultad__icontains=query) |
                        Q(ingredientes__nombre__icontains=query)
            ).distinct()
        
        recetas = recetas.prefetch_related('ingredientes')
        
        return recetas


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
            ).distinct()
        
        return recetas
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        recetas_con_ingredientes = {}
        for receta in context['recetas']:
            recetas_con_ingredientes[receta] = {
                'ingredientes': receta.ingredientes.all(),
                'detalles': receta
            }
        
        context['recetas_con_ingredientes'] = recetas_con_ingredientes
           
        return context


class IngresarRecetaView(LoginRequiredMixin, CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'polls/ingresar_receta.html'
    success_url = '/lista_recetas/'

    def form_valid(self, form):
        receta = form.save(commit=False)
        receta.usuario = self.request.user
        receta.save()
        self.object = receta
        print(f"Receta guardada: {receta}")

        ingredientes_json = self.request.POST.get('ingredientes_json')
        if ingredientes_json:
            try:
                ingredientes = json.loads(ingredientes_json)
                for ingrediente_data in ingredientes:
                    nombre = ingrediente_data['nombre']
                    cantidad = ingrediente_data['cantidad']
                    unidad = ingrediente_data['unidad']
                    
                    ingrediente, created = Ingrediente.objects.get_or_create(
                        nombre=nombre,
                        defaults={'cantidad': cantidad, 'unidad': unidad}
                    )
                    
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

class AgregarComentarioView(View):
    # Método GET: Mostrar el formulario para agregar comentario
    def get(self, request, receta_id):
        receta = get_object_or_404(Receta, id=receta_id)
        form = ComentarioForm()  # Crear un formulario vacío
        comentarios = Comentario.objects.filter(receta=receta)  # Obtener los comentarios de la receta
        return render(request, 'polls/comentarios_calificaciones.html', {'form': form, 'receta': receta, 'comentarios': comentarios})

    # Método POST: Procesar el formulario con información recibida
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

class UsuarioListaView(LoginRequiredMixin, ListView):
    model = User  # Utilizando el modelo User de Django
    template_name = 'polls/usuario_lista.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        """Devuelve la lista de usuarios, puede filtrarse si es necesario."""
        return User.objects.all() 


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


class ListaComprasView(LoginRequiredMixin, ListView):
    model = ListaDeCompras
    template_name = 'polls/lista_compras.html'
    context_object_name = 'lista_compras'

    def get_queryset(self):
        # Obtener la lista de compras del usuario logueado
        return ListaDeCompras.objects.filter(usuario=self.request.user)

    def post(self, request, *args, **kwargs):
        """ Maneja la eliminación de un ingrediente de la lista de compras vía AJAX. """
        item_id = request.POST.get("item_id")
        item = get_object_or_404(ListaDeCompras, id=item_id, usuario=request.user)
        item.delete()

        return JsonResponse({"success": True, "item_id": item_id})


@method_decorator(login_required, name='dispatch')
class MarcarFavoritoView(View):
    def post(self, request, pk):
        receta = get_object_or_404(Receta, pk=pk)

        # Comprobar si el usuario tiene un perfil. Si no lo tiene, crear uno.
        perfil, created = Perfil.objects.get_or_create(user=request.user)

        # Verificar si la receta ya está en los favoritos
        if receta in perfil.favoritos.all():
            perfil.favoritos.remove(receta)  # Eliminar de favoritos
            new_state = False
            mensaje = "Receta eliminada de favoritos"
        else:
            perfil.favoritos.add(receta)  # Añadir a favoritos
            new_state = True
            mensaje = "Receta añadida a favoritos"

        return JsonResponse({'mensaje': mensaje, 'nuevo_estado': new_state}, status=200)



class ListaFavoritasView(ListView):
    model = Receta
    template_name = 'polls/recetas_favoritas.html'
    context_object_name = 'recetas_favoritas'
    
    def get_queryset(self):
        # Verifica si el usuario tiene un perfil asociado
        perfil = getattr(self.request.user, 'perfil', None)
        if perfil:
            # Si tiene perfil, devuelve las recetas favoritas
            return perfil.favoritos.all()
        else:
            # Si no tiene perfil, retorna un conjunto vacío o el comportamiento que desees
            return Receta.objects.none()


#historial recetas cocinadas

class RegistrarCocinadoView(LoginRequiredMixin, View):
    def post(self, request, receta_id):
        receta = get_object_or_404(Receta, id=receta_id)
        # Verificar si la receta ya está registrada
        HistorialCocinado.objects.create(usuario=request.user, receta=receta)
            
        return redirect('historial/')


class HistorialCocinadoView(LoginRequiredMixin, ListView):
    model = HistorialCocinado
    template_name = 'polls/historial_cocinados.html'
    context_object_name = 'historial'
    ordering = ['-fecha_cocinado']

    def get_queryset(self):
        return HistorialCocinado.objects.filter(usuario=self.request.user).order_by('-fecha_cocinado')


#estadisticas y reportes 



class ReporteEstadisticasView(View):
    def get(self, request):
        recetas_cocinadas = HistorialCocinado.objects.values('receta__titulo').annotate(total_cocinados=Count('receta')).order_by('-total_cocinados')
        categorias_populares = Receta.objects.values('categoria').annotate(cantidad=Count('categoria')).order_by('-cantidad')
        recetas_usuario = HistorialCocinado.objects.filter(usuario=request.user).values('receta__titulo').annotate(total_cocinados=Count('receta')).order_by('-total_cocinados')
        total_recetas_cocinadas = HistorialCocinado.objects.filter(usuario=request.user).count()

        context = {
            'recetas_cocinadas': recetas_cocinadas,
            'categorias_populares': categorias_populares,
            'recetas_usuario': recetas_usuario,
            'total_recetas_cocinadas': total_recetas_cocinadas
        }

        return render(request, 'polls/reporte_estadisticas.html', context)



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




class NotificacionesView(LoginRequiredMixin, ListView):
    model = Comentario #el tipo de objeto que esta pasando
    template_name = "polls/notificaciones.html"
    context_object_name = "notificaciones" #es el nombre del objeto que se usara en el contexto(en la plantilla html)

    def get_queryset(self):
        return Comentario.objects.filter(receta__usuario=self.request.user).order_by('-fecha_creacion')



class MarcarNotificacionLeidaView(View):
    def post(self, request, notificacion_id):
        # Obtén el comentario por ID y asegúrate de que es del usuario actual
        comentario = get_object_or_404(Comentario, id=notificacion_id)
        
        # Cambia el estado de "leída" (si es True se pone False, si es False se pone True)
        comentario.leida = not comentario.leida
        comentario.save()

        # Devuelve el nuevo estado de "leída"
        return JsonResponse({"nuevo_estado": comentario.leida})

      
