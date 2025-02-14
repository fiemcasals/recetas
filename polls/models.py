import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.conf import settings


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2)  # Asegúrate de que este campo existe
    unidad = models.CharField(max_length=50)  # Asegúrate de que este campo existe

    def __str__(self):
        return self.nombre

from django.conf import settings
from django.db import models

from django.conf import settings
from django.db import models

class Receta(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(default="Descripción no disponible")
    imagen = models.ImageField(upload_to='recetas/', null=True, blank=True)
    pasos_de_preparacion = models.TextField()
    categoria = models.CharField(max_length=50)
    dificultad = models.CharField(max_length=50)
    tiempo_de_coccion = models.IntegerField()
    # Definición de la relación ManyToMany usando un modelo intermedio
    ingredientes = models.ManyToManyField(Ingrediente, through='RecetaIngrediente', blank=True)
    # Relación con el modelo Usuario para favoritos
    favoritos = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favoritos_recetas', blank=True)
    
    def __str__(self):
        return self.titulo

class Usuario(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=False)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    # Relación muchos a muchos con Receta para almacenar los favoritos
    favoritos = models.ManyToManyField('Receta', related_name='usuarios_favoritos', blank=True)
    
    def clean(self):
        if not self.username.strip():
            raise ValidationError("El nombre de usuario no puede estar vacío.")
    
    def __str__(self):  
        return f"{self.first_name} {self.last_name}"
    
class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2)  # Cantidad específica para esta receta
    unidad = models.CharField(max_length=50)  # Unidad específica para esta receta

    def __str__(self):
        return f"{self.cantidad} {self.unidad} de {self.ingrediente.nombre} para {self.receta.titulo}"

    
class UsuarioReceta(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="usuario_recetas")
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name="receta_usuarios")
    
    class Meta:
        unique_together = ('usuario', 'receta')
    
    def __str__(self):
        return f"Usuario: {self.usuario} - Receta: {self.receta}"


class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comentarios')
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='comentarios')
    comentario = models.TextField()
    calificacion = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Comentario de {self.usuario} para {self.receta}"




#lista de compras

class ListaDeCompras(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2)  # Cantidad necesaria para la receta
    unidad = models.CharField(max_length=50)  # Unidad de medida del ingrediente

    def __str__(self):
        return f"Lista de compras para {self.receta.titulo} - {self.ingrediente.nombre}"


#historial de comidas
from django.db import models

class HistorialCocinado(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receta = models.ForeignKey('Receta', on_delete=models.CASCADE)
    fecha_cocinado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} cocinó {self.receta.titulo} el {self.fecha_cocinado}"


#comentarios dirigidos
# polls/models.py
    
class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comentarios')
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='comentarios')
    comentario = models.TextField()
    calificacion = models.PositiveIntegerField()
    leida = models.BooleanField(default=False)  # Para marcar si fue leída
    fecha_creacion = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"Comentario de {self.usuario} para {self.receta}"

